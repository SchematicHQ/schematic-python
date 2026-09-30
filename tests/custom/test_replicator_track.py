"""Track's local usage update in replicator mode while the replicator reports
not ready.

When a Schematic account is closed or Schematic is unreachable, the replicator
stays up and keeps its cache but reports ``ready: false``. Flag checks keep
evaluating from that cache, so track has to keep bumping the cached company
metric, or a numeric limit would never trip while the replicator is down.
"""

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

from httpx import AsyncClient
from lease_support import make_fake_redis

from schematic.cache import RedisCache
from schematic.client import AsyncSchematic, AsyncSchematicConfig, DataStreamConfig
from schematic.types import (
    RulesengineCompany,
    RulesengineCompanyMetric,
    RulesengineCondition,
    RulesengineFlag,
    RulesengineRule,
)

COMPANY_ID = "co_metered"
FLAG_KEY = "api-access"
EVENT = "api-calls"
LIMIT = 100


def _metered_company(usage: int) -> RulesengineCompany:
    # A company override grants the flag while usage stays under LIMIT.
    company_condition = RulesengineCondition(
        id="cond_company",
        account_id="acc_1",
        environment_id="env_1",
        condition_type="company",
        operator="eq",
        resource_ids=[COMPANY_ID],
        trait_value="",
    )
    metric_condition = RulesengineCondition(
        id="cond_metric",
        account_id="acc_1",
        environment_id="env_1",
        condition_type="metric",
        operator="lt",
        resource_ids=[],
        event_subtype=EVENT,
        metric_value=LIMIT,
        metric_period="all_time",
        trait_value=str(LIMIT),
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
        conditions=[company_condition, metric_condition],
        condition_groups=[],
    )
    metric = RulesengineCompanyMetric(
        account_id="acc_1",
        environment_id="env_1",
        company_id=COMPANY_ID,
        event_subtype=EVENT,
        period="all_time",
        month_reset="first_of_month",
        value=usage,
        created_at="2026-01-01T00:00:00Z",
    )
    return RulesengineCompany(
        id=COMPANY_ID,
        account_id="acc_1",
        environment_id="env_1",
        keys={"id": COMPANY_ID},
        traits=[],
        metrics=[metric],
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


async def _replicator_client_not_ready(usage: int) -> AsyncSchematic:
    """An AsyncSchematic in replicator mode whose replicator has just reported
    ``ready: false`` with a metered company and its flag still in Redis."""
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

    await ds._cache_company(_metered_company(usage))
    await ds._flag_cache.set(ds._flag_cache_key(FLAG_KEY), _flag())

    client.features.check_flag = AsyncMock(side_effect=RuntimeError("api unreachable"))
    client.flag_check_cache_providers = []
    return client


async def test_track_counts_usage_locally_when_replicator_not_ready() -> None:
    client = await _replicator_client_not_ready(usage=95)
    ds = client._datastream_client
    assert ds is not None
    try:
        with patch.object(client.event_buffer, "push", new=AsyncMock()) as push:
            assert await client.check_flag(FLAG_KEY, company={"id": COMPANY_ID}) is True

            await client.track(EVENT, company={"id": COMPANY_ID}, quantity=10)

            # The event still goes out for the server to count.
            track_events = [c.args[0] for c in push.await_args_list if c.args[0].event_type == "track"]
            assert len(track_events) == 1

        cached = await ds.get_cached_company({"id": COMPANY_ID})
        assert cached is not None
        assert cached.metrics is not None
        assert cached.metrics[0].value == 105

        # The cached figure now crosses the limit, so the check denies without
        # waiting for the replicator to come back.
        assert await client.check_flag(FLAG_KEY, company={"id": COMPANY_ID}) is False
        client.features.check_flag.assert_not_called()
    finally:
        await client.shutdown()


async def test_track_for_an_uncached_company_is_a_no_op_when_replicator_not_ready() -> None:
    client = await _replicator_client_not_ready(usage=0)
    ds = client._datastream_client
    assert ds is not None
    try:
        with patch.object(client.event_buffer, "push", new=AsyncMock()) as push:
            await client.track(EVENT, company={"id": "co_unknown"}, quantity=10)
            push.assert_awaited_once()

        # Nothing is invented for a company the replicator never cached, and
        # the cached one is untouched.
        assert await ds.get_cached_company({"id": "co_unknown"}) is None
        cached = await ds.get_cached_company({"id": COMPANY_ID})
        assert cached is not None
        assert cached.metrics is not None
        assert cached.metrics[0].value == 0
    finally:
        await client.shutdown()
