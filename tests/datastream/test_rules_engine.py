from __future__ import annotations

import pytest

from schematic.datastream.rules_engine import RulesEngineClient
from schematic.types import (
    RulesengineCheckFlagResult,
    RulesengineCompany,
    RulesengineFlag,
    RulesengineRule,
)

# Skip all tests if wasmtime is not installed
wasmtime = pytest.importorskip("wasmtime", reason="wasmtime not installed")


def _make_flag(**overrides: object) -> RulesengineFlag:
    """Build a minimal valid flag for the WASM rules engine."""
    defaults = dict(
        id="flag1",
        key="test-flag",
        account_id="acc_1",
        environment_id="env_1",
        default_value=False,
        rules=[],
    )
    defaults.update(overrides)
    return RulesengineFlag(**defaults)  # type: ignore[arg-type]



class TestRulesEngineClientInit:
    async def test_initialize_loads_wasm(self) -> None:
        engine = RulesEngineClient()
        assert not engine.is_initialized()
        await engine.initialize()
        assert engine.is_initialized()

    async def test_initialize_is_idempotent(self) -> None:
        engine = RulesEngineClient()
        await engine.initialize()
        await engine.initialize()  # Should not raise
        assert engine.is_initialized()

    async def test_get_version_key(self) -> None:
        engine = RulesEngineClient()
        await engine.initialize()
        version = engine.get_version_key()
        assert isinstance(version, str)
        assert len(version) == 8  # 8-char hex string

    def test_check_flag_before_init_raises(self) -> None:
        engine = RulesEngineClient()
        with pytest.raises(RuntimeError, match="not initialized"):
            engine.check_flag(_make_flag())


class TestRulesEngineCheckFlag:
    @pytest.fixture
    async def engine(self) -> RulesEngineClient:
        e = RulesEngineClient()
        await e.initialize()
        return e

    async def test_evaluates_flag_with_default_value(self, engine: RulesEngineClient) -> None:
        flag = _make_flag(default_value=True)
        result = engine.check_flag(flag)
        assert isinstance(result, RulesengineCheckFlagResult)
        assert result.value is True
        assert result.flag_key == "test-flag"
        assert result.reason != ""

    async def test_evaluates_flag_with_company_context(self, engine: RulesEngineClient) -> None:
        from schematic.types import RulesengineCompany

        flag = _make_flag(
            default_value=False,
            rules=[
                RulesengineRule(
                    id="rule1",
                    account_id="acc_1",
                    environment_id="env_1",
                    name="Global Override",
                    rule_type="global_override",
                    value=True,
                    priority=1,
                    conditions=[],
                    condition_groups=[],
                )
            ],
        )
        company = RulesengineCompany(
            id="co_123",
            account_id="acc_1",
            environment_id="env_1",
            keys={"id": "co_123"},
            traits=[],
            metrics=[],
            rules=[],
            entitlements=[],
            billing_product_ids=[],
            credit_balances={},
            plan_ids=[],
            plan_version_ids=[],
        )
        result = engine.check_flag(flag, company)
        assert isinstance(result, RulesengineCheckFlagResult)
        assert result.value is True
        assert result.flag_key == "test-flag"
        assert result.rule_id == "rule1"
        assert result.rule_type is not None
        assert result.reason != ""

    async def test_evaluates_flag_with_user_context(self, engine: RulesEngineClient) -> None:
        from schematic.types import RulesengineUser

        flag = _make_flag(id="flag2", key="user-flag", default_value=True)
        user = RulesengineUser(
            id="usr_456",
            account_id="acc_1",
            environment_id="env_1",
            keys={"id": "usr_456"},
            traits=[],
            rules=[],
        )
        result = engine.check_flag(flag, None, user)
        assert isinstance(result, RulesengineCheckFlagResult)
        assert result.value is True
        assert result.flag_key == "user-flag"

    async def test_returns_default_for_empty_rules(self, engine: RulesEngineClient) -> None:
        flag = _make_flag(id="flag3", key="empty-rules", default_value=False)
        result = engine.check_flag(flag)
        assert result.value is False
        assert result.flag_key == "empty-rules"


