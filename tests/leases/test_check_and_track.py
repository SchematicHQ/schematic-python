"""The client-mode check and settle flow against scripted stores and engine.

Ports schematic-node's check-and-track suite. The engine is scripted rather
than real (``test_wasm_credit_gate`` drives the real one), so what these pin is
the orchestration: which balance the engine is handed, when a hold is taken,
and what happens to it when something downstream says no.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import pytest
from lease_support import ScriptedDataStream, ScriptedWireClient, VirtualClock, make_fake_redis

from schematic.client import CheckOptions, CheckResult, Reservation
from schematic.leases import (
    CreditCheckDeps,
    InMemoryLeaseStore,
    InMemoryReservationStore,
    LeaseConfig,
    LeaseManager,
    LeaseStore,
    RedisLeaseStore,
    RedisReservationStore,
    ReservationRecord,
    ReservationStore,
    ReserveResult,
    check_with_lease,
    consume_reservation_and_build_event,
)
from schematic.leases.check import FAIL_OPEN_BALANCE
from schematic.types import (
    EventBodyFlagCheck,
    RulesengineCheckFlagResult,
    RulesengineFeatureEntitlement,
    RulesengineUser,
)

FLAG_KEY = "inference"
CREDIT_ID = "bilcr_inference"
EVENT_SUBTYPE = "inference_tokens"
LEASE_SIZE = 1000.0
LEASE_DURATION = 300.0
COMPANY = {"id": "co_1"}

CREDIT_ENTITLEMENT = RulesengineFeatureEntitlement(
    feature_id="feat",
    feature_key=FLAG_KEY,
    value_type="credit",
    credit_id=CREDIT_ID,
    consumption_rate=10,
    event_subtype=EVENT_SUBTYPE,
)


def _verdict(
    value: bool, reason: str, entitlement: Optional[RulesengineFeatureEntitlement] = None,
) -> RulesengineCheckFlagResult:
    return RulesengineCheckFlagResult(
        value=value, reason=reason, flag_key=FLAG_KEY, flag_id="flag_1", entitlement=entitlement
    )


class FlowEngine:
    """The engine the lease path asks twice: the probe, then the gate.

    The gate is the call carrying ``credit_cost``, which is also what puts the
    fail-open re-evaluation on the probe branch, as it is in the reference
    implementation.
    """

    def __init__(
        self,
        *,
        probe: Optional[RulesengineCheckFlagResult] = None,
        gate: Optional[RulesengineCheckFlagResult] = None,
        probe_error: Optional[Exception] = None,
        gate_error: Optional[Exception] = None,
    ) -> None:
        self.probe = probe if probe is not None else _verdict(True, "probe", CREDIT_ENTITLEMENT)
        self.gate = gate if gate is not None else _verdict(True, "matched", CREDIT_ENTITLEMENT)
        self.probe_error = probe_error
        self.gate_error = gate_error
        self.calls: List[Dict[str, Any]] = []

    def __call__(self, flag: Any, company: Any, user: Any, options: Any = None) -> RulesengineCheckFlagResult:
        gating = bool(options is not None and getattr(options, "credit_cost", None))
        self.calls.append({"company": company, "user": user, "options": options, "gating": gating})
        if gating:
            if self.gate_error is not None:
                raise self.gate_error
            return self.gate
        if self.probe_error is not None:
            raise self.probe_error
        return self.probe

    @property
    def gate_call(self) -> Optional[Dict[str, Any]]:
        return next((call for call in self.calls if call["gating"]), None)

    def balance(self, index: int) -> float:
        return float(self.calls[index]["company"].credit_balances[CREDIT_ID])


class _ProbeThenExplodes(FlowEngine):
    """Answers the probe, then fails every evaluation after it."""

    def __call__(self, flag: Any, company: Any, user: Any, options: Any = None) -> RulesengineCheckFlagResult:
        result = super().__call__(flag, company, user, options)
        if len(self.calls) > 1:
            raise RuntimeError("wasm exploded")
        return result


class Fallback:
    """The plain flag check the lease path defers to."""

    def __init__(self) -> None:
        self.called = False

    async def __call__(self) -> CheckResult:
        self.called = True
        return CheckResult(allowed=True, value=True, reason="fallback", flag_key=FLAG_KEY)


class UnreachableLeaseStore(InMemoryLeaseStore):
    """A store that can be read but never debited, as an unreachable Redis is."""

    async def try_reserve(
        self, company_id: str, credit_type_id: str, credits: float
    ) -> Optional[ReserveResult]:
        raise RuntimeError("redis down")


class RecordedFlagChecks:
    """Stands in for the client's event buffer so the tests can see what the
    lease path reported."""

    def __init__(self) -> None:
        self.events: List[EventBodyFlagCheck] = []
        self.explode = False

    async def __call__(self, body: EventBodyFlagCheck) -> None:
        if self.explode:
            raise RuntimeError("event buffer down")
        self.events.append(body)


@dataclass
class Flow:
    deps: CreditCheckDeps
    engine: FlowEngine
    wire: ScriptedWireClient
    leases: LeaseStore
    reservations: ReservationStore
    manager: LeaseManager
    flag_checks: RecordedFlagChecks = field(default_factory=RecordedFlagChecks)
    fallback: Fallback = field(default_factory=Fallback)

    async def check(self, **option_overrides: Any) -> CheckResult:
        options = CheckOptions(usage=50, event_subtype=EVENT_SUBTYPE)
        for name, value in option_overrides.items():
            setattr(options, name, value)
        result = await check_with_lease(self.deps, FLAG_KEY, COMPANY, None, options, self.fallback)
        await self.manager._drain_background()
        return result

    async def remaining(self) -> Optional[float]:
        entry = await self.leases.get(COMPANY["id"], CREDIT_ID)
        return entry.local_remaining_credits if entry is not None else None


def make_flow(
    clock: VirtualClock,
    *,
    engine: Optional[FlowEngine] = None,
    lease_store: Optional[LeaseStore] = None,
    reservation_store: Optional[ReservationStore] = None,
    acquire: str = "ok",
    credit_balances: Optional[Dict[str, float]] = None,
    **datastream_kwargs: Any,
) -> Flow:
    engine = engine or FlowEngine()
    leases = lease_store if lease_store is not None else InMemoryLeaseStore(clock=clock)
    reservations = (
        reservation_store if reservation_store is not None else InMemoryReservationStore(leases, clock=clock)
    )
    wire = ScriptedWireClient()
    if acquire == "ok":
        wire.acquire_responses.append(
            {"lease": {"lease_id": "lse_1", "granted_amount": LEASE_SIZE, "expires_at": clock() + LEASE_DURATION}}
        )
    elif acquire == "error":
        wire.acquire_responses.append({"error": "lease 503"})
    manager = LeaseManager(
        wire,
        leases,
        reservation_store=reservations,
        config=LeaseConfig(
            lease_duration=LEASE_DURATION, reservation_ttl=60.0, lease_size=LEASE_SIZE, low_water_mark=0.25
        ),
        clock=clock,
    )
    datastream = ScriptedDataStream(
        engine,
        FLAG_KEY,
        {"id": COMPANY["id"], "credit_balances": credit_balances if credit_balances is not None else {CREDIT_ID: 5000}},
        **datastream_kwargs,
    )
    flag_checks = RecordedFlagChecks()
    return Flow(
        deps=CreditCheckDeps(
            datastream=datastream,
            lease_store=leases,
            reservations=reservations,
            manager=manager,
            logger=logging.getLogger("lease-flow-test"),
            enqueue_flag_check=flag_checks,
            clock=clock,
        ),
        engine=engine,
        wire=wire,
        leases=leases,
        reservations=reservations,
        manager=manager,
        flag_checks=flag_checks,
    )


class TestCheckWithLease:
    async def test_issues_a_reservation_when_the_engine_allows(self, clock: VirtualClock) -> None:
        flow = make_flow(clock)
        result = await flow.check()

        assert result.allowed is True
        assert result.reservation is not None
        assert result.reservation.mode == "client"
        assert result.reservation.lease_id == "lse_1"
        assert result.reservation.quantity_reserved == 50
        assert result.reservation.credits_reserved == 500
        assert result.reservation.consumption_rate == 10
        assert len(flow.wire.acquire_calls) == 1
        # The probe sees the company's real balance; the gate sees the
        # pre-reservation lease balance and the cost this call just debited.
        assert flow.engine.balance(0) == 5000
        assert flow.engine.balance(1) == LEASE_SIZE
        assert flow.engine.gate_call is not None
        assert flow.engine.gate_call["options"].credit_cost == {CREDIT_ID: 500}
        assert await flow.remaining() == 500
        assert await flow.reservations.count() == 1

    async def test_leases_the_credit_the_matched_entitlement_names(self, clock: VirtualClock) -> None:
        # Entitlement-first resolution: the credit and the rate come off the
        # probe's entitlement, whatever the flag's conditions look like.
        ai_entitlement = RulesengineFeatureEntitlement(
            feature_id="feat",
            feature_key=FLAG_KEY,
            value_type="credit",
            credit_id="bilcr_ai",
            consumption_rate=5,
            event_subtype=EVENT_SUBTYPE,
        )
        engine = FlowEngine(
            probe=_verdict(True, "probe", ai_entitlement), gate=_verdict(True, "matched", ai_entitlement)
        )
        flow = make_flow(clock, engine=engine)
        flow.wire.acquire_responses[0]["lease"]["lease_id"] = "lse_ai"
        result = await flow.check()

        assert result.reservation is not None
        assert result.reservation.credit_type_id == "bilcr_ai"
        assert result.reservation.consumption_rate == 5
        assert result.reservation.credits_reserved == 250
        assert flow.wire.acquire_calls[0]["credit_type_id"] == "bilcr_ai"
        assert len(flow.engine.calls) == 2

    async def test_skips_the_lease_when_the_entitlement_is_not_credit_metered(self, clock: VirtualClock) -> None:
        # A boolean grant (an override, say) draws no credit, so the lease path
        # never acquires: the plain check decides, with no reserve to cancel.
        entitlement = RulesengineFeatureEntitlement(feature_id="feat", feature_key=FLAG_KEY, value_type="boolean")
        flow = make_flow(clock, engine=FlowEngine(probe=_verdict(True, "override", entitlement)))
        result = await flow.check()

        assert flow.fallback.called is True
        assert result.allowed is True
        assert result.reservation is None
        assert flow.wire.acquire_calls == []
        assert flow.engine.gate_call is None

    async def test_denies_and_refunds_when_the_gate_denies(self, clock: VirtualClock) -> None:
        flow = make_flow(clock, engine=FlowEngine(gate=_verdict(False, "denied_by_targeting")))
        result = await flow.check()

        assert result.allowed is False
        assert result.reason == "denied_by_targeting"
        assert result.reservation is None
        assert await flow.remaining() == LEASE_SIZE
        assert await flow.reservations.count() == 0

    async def test_fails_closed_when_the_acquire_fails(self, clock: VirtualClock) -> None:
        flow = make_flow(clock, acquire="error")
        result = await flow.check(on_acquire_failure="fail-closed")

        assert result.allowed is False
        assert result.reason == "lease_acquire_failed"
        assert result.error == "lease_acquire_failed"
        assert result.reservation is None
        assert flow.engine.gate_call is None

    async def test_defaults_to_fail_closed(self, clock: VirtualClock) -> None:
        flow = make_flow(clock, acquire="error")
        result = await flow.check()

        assert result.allowed is False
        assert result.reservation is None

    async def test_fail_open_re_evaluates_with_the_balance_assumed_sufficient(self, clock: VirtualClock) -> None:
        flow = make_flow(clock, acquire="error")
        result = await flow.check(on_acquire_failure="fail-open")

        assert result.allowed is True
        assert result.error == "lease_acquire_failed"
        assert result.reservation is None
        # Fail-open runs the rules, it does not skip them: only the credit
        # balance is assumed sufficient, and the caller's usage still rides in.
        assert flow.engine.balance(1) == FAIL_OPEN_BALANCE
        preflight = flow.engine.calls[1]["options"].event_usage
        assert (preflight.event_subtype, preflight.quantity) == (EVENT_SUBTYPE, 50)

    async def test_fail_open_still_denies_a_company_the_rules_do_not_entitle(self, clock: VirtualClock) -> None:
        flow = make_flow(
            clock,
            engine=FlowEngine(probe=_verdict(False, "no matching rule", CREDIT_ENTITLEMENT)),
            acquire="error",
        )
        result = await flow.check(on_acquire_failure="fail-open")

        assert result.allowed is False
        assert result.reason == "no matching rule (lease_acquire_failed_fail_open)"
        assert result.error == "lease_acquire_failed"

    async def test_fail_open_allows_outright_when_the_re_evaluation_errors(self, clock: VirtualClock) -> None:
        # The probe resolves the credit, the acquire fails, and then the
        # fail-open re-evaluation throws, leaving only the blanket allow.
        flow = make_flow(clock, engine=_ProbeThenExplodes(), acquire="error")
        result = await flow.check(on_acquire_failure="fail-open")

        assert result.allowed is True
        assert result.reason == "lease_acquire_failed_fail_open"
        assert result.reservation is None

    async def test_falls_back_when_the_probe_errors(self, clock: VirtualClock) -> None:
        # A probe failure is a resolution miss, not the gate: the plain check
        # has its own degradation, and no lease is acquired.
        flow = make_flow(clock, engine=FlowEngine(probe_error=RuntimeError("wasm exploded")))
        result = await flow.check()

        assert flow.fallback.called is True
        assert result.allowed is True
        assert flow.wire.acquire_calls == []

    async def test_falls_back_when_the_flag_is_not_cached(self, clock: VirtualClock) -> None:
        flow = make_flow(clock, missing_flag=True)
        result = await flow.check()

        assert flow.fallback.called is True
        assert result.reservation is None
        assert flow.engine.calls == []

    async def test_zero_usage_falls_back_without_a_hold(self, clock: VirtualClock) -> None:
        flow = make_flow(clock)
        result = await flow.check(usage=0)

        assert flow.fallback.called is True
        assert result.reservation is None
        assert flow.wire.acquire_calls == []
        assert flow.engine.calls == []

    async def test_falls_back_when_nothing_names_the_event_subtype(self, clock: VirtualClock) -> None:
        # The hold settles into a track event named by the subtype; without one
        # it could be consumed while billing nothing.
        entitlement = RulesengineFeatureEntitlement(
            feature_id="feat",
            feature_key=FLAG_KEY,
            value_type="credit",
            credit_id=CREDIT_ID,
            consumption_rate=10,
        )
        flow = make_flow(clock, engine=FlowEngine(probe=_verdict(True, "probe", entitlement)))
        result = await flow.check(event_subtype=None)

        assert flow.fallback.called is True
        assert result.reservation is None
        assert flow.wire.acquire_calls == []

    async def test_rejects_a_nan_usage_without_touching_the_lease(self, clock: VirtualClock) -> None:
        # An unguarded NaN debit poisons the shared lease balance into
        # approving every later reserve, since NaN loses every comparison.
        flow = make_flow(clock)
        denied = await flow.check(usage=float("nan"))

        assert denied.allowed is False
        assert denied.error == "invalid_usage"
        assert denied.reservation is None
        assert flow.wire.acquire_calls == []
        assert flow.engine.calls == []

        allowed = await flow.check()
        assert allowed.allowed is True
        assert allowed.reservation is not None
        assert allowed.reservation.credits_reserved == 500

    async def test_resolves_an_invalid_usage_through_fail_open(self, clock: VirtualClock) -> None:
        flow = make_flow(clock)
        result = await flow.check(usage=-10, on_acquire_failure="fail-open")

        assert result.allowed is True
        assert result.error == "invalid_usage"
        assert result.reservation is None
        assert flow.wire.acquire_calls == []

    async def test_extends_once_and_retries_when_the_lease_is_short(self, clock: VirtualClock) -> None:
        flow = make_flow(clock)
        await flow.check()  # draws the lease down to 500
        flow.wire.extend_responses.append(
            {"lease": {"granted_total": 2000, "expires_at": clock() + LEASE_DURATION}}
        )
        result = await flow.check(usage=90)  # 900 credits, more than the 500 left

        assert result.allowed is True
        assert result.reservation is not None
        assert len(flow.wire.extend_calls) == 1
        assert await flow.remaining() == 600

    async def test_denies_when_the_retry_after_a_failed_extend_is_still_short(self, clock: VirtualClock) -> None:
        flow = make_flow(clock)
        await flow.check()
        flow.wire.extend_responses.append({"error": "wire down"})
        result = await flow.check(usage=90)

        assert result.allowed is False
        assert result.reason == "insufficient_lease_balance"
        assert result.error == "insufficient_lease_balance"
        assert await flow.remaining() == 500
        assert await flow.reservations.count() == 1


class TestEntityResolution:
    async def test_threads_a_resolved_user_into_both_evaluations(self, clock: VirtualClock) -> None:
        user = RulesengineUser(
            id="user_1", account_id="acc_1", environment_id="env_1", keys={"id": "user_1"}, traits=[], rules=[]
        )
        flow = make_flow(clock, user=user)
        result = await check_with_lease(
            flow.deps,
            FLAG_KEY,
            COMPANY,
            {"id": "user_1"},
            CheckOptions(usage=50, event_subtype=EVENT_SUBTYPE),
            flow.fallback,
        )
        await flow.manager._drain_background()

        assert result.allowed is True
        # Evaluating without the named user would silently skip user-targeted
        # rules and overrides.
        assert [call["user"] for call in flow.engine.calls] == [user, user]

    async def test_falls_back_when_the_user_cannot_be_resolved(self, clock: VirtualClock) -> None:
        flow = make_flow(clock, user_error=RuntimeError("DataStream client is not connected"))
        result = await check_with_lease(
            flow.deps,
            FLAG_KEY,
            COMPANY,
            {"id": "user_1"},
            CheckOptions(usage=50, event_subtype=EVENT_SUBTYPE),
            flow.fallback,
        )

        assert flow.fallback.called is True
        assert result.reservation is None
        assert flow.wire.acquire_calls == []

    async def test_falls_back_when_the_company_cannot_be_resolved(self, clock: VirtualClock) -> None:
        flow = make_flow(clock, company_error=RuntimeError("DataStream client is not connected"))
        result = await flow.check()

        assert flow.fallback.called is True
        assert result.reservation is None
        assert flow.wire.acquire_calls == []

    async def test_falls_back_without_datastream(self, clock: VirtualClock) -> None:
        flow = make_flow(clock)
        flow.deps.datastream = None
        result = await flow.check()

        assert flow.fallback.called is True
        assert result.reservation is None


class TestStoreFailureContainment:
    async def test_a_dead_store_resolves_fail_closed_rather_than_raising(self, clock: VirtualClock) -> None:
        flow = make_flow(clock, lease_store=UnreachableLeaseStore(clock=clock))
        result = await flow.check()

        assert result.allowed is False
        assert result.reason == "lease_store_error"
        assert result.error == "lease_store_error"
        assert result.reservation is None

    async def test_a_dead_store_honors_fail_open(self, clock: VirtualClock) -> None:
        flow = make_flow(clock, lease_store=UnreachableLeaseStore(clock=clock))
        result = await flow.check(on_acquire_failure="fail-open")

        assert result.allowed is True
        assert result.reservation is None
        assert flow.engine.balance(1) == FAIL_OPEN_BALANCE


class TestLeaseReplacedMidCheck:
    """The real extend window, on a shared Redis.

    The first reserve comes up short, so the flow awaits the extend, and while
    that call is on the wire the slot's lease is replaced (here by the wire
    stub's side effect; in production by the sweeper or a sibling pod). The
    retried debit charges the successor, so the reservation has to name it.
    """

    async def test_pins_the_reservation_to_the_lease_the_retried_debit_charged(
        self, frozen_clock: VirtualClock
    ) -> None:
        client = make_fake_redis()
        leases = RedisLeaseStore(client, clock=frozen_clock)
        reservations = RedisReservationStore(client, leases, clock=frozen_clock)
        flow = make_flow(frozen_clock, lease_store=leases, reservation_store=reservations)
        await flow.check()  # draws lse_1 down to 500

        async def swap_the_slot() -> None:
            # Expire lse_1 and install lse_2 over it: replace refuses to
            # displace a live lease.
            await leases.drop(COMPANY["id"], CREDIT_ID)
            await leases.replace(
                lease_id="lse_2",
                company_id=COMPANY["id"],
                credit_type_id=CREDIT_ID,
                granted_amount=2000,
                expires_at=frozen_clock() + LEASE_DURATION,
            )

        flow.wire.during_extend = swap_the_slot
        flow.wire.extend_responses.append(
            {"lease": {"granted_total": 2500, "expires_at": frozen_clock() + LEASE_DURATION}}
        )
        result = await flow.check(usage=90)  # 900 credits, more than lse_1's 500

        # The extend went out against the acquired lease, and the store drops
        # its grant because the slot has moved on...
        assert flow.wire.extend_calls[0]["lease_id"] == "lse_1"
        assert result.allowed is True
        assert result.reservation is not None
        # ...but the debit landed on the successor that replaced it in flight.
        assert result.reservation.lease_id == "lse_2"
        entry = await flow.leases.get(COMPANY["id"], CREDIT_ID)
        assert entry is not None and entry.lease_id == "lse_2"
        assert await flow.remaining() == 1100

        # And the settle refund lands, because it is pinned to lse_2.
        outcome = await consume_reservation_and_build_event(flow.reservations, result.reservation, 50)
        assert outcome.settled_locally is True
        assert outcome.track.lease_id == "lse_2"
        assert await flow.remaining() == 1500


class TestCrashWindow:
    async def test_the_debit_lands_before_the_record(self, clock: VirtualClock) -> None:
        """A crash in the gap leaks the debit; it never leaves a record with no
        debit, which a later consume would refund into a double spend."""
        flow = make_flow(clock)
        seen: Dict[str, Any] = {}

        async def freeze(reservation: ReservationRecord) -> None:
            # Freeze the flow where a process death would: reached, never done,
            # so neither the persist nor the undo runs.
            seen["record"] = reservation
            seen["remaining"] = await flow.leases.get(COMPANY["id"], CREDIT_ID)
            seen["reserved"] = await flow.reservations.reserved_credits(COMPANY["id"], CREDIT_ID)
            raise asyncio.CancelledError()

        flow.reservations.add = freeze  # type: ignore[method-assign]
        with pytest.raises(asyncio.CancelledError):
            await flow.check()

        assert seen["record"].credits_reserved == 500
        assert seen["remaining"].local_remaining_credits == 500
        # Nothing the sweeper could refund: the leak is bounded by this one
        # hold and reclaimed when the lease expires server-side.
        assert seen["reserved"] == 0
        assert await flow.reservations.count() == 0
        assert flow.fallback.called is False


class TestSettle:
    async def _reservation(self, flow: Flow) -> Reservation:
        result = await flow.check()
        assert result.reservation is not None
        return result.reservation

    async def test_underuse_refunds_the_unspent_slice(self, clock: VirtualClock) -> None:
        flow = make_flow(clock)
        reservation = await self._reservation(flow)
        outcome = await consume_reservation_and_build_event(flow.reservations, reservation, 20)

        assert outcome.settled_locally is True
        assert outcome.track.event == EVENT_SUBTYPE
        assert outcome.track.quantity == 20
        assert outcome.track.lease_id == "lse_1"
        assert outcome.track.reservation_id is None
        assert outcome.track.company == COMPANY
        assert await flow.remaining() == 800

    async def test_overuse_bills_the_actual_but_clamps_the_local_debit(self, clock: VirtualClock) -> None:
        flow = make_flow(clock)
        reservation = await self._reservation(flow)
        outcome = await consume_reservation_and_build_event(flow.reservations, reservation, 120)

        # The server is the source of truth for real consumption, so the event
        # bills the unclamped quantity; only the lease's own view is clamped.
        assert outcome.track.quantity == 120
        assert await flow.remaining() == 500

    async def test_a_settle_after_the_sweep_is_a_recovery_emit(self, clock: VirtualClock) -> None:
        flow = make_flow(clock)
        reservation = await self._reservation(flow)
        clock.advance_ms(60_001)
        assert await flow.reservations.sweep_expired() == 1
        assert await flow.remaining() == LEASE_SIZE

        outcome = await consume_reservation_and_build_event(flow.reservations, reservation, 20)

        # The hold was already refunded, so nothing re-debits the consumed
        # slice and the local balance reads high until the lease rolls over.
        assert outcome.settled_locally is False
        assert outcome.track.quantity == 20
        assert outcome.track.lease_id == "lse_1"
        assert await flow.remaining() == LEASE_SIZE

    async def test_a_second_settle_finds_nothing_to_claim(self, clock: VirtualClock) -> None:
        flow = make_flow(clock)
        reservation = await self._reservation(flow)
        await consume_reservation_and_build_event(flow.reservations, reservation, 20)
        outcome = await consume_reservation_and_build_event(flow.reservations, reservation, 20)

        assert outcome.settled_locally is False
        assert await flow.remaining() == 800

    async def test_a_fractional_settle_bills_a_whole_unit(self, clock: VirtualClock) -> None:
        flow = make_flow(clock)
        reservation = await self._reservation(flow)
        outcome = await consume_reservation_and_build_event(flow.reservations, reservation, 0.5)

        assert outcome.track.quantity == 1


class TestFlagCheckEvents:
    async def test_an_allowed_check_reports_the_engine_verdict(self, clock: VirtualClock) -> None:
        flow = make_flow(clock)
        result = await flow.check()

        assert len(flow.flag_checks.events) == 1
        event = flow.flag_checks.events[0]
        assert event.flag_key == FLAG_KEY
        assert event.value is True
        assert event.reason == result.reason
        assert event.flag_id == "flag_1"
        assert event.company_id == COMPANY["id"]
        assert event.req_company == COMPANY
        assert event.error is None

    async def test_a_denied_check_reports_the_denial(self, clock: VirtualClock) -> None:
        flow = make_flow(clock, engine=FlowEngine(gate=_verdict(False, "denied_by_targeting")))
        await flow.check()

        assert len(flow.flag_checks.events) == 1
        assert flow.flag_checks.events[0].value is False
        assert flow.flag_checks.events[0].reason == "denied_by_targeting"

    async def test_a_lease_failure_reports_once(self, clock: VirtualClock) -> None:
        flow = make_flow(clock, acquire="error")
        await flow.check(on_acquire_failure="fail-closed")

        assert len(flow.flag_checks.events) == 1
        assert flow.flag_checks.events[0].value is False
        assert flow.flag_checks.events[0].error == "lease_acquire_failed"

    async def test_a_fallback_exit_reports_nothing(self, clock: VirtualClock) -> None:
        # The plain check the lease path defers to reports its own.
        flow = make_flow(clock)
        await flow.check(usage=0)

        assert flow.fallback.called is True
        assert flow.flag_checks.events == []

    async def test_a_reporting_failure_leaves_the_verdict_alone(self, clock: VirtualClock) -> None:
        flow = make_flow(clock)
        flow.flag_checks.explode = True
        result = await flow.check()

        assert result.allowed is True
        assert result.reservation is not None
        assert await flow.remaining() == 500


class TestPerCheckTimeout:
    async def test_the_timeout_reaches_the_acquire(self, clock: VirtualClock) -> None:
        flow = make_flow(clock)
        await flow.check(timeout=2.5)

        assert flow.wire.acquire_calls[0]["timeout"] == 2.5

    async def test_the_timeout_reaches_the_extend_the_reserve_triggers(self, clock: VirtualClock) -> None:
        flow = make_flow(clock)
        await flow.check()  # draws the lease down to 500
        flow.wire.extend_responses.append(
            {"lease": {"granted_total": 2000, "expires_at": clock() + LEASE_DURATION}}
        )
        await flow.check(usage=90, timeout=2.5)  # 900 credits, more than the 500 left

        assert flow.wire.extend_calls[0]["timeout"] == 2.5

    async def test_no_timeout_leaves_the_wire_calls_alone(self, clock: VirtualClock) -> None:
        flow = make_flow(clock)
        await flow.check()

        assert flow.wire.acquire_calls[0]["timeout"] is None
