"""The windows between the two steps of a transition, on both backends.

A crash in one must strand locally held credits (which the server reclaims at
lease expiry) rather than enable a double-spend. The debit and the claim are
durable first; the record and the refund are what may be lost.

The last window here is not a crash: the slot's lease can be replaced between
the acquire and the debit, and the reservation has to pin the lease the debit
actually charged, or its refunds are dropped.
"""

from __future__ import annotations

import logging
from typing import Any, Awaitable, Optional, Tuple, cast

import pytest
from lease_support import (
    CrashingRefundLeaseStore,
    ScriptedDataStream,
    ScriptedEngine,
    ScriptedWireClient,
    VirtualClock,
    make_fake_redis,
    make_reservation,
)

from schematic.client import CheckOptions, CheckResult
from schematic.leases import (
    CreditCheckDeps,
    InMemoryLeaseStore,
    InMemoryReservationStore,
    LeaseConfig,
    LeaseManager,
    LeaseState,
    LeaseStore,
    RedisLeaseStore,
    RedisReservationStore,
    ReservationStore,
    ReserveResult,
    check_with_lease,
    consume_reservation_and_build_event,
)

BACKENDS = ("in_memory", "redis")


@pytest.fixture(autouse=True)
def _frozen(frozen_clock: VirtualClock) -> VirtualClock:
    """fakeredis reads TIME from the process clock, so the virtual clock is it."""
    return frozen_clock


def _make_stores(
    backend: str, clock: VirtualClock
) -> Tuple[LeaseStore, ReservationStore, CrashingRefundLeaseStore]:
    leases: LeaseStore
    reservations: ReservationStore
    if backend == "in_memory":
        leases = InMemoryLeaseStore(clock=clock)
        crash = CrashingRefundLeaseStore(leases)
        reservations = InMemoryReservationStore(crash, clock=clock)
    else:
        client = make_fake_redis()
        leases = RedisLeaseStore(client, clock=clock)
        crash = CrashingRefundLeaseStore(leases)
        reservations = RedisReservationStore(client, crash, clock=clock)
    return leases, reservations, crash


async def _seed(leases: LeaseStore, clock: VirtualClock, ttl: float = 60) -> None:
    await leases.replace(
        lease_id="lse_1",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=1000,
        expires_at=clock() + ttl,
    )


async def _balance(leases: LeaseStore) -> float:
    entry = await leases.get("co_1", "ct_1")
    assert entry is not None
    return entry.local_remaining_credits


@pytest.mark.parametrize("backend", BACKENDS)
async def test_debit_without_record_leaks_only_the_hold(backend: str, frozen_clock: VirtualClock) -> None:
    leases, reservations, _crash = _make_stores(backend, frozen_clock)
    await _seed(leases, frozen_clock)

    # The crash: the atomic debit landed, the reservation record never did.
    assert await leases.try_reserve("co_1", "ct_1", 100) == ReserveResult(balance=900, lease_id="lse_1")

    # Exactly the reserved amount is stranded, and it is invisible to the
    # reservation table, so no sweep can ever refund it.
    assert await _balance(leases) == 900
    assert await reservations.reserved_credits("co_1", "ct_1") == 0
    assert await reservations.sweep_expired(frozen_clock() + 3600) == 0
    assert await _balance(leases) == 900


@pytest.mark.parametrize("backend", BACKENDS)
async def test_debit_leak_is_reclaimed_at_lease_expiry(backend: str, frozen_clock: VirtualClock) -> None:
    leases, _reservations, _crash = _make_stores(backend, frozen_clock)
    await _seed(leases, frozen_clock)
    assert await leases.try_reserve("co_1", "ct_1", 100) == ReserveResult(balance=900, lease_id="lse_1")

    frozen_clock.advance_ms(60_001)
    # The stale balance is never served again, and the successor installs at
    # the full grant: the leak does not outlive the lease.
    assert await leases.try_reserve("co_1", "ct_1", 1) is None
    assert await leases.replace(
        lease_id="lse_2",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=1000,
        expires_at=frozen_clock() + 120,
    )
    assert await _balance(leases) == 1000


@pytest.mark.parametrize("backend", BACKENDS)
async def test_a_retried_check_settles_independently(backend: str, frozen_clock: VirtualClock) -> None:
    leases, reservations, _crash = _make_stores(backend, frozen_clock)
    await _seed(leases, frozen_clock, ttl=3600)
    # The crashed attempt, then the retry with a fresh reservation.
    assert await leases.try_reserve("co_1", "ct_1", 100) == ReserveResult(balance=900, lease_id="lse_1")
    assert await leases.try_reserve("co_1", "ct_1", 100) == ReserveResult(balance=800, lease_id="lse_1")
    await reservations.add(make_reservation(id="res_retry", expires_at=frozen_clock() + 60))

    assert await reservations.consume("res_retry", 40) == 40
    # 1000 less the 100 leaked and the 40 consumed: the retry's unspent 60 came
    # back exactly once, the leaked 100 stayed leaked.
    assert await _balance(leases) == 860

    assert await reservations.consume("res_retry", 40) is None
    assert await reservations.sweep_expired(frozen_clock() + 3600) == 0
    assert await _balance(leases) == 860


