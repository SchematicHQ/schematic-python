"""Flag checks in replicator mode while the replicator reports not ready.

When a Schematic account is closed or Schematic is unreachable, the replicator
stays up and keeps its cache but reports ``ready: false``. Flag checks should
keep evaluating from that cache, as the Go SDK does, rather than falling back
to the API (which cannot answer either) and handing back defaults.
"""

from typing import Any
from unittest.mock import AsyncMock, MagicMock

from httpx import AsyncClient
from lease_support import make_fake_redis

from schematic.cache import RedisCache
from schematic.client import AsyncSchematic, AsyncSchematicConfig, DataStreamConfig
from schematic.types import (
    RulesengineCompany,
    RulesengineCondition,
    RulesengineFlag,
    RulesengineRule,
)

COMPANY_ID = "co_cached"
FLAG_KEY = "cached-flag"


def _company() -> RulesengineCompany:
    # A company override grants the flag, so a True verdict can only come from
    # evaluating the cached company. The flag's own default is False.
    condition = RulesengineCondition(
        id="cond_company",
        account_id="acc_1",
        environment_id="env_1",
        condition_type="company",
        operator="eq",
        resource_ids=[COMPANY_ID],
        trait_value="",
    )
    rule = RulesengineRule(
        id="rule_override",
        flag_id="flag_1",
        account_id="acc_1",
        environment_id="env_1",
        name="Company Override",
        rule_type="company_override",
        value=True,
        priority=0,
        conditions=[condition],
        condition_groups=[],
    )
    return RulesengineCompany(
        id=COMPANY_ID,
        account_id="acc_1",
        environment_id="env_1",
        keys={"id": COMPANY_ID},
        traits=[],
        metrics=[],
        rules=[rule],
        entitlements=[],
        billing_product_ids=[],
        credit_balances={},
        plan_ids=[],
        plan_version_ids=[],
    )


def _flag() -> RulesengineFlag:
    return RulesengineFlag(
        id="flag_1",
        key=FLAG_KEY,
        account_id="acc_1",
        environment_id="env_1",
        default_value=False,
        rules=[],
    )


def _health_client(body: dict) -> MagicMock:
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.json = MagicMock(return_value=body)
    client = MagicMock()
    client.get = AsyncMock(return_value=resp)
    return client


async def _replicator_client_not_ready() -> AsyncSchematic:
    """An AsyncSchematic in replicator mode whose replicator has just reported
    ``ready: false`` with the company and flag still in its Redis cache."""
    redis: RedisCache[Any] = RedisCache(make_fake_redis())
    client = AsyncSchematic("test_key", AsyncSchematicConfig(
        logger=MagicMock(),
        httpx_client=MagicMock(spec=AsyncClient),
        event_buffer_period=1,
        flag_defaults={FLAG_KEY: False},
        use_datastream=True,
        datastream=DataStreamConfig(
            replicator_mode=True,
            replicator_health_url="http://replicator.test/ready",
            company_cache=redis,
            company_lookup_cache=redis,
            user_cache=redis,
            user_lookup_cache=redis,
            flag_cache=redis,
        ),
    ))
    ds = client._datastream_client
    assert ds is not None
    await ds._rules_engine.initialize()

    # The replicator was ready, then reports not ready. The poll is what the
    # background health loop runs, driven once here.
    ds._replicator_ready = True
    ds._health_check_client = _health_client({"ready": False, "cache_version": "v1"})
    await ds._check_replicator_health()
    assert not ds.is_connected()

    await ds._cache_company(_company())
    await ds._flag_cache.set(ds._flag_cache_key(FLAG_KEY), _flag())

    # The API is unreachable too, so any fallback to it would surface as the
    # configured default (False) rather than the cached verdict.
    client.features.check_flag = AsyncMock(side_effect=RuntimeError("api unreachable"))
    client.features.check_flags = AsyncMock(side_effect=RuntimeError("api unreachable"))
    client.flag_check_cache_providers = []
    return client


async def test_check_flag_evaluates_from_cache_when_replicator_not_ready() -> None:
    client = await _replicator_client_not_ready()
    try:
        resp = await client.check_flag_with_entitlement(FLAG_KEY, company={"id": COMPANY_ID})
        assert resp.value is True
        assert resp.company_id == COMPANY_ID
        client.features.check_flag.assert_not_called()
    finally:
        await client.shutdown()


async def test_check_flags_evaluates_from_cache_when_replicator_not_ready() -> None:
    client = await _replicator_client_not_ready()
    try:
        results = await client.check_flags([FLAG_KEY], company={"id": COMPANY_ID})
        assert [r.value for r in results] == [True]
        assert results[0].company_id == COMPANY_ID
        client.features.check_flags.assert_not_called()
    finally:
        await client.shutdown()
