"""The credit gate against the real WASM rules engine.

Every other lease test scripts the engine, so the contract that matters most
goes unexercised: resolving the matched credit entitlement from the probe,
substituting the lease balance into the company's credit balances, and letting
the engine's credit_cost gate decide. A drift in the option envelope or in the
entity shape the SDK feeds the engine fails here rather than mis-gating in
production.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import pytest
from lease_support import ScriptedWireClient, VirtualClock

from schematic.client import CheckFlagOptions, CheckOptions, CheckResult, EventUsage
from schematic.datastream.rules_engine import RulesEngineClient
from schematic.leases import (
    CreditCheckDeps,
    InMemoryLeaseStore,
    InMemoryReservationStore,
    LeaseConfig,
    LeaseManager,
    check_with_lease,
)
from schematic.types import (
    RulesengineCompany,
    RulesengineCondition,
    RulesengineFeatureEntitlement,
    RulesengineFlag,
    RulesengineRule,
)

wasmtime = pytest.importorskip("wasmtime", reason="wasmtime not installed")

FLAG_KEY = "infer"
CREDIT_ID = "credit-1"
EVENT_SUBTYPE = "inference_tokens"
COMPANY_ID = "co"
LEASE_SIZE = 10_000.0


def _credit_condition() -> RulesengineCondition:
    # A consumption rate of 1 keeps credits equal to quantity, so the
    # arithmetic in the assertions is the engine's own.
    return RulesengineCondition(
        id="cond-credit",
        account_id="acct",
        environment_id="env",
        condition_type="credit",
        operator="lt",
        resource_ids=[],
        trait_value="",
        metric_value=0,
        credit_id=CREDIT_ID,
        consumption_rate=1,
        event_subtype=EVENT_SUBTYPE,
    )


def _company_condition(resource_ids: List[str]) -> RulesengineCondition:
    """A membership condition to flip, so the engine can deny for a reason that
    has nothing to do with the balance."""
    return RulesengineCondition(
        id="cond-company",
        account_id="acct",
        environment_id="env",
        condition_type="company",
        operator="eq",
        resource_ids=resource_ids,
        trait_value="",
        metric_value=0,
    )


def _credit_flag(extra_conditions: Optional[List[RulesengineCondition]] = None) -> RulesengineFlag:
    return RulesengineFlag(
        id="flag-infer",
        account_id="acct",
        environment_id="env",
        key=FLAG_KEY,
        default_value=False,
        rules=[
            RulesengineRule(
                id="rule-credit",
                account_id="acct",
                environment_id="env",
                name="Credit",
                rule_type="plan_entitlement",
                priority=100,
                value=True,
                conditions=[_credit_condition(), *(extra_conditions or [])],
                condition_groups=[],
            )
        ],
    )


def _company(
    credit_balance: float, entitlements: Optional[List[RulesengineFeatureEntitlement]] = None
) -> RulesengineCompany:
    # The company carries its resolved entitlement for the feature, the shape
    # the DataStream cache holds after a plan assignment. Entitlement-first
    # resolution reads the credit, the rate, and the subtype off it.
    default = RulesengineFeatureEntitlement(
        feature_id="feat-infer",
        feature_key=FLAG_KEY,
        value_type="credit",
        credit_id=CREDIT_ID,
        consumption_rate=1,
        event_subtype=EVENT_SUBTYPE,
        credit_total=credit_balance,
        credit_used=0,
        credit_remaining=credit_balance,
    )
    return RulesengineCompany(
        id=COMPANY_ID,
        account_id="acct",
        environment_id="env",
        keys={"id": COMPANY_ID},
        traits=[],
        metrics=[],
        rules=[],
        entitlements=entitlements if entitlements is not None else [default],
        billing_product_ids=[],
        credit_balances={CREDIT_ID: credit_balance},
        plan_ids=[],
        plan_version_ids=[],
    )


class RealEngineDataStream:
    """Serves a fixed flag and company, and the real rules engine behind them."""

    def __init__(self, engine: RulesEngineClient, flag: RulesengineFlag, company: RulesengineCompany) -> None:
        self._engine = engine
        self._flag = flag
        self._company = company

    async def get_flag(self, flag_key: str) -> RulesengineFlag:
        return self._flag

    async def get_company(self, keys: Dict[str, str]) -> RulesengineCompany:
        return self._company

    async def get_user(self, keys: Dict[str, str]) -> None:
        return None

    def evaluate_flag(self, flag: Any, company: Any, user: Any, options: Any = None) -> Any:
        return self._engine.check_flag(flag, company, user, options)


def _deps(
    engine: RulesEngineClient, flag: RulesengineFlag, company: RulesengineCompany, clock: VirtualClock
) -> CreditCheckDeps:
    leases = InMemoryLeaseStore(clock=clock)
    reservations = InMemoryReservationStore(leases, clock=clock)
    wire = ScriptedWireClient()
    wire.acquire_responses.append(
        {"lease": {"lease_id": "lse-1", "granted_amount": LEASE_SIZE, "expires_at": clock() + 60}}
    )
    manager = LeaseManager(
        wire,
        leases,
        reservation_store=reservations,
        config=LeaseConfig(lease_duration=60.0, reservation_ttl=60.0, lease_size=LEASE_SIZE),
        clock=clock,
    )
    async def enqueue_flag_check(body: Any) -> None:
        """These tests pin the engine's verdict, not the analytics event."""

    return CreditCheckDeps(
        datastream=RealEngineDataStream(engine, flag, company),
        lease_store=leases,
        reservations=reservations,
        manager=manager,
        logger=logging.getLogger("wasm-credit-gate-test"),
        enqueue_flag_check=enqueue_flag_check,
        clock=clock,
    )


