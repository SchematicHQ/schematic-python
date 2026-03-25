from __future__ import annotations

import pytest

from schematic.datastream.rules_engine import RulesEngineClient
from schematic.types import RulesengineCheckFlagResult, RulesengineFlag, RulesengineRule

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

    async def test_returns_default_for_empty_rules(self, engine: RulesEngineClient) -> None:
        flag = _make_flag(id="flag3", key="empty-rules", default_value=False)
        result = engine.check_flag(flag)
        assert result.value is False


class TestRulesEngineFileNotFound:
    async def test_missing_wasm_raises(self) -> None:
        engine = RulesEngineClient(wasm_path="/nonexistent/rulesengine.wasm")
        with pytest.raises(FileNotFoundError):
            await engine.initialize()