class TestRulesEngineClockRegression:
    """Regression for SCHY-471.

    A company-override entitlement rule whose metric condition uses a
    calendar/billing metric period drives the engine into the
    metric-period-reset code path, which calls ``Utc::now()``. On the raw
    ``wasm32-unknown-unknown`` build that has no clock, so the wasm used to trap
    (``wasm unreachable``); the SDK surfaced it as ``WASM check_flag failed`` and
    the caller wrongly saw the flag's ``default_value`` (false) for a company
    that is legitimately entitled. The host now injects the current time via
    ``setCurrentTimeMillis`` so this path evaluates cleanly.
    """

    def _entitled_company(self) -> RulesengineCompany:
        from schematic.types import (
            RulesengineCompanyMetric,
            RulesengineCondition,
            RulesengineRule,
        )

        company_id = "co_entitled"
        company_condition = RulesengineCondition(
            id="cond_company",
            account_id="acc_1",
            environment_id="env_1",
            condition_type="company",
            operator="eq",
            resource_ids=[company_id],
            trait_value="",
        )
        # Usage 40 < allocation 100 -> override grants the feature.
        metric_condition = RulesengineCondition(
            id="cond_metric",
            account_id="acc_1",
            environment_id="env_1",
            condition_type="metric",
            operator="lt",
            resource_ids=[],
            event_subtype="api-calls",
            metric_value=100,
            metric_period="current_month",
            metric_period_month_reset="billing_cycle",
            trait_value="100",
        )
        override_rule = RulesengineRule(
            id="rule_override",
            flag_id="flag1",
            account_id="acc_1",
            environment_id="env_1",
            name="Company Override",
            rule_type="company_override",
            value=True,
            priority=0,
            conditions=[company_condition, metric_condition],
            condition_groups=[],
        )
        metric = RulesengineCompanyMetric(
            account_id="acc_1",
            environment_id="env_1",
            company_id=company_id,
            event_subtype="api-calls",
            period="current_month",
            month_reset="billing_cycle",
            value=40,
            created_at="2023-01-01T00:00:00Z",
        )
        return RulesengineCompany(
            id=company_id,
            account_id="acc_1",
            environment_id="env_1",
            keys={"id": company_id},
            traits=[],
            metrics=[metric],
            rules=[override_rule],
            entitlements=[],
            billing_product_ids=[],
            credit_balances={},
            plan_ids=[],
            plan_version_ids=[],
        )

    async def test_billing_metric_override_evaluates_without_trapping(self) -> None:
        engine = RulesEngineClient()
        await engine.initialize()

        flag = _make_flag(id="flag1", key="mcp-access", default_value=False)
        # Must not raise (the bug surfaced as RuntimeError "WASM flag check failed").
        result = engine.check_flag(flag, self._entitled_company())

        # The override grants the feature; a fallback to default_value would be False.
        assert result.value is True
        assert result.reason and "override" in result.reason.lower()

    async def test_billing_metric_override_populates_reset_at(self) -> None:
        engine = RulesEngineClient()
        await engine.initialize()

        flag = _make_flag(id="flag1", key="mcp-access", default_value=False)
        result = engine.check_flag(flag, self._entitled_company())

        # setCurrentTimeMillis lets the engine compute the next reset boundary.
        assert result.feature_usage_reset_at is not None


class TestRulesEngineFileNotFound:
    async def test_missing_wasm_raises(self) -> None:
        engine = RulesEngineClient(wasm_path="/nonexistent/rulesengine.wasm")
        with pytest.raises(FileNotFoundError):
            await engine.initialize()


class TestRulesEngineEnvelopeNulls:
    """Regression for schematichq 1.3.4 / rules engine WASM v0.7.0.

    The generated models keep explicitly-set ``None`` values when dumped with
    ``exclude_none=True``, and ``partial_company`` sets every unset optional
    entitlement field to ``None`` when it merges a partial update. The WASM
    treats an absent key and an explicit ``null`` differently, and rejected
    ``"warning_tiers": null`` with an error code, so every check against a
    company failed from its first partial update onward. The envelope must
    never carry nulls, whatever shape the models are in.
    """

    @pytest.fixture
    async def engine(self) -> RulesEngineClient:
        e = RulesEngineClient()
        await e.initialize()
        return e

    def _merged_company(self) -> RulesengineCompany:
        from schematic.datastream.datastream_client import _validate
        from schematic.datastream.merge import partial_company

        raw = {
            "id": "co_1",
            "account_id": "acc_1",
            "environment_id": "env_1",
            "keys": {"id": "c1"},
            "traits": [],
            "metrics": [],
            "rules": [],
            "plan_ids": ["plan_1"],
            "plan_version_ids": [],
            "billing_product_ids": [],
            "credit_balances": {},
            "entitlements": [
                {"feature_id": "feat_1", "feature_key": "test-flag", "value_type": "boolean"},
            ],
        }
        full = _validate(RulesengineCompany, raw)
        return partial_company(full, {"credit_balances": {"crd_1": 5.0}})

    def test_merged_company_dump_carries_explicit_nulls(self) -> None:
        # Documents the model behaviour the envelope has to defend against. If
        # this ever starts failing, the stripping below is no longer load-bearing.
        dumped = self._merged_company().model_dump(exclude_none=True, mode="json")
        assert "warning_tiers" in dumped["entitlements"][0]
        assert dumped["entitlements"][0]["warning_tiers"] is None

    async def test_envelope_contains_no_nulls(self, engine: RulesEngineClient) -> None:
        import json

        captured: list[str] = []
        original = engine._call_wasm

        def spy(input_json: str) -> str:
            captured.append(input_json)
            return original(input_json)

        engine._call_wasm = spy  # type: ignore[method-assign]
        engine.check_flag(_make_flag(default_value=True), self._merged_company())

        assert len(captured) == 1
        envelope = json.loads(captured[0])
        assert envelope["user"] is None  # top-level absence is still expressed as null

        def has_null(obj: object) -> bool:
            if isinstance(obj, dict):
                return any(v is None or has_null(v) for v in obj.values())
            if isinstance(obj, list):
                return any(item is None or has_null(item) for item in obj)
            return False

        assert not has_null(envelope["flag"])
        assert not has_null(envelope["company"])
        assert "warning_tiers" not in envelope["company"]["entitlements"][0]

    async def test_check_flag_after_partial_merge_evaluates(self, engine: RulesEngineClient) -> None:
        result = engine.check_flag(_make_flag(default_value=True), self._merged_company())
        assert isinstance(result, RulesengineCheckFlagResult)
        assert result.value is True
        assert result.err is None