async def _fail_fallback() -> CheckResult:
    raise AssertionError("the lease path should not have fallen back")


@pytest.fixture
async def engine() -> RulesEngineClient:
    client = RulesEngineClient()
    await client.initialize()
    return client


class TestCreditGateAgainstTheRealEngine:
    async def test_a_within_balance_usage_passes_and_holds(
        self, engine: RulesEngineClient, clock: VirtualClock
    ) -> None:
        deps = _deps(engine, _credit_flag(), _company(100), clock)
        result = await check_with_lease(
            deps,
            FLAG_KEY,
            {"id": COMPANY_ID},
            None,
            CheckOptions(usage=50, event_subtype=EVENT_SUBTYPE),
            _fail_fallback,
        )
        await deps.manager._drain_background()

        assert result.allowed is True
        assert result.value is True
        assert result.reservation is not None
        assert result.reservation.credit_type_id == CREDIT_ID
        assert result.reservation.credits_reserved == 50
        entry = await deps.lease_store.get(COMPANY_ID, CREDIT_ID)
        assert entry is not None and entry.local_remaining_credits == LEASE_SIZE - 50
        assert await deps.reservations.count() == 1

    async def test_a_non_credit_denial_refunds_the_hold(
        self, engine: RulesEngineClient, clock: VirtualClock
    ) -> None:
        # Credits are plentiful, but the membership condition excludes this
        # company, so the hold taken before the gate has to come back.
        flag = _credit_flag([_company_condition(["some-other-company"])])
        deps = _deps(engine, flag, _company(10_000), clock)
        result = await check_with_lease(
            deps,
            FLAG_KEY,
            {"id": COMPANY_ID},
            None,
            CheckOptions(usage=50, event_subtype=EVENT_SUBTYPE),
            _fail_fallback,
        )

        assert result.allowed is False
        assert result.value is False
        assert result.reservation is None
        entry = await deps.lease_store.get(COMPANY_ID, CREDIT_ID)
        assert entry is not None and entry.local_remaining_credits == LEASE_SIZE
        assert await deps.reservations.count() == 0

    async def test_an_override_granted_company_never_touches_the_lease(
        self, engine: RulesEngineClient, clock: VirtualClock
    ) -> None:
        # A company override grants the feature outright, so the company's
        # effective entitlement is boolean rather than credit-metered: no
        # reserve-then-cancel, and no credits billed for usage the override
        # grants for free.
        flag = _credit_flag()
        override = RulesengineRule(
            id="rule-override",
            account_id="acct",
            environment_id="env",
            name="Override",
            rule_type="company_override",
            priority=1,
            value=True,
            conditions=[_company_condition([COMPANY_ID])],
            condition_groups=[],
        )
        flag = flag.model_copy(update={"rules": [override, *flag.rules]})
        company = _company(
            100,
            [RulesengineFeatureEntitlement(feature_id="feat-infer", feature_key=FLAG_KEY, value_type="boolean")],
        )
        deps = _deps(engine, flag, company, clock)
        fell_back = False

        async def fallback() -> CheckResult:
            nonlocal fell_back
            fell_back = True
            return CheckResult(allowed=True, value=True, reason="override", flag_key=FLAG_KEY)

        result = await check_with_lease(
            deps, FLAG_KEY, {"id": COMPANY_ID}, None, CheckOptions(usage=50, event_subtype=EVENT_SUBTYPE), fallback
        )

        assert fell_back is True
        assert result.allowed is True
        assert result.reservation is None
        assert await deps.lease_store.get(COMPANY_ID, CREDIT_ID) is None
        assert await deps.reservations.count() == 0

    async def test_the_preflight_envelope_gates_at_the_balance_boundary(self, engine: RulesEngineClient) -> None:
        # The contract the lease path leans on: the SDK's event_usage option
        # reaches the engine as the envelope it gates on.
        flag = _credit_flag()
        company = _company(100)

        under = engine.check_flag(
            flag, company, None, CheckFlagOptions(event_usage=EventUsage(event_subtype=EVENT_SUBTYPE, quantity=50))
        )
        over = engine.check_flag(
            flag, company, None, CheckFlagOptions(event_usage=EventUsage(event_subtype=EVENT_SUBTYPE, quantity=150))
        )

        assert under.value is True
        assert over.value is False
