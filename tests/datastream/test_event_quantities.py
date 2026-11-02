"""The event_quantities preflight and the quantity_rates it prices from, run
through the WASM engine.

Flags and companies are built from the snake_case payloads DataStream sends,
through the same validation the client uses, so a quantity_rates the generated
models would drop fails here.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

import pytest

from schematic.client import CheckFlagOptions, EventQuantities, EventUsage
from schematic.datastream.datastream_client import _validate
from schematic.datastream.rules_engine import RulesEngineClient
from schematic.types import RulesengineCompany, RulesengineFlag

wasmtime = pytest.importorskip("wasmtime", reason="wasmtime not installed")

SUBTYPE = "chat"
CREDIT_ID = "credit-abc"
RATES = {"input_tokens": 0.001, "output_tokens": 0.01}
# 1 request x 0.5 + (1000 - 400 cached) x 0.001 + 100 x 0.01 = 2.1. The cached
# tokens are unrated, so they cost nothing but still come out of input.
QUANTITIES = {"input_tokens": 1000.0, "cached_input_tokens": 400.0, "output_tokens": 100.0}
CALL = CheckFlagOptions(event_quantities=EventQuantities(event_subtype=SUBTYPE, quantities=QUANTITIES))


def _inference_flag(consumption_rate: float, quantity_rates: Optional[Dict[str, float]] = None) -> RulesengineFlag:
    """A single credit-balance rule priced like an inference entitlement:
    requests at consumption_rate, tokens at their own rates."""
    condition: Dict[str, Any] = {
        "id": "cond-1",
        "account_id": "acct",
        "environment_id": "env",
        "condition_type": "credit",
        "operator": "lt",
        "resource_ids": [],
        "trait_value": "",
        "metric_value": 0,
        "credit_id": CREDIT_ID,
        "consumption_rate": consumption_rate,
        "event_subtype": SUBTYPE,
    }
    if quantity_rates is not None:
        condition["quantity_rates"] = quantity_rates
    return _validate(
        RulesengineFlag,
        {
            "id": "flag-1",
            "account_id": "acct",
            "environment_id": "env",
            "key": "chat",
            "default_value": False,
            "rules": [
                {
                    "id": "rule-1",
                    "account_id": "acct",
                    "environment_id": "env",
                    "name": "Credits",
                    "rule_type": "plan_entitlement",
                    "priority": 0,
                    "value": True,
                    "conditions": [condition],
                    "condition_groups": [],
                }
            ],
        },
    )


def _company(balance: float, **extra: Any) -> RulesengineCompany:
    return _validate(
        RulesengineCompany,
        {
            "id": "co",
            "account_id": "acct",
            "environment_id": "env",
            "keys": {"id": "co"},
            "billing_product_ids": [],
            "crm_product_ids": [],
            "credit_balances": {CREDIT_ID: balance},
            "plan_ids": [],
            "plan_version_ids": [],
            "metrics": [],
            "traits": [],
            "rules": [],
            **extra,
        },
    )


@pytest.fixture
async def engine() -> RulesEngineClient:
    client = RulesEngineClient()
    await client.initialize()
    return client


def _check(engine: RulesEngineClient, balance: float, options: CheckFlagOptions) -> Any:
    return engine.check_flag(_inference_flag(0.5, RATES), _company(balance), None, options)


class TestEventQuantities:
    async def test_passes_when_the_balance_covers_the_call(self, engine: RulesEngineClient) -> None:
        result = _check(engine, 2.1, CALL)
        assert result.rule_id == "rule-1"
        assert result.value is True

    async def test_refuses_when_the_balance_falls_short(self, engine: RulesEngineClient) -> None:
        # Covers the request and the legacy single unit, not the tokens.
        result = _check(engine, 2.0, CALL)
        assert result.rule_id is None
        assert result.value is False

    async def test_ignored_for_another_subtype(self, engine: RulesEngineClient) -> None:
        other = CheckFlagOptions(
            event_quantities=EventQuantities(event_subtype="other", quantities={"input_tokens": 1e6})
        )
        assert _check(engine, 1.0, other).rule_id == "rule-1"

    async def test_quantity_multiplies_the_base_not_the_quantities(self, engine: RulesEngineClient) -> None:
        # 3 x 0.5 + 600 x 0.001 + 100 x 0.01 = 3.1.
        options = CheckFlagOptions(
            event_quantities=EventQuantities(event_subtype=SUBTYPE, quantity=3, quantities=QUANTITIES)
        )
        assert _check(engine, 3.1, options).rule_id == "rule-1"
        assert _check(engine, 3.0, options).rule_id is None

    async def test_credit_cost_beats_event_quantities(self, engine: RulesEngineClient) -> None:
        options = CheckFlagOptions(event_quantities=CALL.event_quantities, credit_cost={CREDIT_ID: 1.0})
        assert _check(engine, 1.0, options).rule_id == "rule-1"

    async def test_event_quantities_beats_event_usage(self, engine: RulesEngineClient) -> None:
        # event_usage alone would ask 1 x 0.5, which 2.0 covers.
        options = CheckFlagOptions(
            event_quantities=CALL.event_quantities,
            event_usage=EventUsage(event_subtype=SUBTYPE, quantity=1),
        )
        assert _check(engine, 2.0, options).rule_id is None

    async def test_passes_fractional_quantities_through_unrounded(self, engine: RulesEngineClient) -> None:
        # 0.5 + 0.5 x 0.01 = 0.505; rounding the half token up would ask 0.51.
        options = CheckFlagOptions(
            event_quantities=EventQuantities(event_subtype=SUBTYPE, quantities={"output_tokens": 0.5})
        )
        assert _check(engine, 0.505, options).rule_id == "rule-1"

    @pytest.mark.parametrize(
        "event_quantities",
        [
            EventQuantities(event_subtype=SUBTYPE, quantity=-1),
            EventQuantities(event_subtype=SUBTYPE, quantities={"input_tokens": -1}),
        ],
        ids=["quantity", "quantities"],
    )
    async def test_rejects_negative_values(self, engine: RulesEngineClient, event_quantities: EventQuantities) -> None:
        result = _check(engine, 100, CheckFlagOptions(event_quantities=event_quantities))
        assert result.value is False
        assert result.err

    async def test_a_company_entitlements_quantity_rates_reach_the_result(self, engine: RulesEngineClient) -> None:
        flag = _inference_flag(0.5)
        company = _company(
            0,
            entitlements=[
                {"feature_id": "feat-1", "feature_key": flag.key, "value_type": "credit", "quantity_rates": RATES}
            ],
        )

        result = engine.check_flag(flag, company)

        assert result.entitlement is not None
        assert result.entitlement.quantity_rates == RATES  # type: ignore[attr-defined]


# testdata/quantity_cost.json is copied verbatim from schematic-api's
# api/lib/rulesengine/testdata/quantity_cost.json. The API's burn and the engine
# both price every case there; running them through the WASM engine here pins
# that this SDK's wire shape for quantity_rates and event_quantities reaches
# that pricing intact.
_FIXTURE = json.loads((Path(__file__).parent / "testdata" / "quantity_cost.json").read_text())
# The preflight rejects negative quantities before pricing.
_CASES = [
    c
    for c in _FIXTURE["cases"]
    if c.get("quantity", 0) >= 0 and all(q >= 0 for q in c.get("quantities", {}).values())
]


@pytest.mark.parametrize("case", _CASES, ids=[c["name"] for c in _CASES])
async def test_shared_quantity_cost_fixture(engine: RulesEngineClient, case: Dict[str, Any]) -> None:
    flag = _inference_flag(case["consumption_rate"], case.get("quantity_rates"))
    options = CheckFlagOptions(
        event_quantities=EventQuantities(
            event_subtype=SUBTYPE, quantity=case.get("quantity"), quantities=case.get("quantities")
        )
    )
    cost = case["expected_cost"]

    # A cost priced to zero gates on balance > 0, so the smallest positive
    # balance passes and zero does not.
    covers = cost * (1 + 1e-9) + 1e-9
    short = 0 if cost == 0 else cost * (1 - 1e-6)

    assert engine.check_flag(flag, _company(covers), None, options).rule_id == "rule-1"
    assert engine.check_flag(flag, _company(short), None, options).rule_id is None