@pytest.mark.parametrize("backend", BACKENDS)
async def test_crash_before_refund_keeps_the_claim(backend: str, frozen_clock: VirtualClock) -> None:
    leases, reservations, crash = _make_stores(backend, frozen_clock)
    await _seed(leases, frozen_clock)
    assert await leases.try_reserve("co_1", "ct_1", 100) == ReserveResult(balance=900, lease_id="lse_1")
    await reservations.add(make_reservation(expires_at=frozen_clock() + 60))

    crash.arm()
    with pytest.raises(RuntimeError, match="simulated crash before refund"):
        await reservations.consume("res_1", 30)

    # The claim survived, so the reservation is gone everywhere and nothing can
    # double-spend; the 70-credit refund is lost, bounded by the hold.
    assert await reservations.get("res_1") is None
    assert await reservations.reserved_credits("co_1", "ct_1") == 0
    assert await _balance(leases) == 900

    # Neither a retried settle nor the sweeper can refund a claimed hold.
    assert await reservations.consume("res_1", 30) is None
    assert await reservations.sweep_expired(frozen_clock() + 3600) == 0
    assert await _balance(leases) == 900


@pytest.mark.parametrize("backend", BACKENDS)
async def test_crash_before_refund_never_leaks_into_a_successor(
    backend: str, frozen_clock: VirtualClock
) -> None:
    leases, reservations, crash = _make_stores(backend, frozen_clock)
    await _seed(leases, frozen_clock)
    assert await leases.try_reserve("co_1", "ct_1", 100) == ReserveResult(balance=900, lease_id="lse_1")
    await reservations.add(make_reservation(expires_at=frozen_clock() + 60))

    crash.arm()
    with pytest.raises(RuntimeError, match="simulated crash before refund"):
        await reservations.consume("res_1", 30)

    frozen_clock.advance_ms(60_001)
    assert await leases.try_reserve("co_1", "ct_1", 1) is None
    assert await leases.replace(
        lease_id="lse_2",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=1000,
        expires_at=frozen_clock() + 120,
    )
    # A very late retried settle must not push the lost refund into lse_2.
    assert await reservations.consume("res_1", 0) is None
    assert await _balance(leases) == 1000


async def test_crash_after_the_claim_is_reconciled_without_a_refund(frozen_clock: VirtualClock) -> None:
    # Redis only: a process death after the claim but before the index cleanup
    # leaves the per-tenant index over-counting. The sweeper reconciles it, and
    # deliberately does not refund: without the reservation hash, exactly-once
    # cannot be arbitrated across racing sweepers.
    client = make_fake_redis()
    leases = RedisLeaseStore(client, clock=frozen_clock)
    reservations = RedisReservationStore(client, leases, clock=frozen_clock)
    await _seed(leases, frozen_clock)
    assert await leases.try_reserve("co_1", "ct_1", 100) == ReserveResult(balance=900, lease_id="lse_1")
    await reservations.add(make_reservation(expires_at=frozen_clock() - 0.001))

    original_evalsha = client.evalsha
    armed = True

    async def crash_after_claim(sha: str, numkeys: int, *args: Any) -> Any:
        nonlocal armed
        result = await cast(Awaitable[Any], original_evalsha(sha, numkeys, *args))
        if armed and isinstance(result, list):
            armed = False
            raise RuntimeError("simulated crash after claim")
        return result

    client.evalsha = crash_after_claim  # type: ignore[method-assign]

    with pytest.raises(RuntimeError, match="simulated crash after claim"):
        await reservations.consume("res_1", 30)
    client.evalsha = original_evalsha  # type: ignore[method-assign]

    # The orphaned index field still counts the hold...
    assert await reservations.reserved_credits("co_1", "ct_1") == 100
    # ...until the sweeper reconciles it, without refunding.
    assert await reservations.sweep_expired() == 0
    assert await reservations.reserved_credits("co_1", "ct_1") == 0
    assert await reservations.count() == 0
    assert await _balance(leases) == 900


class _SwapLeaseOnReserve(LeaseStore):
    """Wrapper that replaces the slot's lease with a successor right before the
    first debit reaches the store.

    The deterministic form of the window between ``acquire_if_needed`` and
    ``try_reserve``: the awaited extend wire call, or a sibling pod's
    ``replace`` on a shared backend. The debit is not keyed by lease id, so it
    lands on the successor.
    """

    def __init__(self, target: LeaseStore, successor_id: str, clock: VirtualClock) -> None:
        self._target = target
        self._successor_id = successor_id
        self._clock = clock
        self._swapped = False

    async def get(self, company_id: str, credit_type_id: str) -> Optional[LeaseState]:
        return await self._target.get(company_id, credit_type_id)

    async def replace(
        self,
        *,
        lease_id: str,
        company_id: str,
        credit_type_id: str,
        granted_amount: float,
        expires_at: float,
    ) -> bool:
        return await self._target.replace(
            lease_id=lease_id,
            company_id=company_id,
            credit_type_id=credit_type_id,
            granted_amount=granted_amount,
            expires_at=expires_at,
        )

    async def try_reserve(self, company_id: str, credit_type_id: str, credits: float) -> Optional[ReserveResult]:
        if not self._swapped:
            self._swapped = True
            # replace refuses to displace a live lease, so the incumbent goes
            # first and the successor installs into an empty slot.
            await self._target.drop(company_id, credit_type_id)
            await self._target.replace(
                lease_id=self._successor_id,
                company_id=company_id,
                credit_type_id=credit_type_id,
                granted_amount=1000,
                expires_at=self._clock() + 60,
            )
        return await self._target.try_reserve(company_id, credit_type_id, credits)

    async def refund(
        self,
        company_id: str,
        credit_type_id: str,
        credits: float,
        pin_lease_id: Optional[str] = None,
    ) -> None:
        await self._target.refund(company_id, credit_type_id, credits, pin_lease_id)

    async def extend(
        self,
        company_id: str,
        credit_type_id: str,
        granted_total: float,
        new_expires_at: Optional[float] = None,
        pin_lease_id: Optional[str] = None,
    ) -> None:
        await self._target.extend(company_id, credit_type_id, granted_total, new_expires_at, pin_lease_id)

    async def drop(self, company_id: str, credit_type_id: str) -> None:
        await self._target.drop(company_id, credit_type_id)


_ENTITLEMENT = {
    "value_type": "credit",
    "credit_id": "ct_1",
    "consumption_rate": 10,
    "event_subtype": "inference_tokens",
}


def _check_deps(
    lease_store: LeaseStore, reservations: ReservationStore, clock: VirtualClock
) -> CreditCheckDeps:
    """The real check flow, wired to whatever lease store is handed in."""

    async def _noop(_body: Any) -> None:
        return None

    engine = ScriptedEngine(
        [
            {"value": True, "reason": "probe", "entitlement": _ENTITLEMENT},
            {"value": True, "reason": "matched", "entitlement": _ENTITLEMENT},
        ],
        "inference",
    )
    manager = LeaseManager(
        # The seeded live lease means acquire_if_needed never hits the wire.
        ScriptedWireClient(),
        lease_store,
        reservation_store=reservations,
        config=LeaseConfig(lease_duration=300.0, reservation_ttl=60.0, lease_size=1000.0, low_water_mark=0.25),
        clock=clock,
    )
    return CreditCheckDeps(
        datastream=ScriptedDataStream(engine, "inference", {"id": "co_1", "credit_balances": {"ct_1": 5000}}),
        lease_store=lease_store,
        reservations=reservations,
        manager=manager,
        logger=logging.getLogger("lease-swap-test"),
        enqueue_flag_check=_noop,
        clock=clock,
    )


async def _unused_fallback() -> CheckResult:
    raise AssertionError("the lease path must not fall back here")


async def _check_over_a_swapped_lease(
    backend: str, clock: VirtualClock
) -> Tuple[LeaseStore, ReservationStore, CheckResult]:
    leases, reservations, _crash = _make_stores(backend, clock)
    await _seed(leases, clock)
    deps = _check_deps(_SwapLeaseOnReserve(leases, "lse_2", clock), reservations, clock)
    result = await check_with_lease(
        deps,
        "inference",
        {"id": "co_1"},
        None,
        CheckOptions(usage=10, event_subtype="inference_tokens"),
        _unused_fallback,
    )
    await deps.manager._drain_background()
    return leases, reservations, result


@pytest.mark.parametrize("backend", BACKENDS)
async def test_the_reservation_pins_the_lease_the_debit_landed_on(
    backend: str, frozen_clock: VirtualClock
) -> None:
    leases, reservations, result = await _check_over_a_swapped_lease(backend, frozen_clock)

    assert result.allowed is True
    assert result.reservation is not None
    # Pinning acquire_if_needed's lse_1 here would name a lease that was never
    # charged.
    assert result.reservation.lease_id == "lse_2"
    entry = await leases.get("co_1", "ct_1")
    assert entry is not None and entry.lease_id == "lse_2"
    assert await _balance(leases) == 900

    # Cancelling refunds the successor: refund's pin drops a refund aimed at
    # any other lease, so a stale pin would leave the balance at 900.
    assert await reservations.consume(result.reservation.id, 0) == 0
    assert await _balance(leases) == 1000


@pytest.mark.parametrize("backend", BACKENDS)
async def test_the_settling_track_event_bills_the_lease_the_debit_landed_on(
    backend: str, frozen_clock: VirtualClock
) -> None:
    leases, reservations, result = await _check_over_a_swapped_lease(backend, frozen_clock)
    assert result.reservation is not None

    outcome = await consume_reservation_and_build_event(reservations, result.reservation, 4)

    assert outcome.settled_locally is True
    # A stale pin would bill lse_2's spend against the released lse_1, and the
    # server would fall through to the grants.
    assert outcome.track.lease_id == "lse_2"
    # 1000 less the 100 reserved, plus the 60 unspent refunded to lse_2.
    assert await _balance(leases) == 960
