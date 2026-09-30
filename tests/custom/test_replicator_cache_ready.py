"""Replicator mode serves flag checks from the cache only once it is ready.

The replicator's /ready endpoint answers 200 with ``ready: true`` once the
cache is complete for its ``cache_version`` and 503 with ``ready: false``
before that. Until the SDK has seen ``ready: true``, check_flag and check_flags
both skip the cache and ask the API; once it has, both evaluate from the cache.
The cache here is seeded the way the replicator writes it: JSON values in
Redis under the versioned keys pinned by tests/datastream/redis_key_layout.json.
"""

from __future__ import annotations

import json
import logging
from typing import Any, AsyncIterator, Callable, Dict, List, Optional
from unittest.mock import AsyncMock, MagicMock

import fakeredis.aioredis
import httpx
import pytest

from schematic.cache.redis import RedisCache
from schematic.client import REASON_ERROR, AsyncSchematic, AsyncSchematicConfig, DataStreamConfig
from schematic.datastream.datastream_client import DataStreamClient
from schematic.types import CheckFlagResponseData

HEALTH_URL = "http://replicator.test/ready"
CACHE_VERSION = "v-ready"
FLAG_KEY = "premium"
COMPANY_KEYS = {"id": "acme"}

# Flag defaults to off; a standard rule turns it on for comp_1 only, so a True
# verdict can only come from evaluating the cached flag against the cached
# company.
FLAG = {
    "id": "flag_1",
    "key": FLAG_KEY,
    "account_id": "acc_1",
    "environment_id": "env_1",
    "default_value": False,
    "rules": [
        {
            "id": "rule_1",
            "account_id": "acc_1",
            "environment_id": "env_1",
            "flag_id": "flag_1",
            "name": "acme gets premium",
            "priority": 1,
            "rule_type": "standard",
            "value": True,
            "condition_groups": [],
            "conditions": [
                {
                    "id": "cond_1",
                    "account_id": "acc_1",
                    "environment_id": "env_1",
                    "condition_type": "company",
                    "operator": "eq",
                    "resource_ids": ["comp_1"],
                    "trait_value": "",
                }
            ],
        }
    ],
}

COMPANY = {
    "id": "comp_1",
    "account_id": "acc_1",
    "environment_id": "env_1",
    "keys": COMPANY_KEYS,
    "billing_product_ids": [],
    "credit_balances": {},
    "metrics": [],
    "plan_ids": [],
    "plan_version_ids": [],
    "rules": [],
    "traits": [],
}


class HealthEndpoint:
    """A scripted replicator /ready endpoint behind an httpx MockTransport."""

    def __init__(self) -> None:
        self.status = 503
        self.body: Any = {"ready": False, "cache_version": CACHE_VERSION}
        self.error: Optional[Exception] = None

    def handler(self, request: httpx.Request) -> httpx.Response:
        if self.error is not None:
            raise self.error
        if isinstance(self.body, str):
            return httpx.Response(self.status, text=self.body)
        return httpx.Response(self.status, json=self.body)

    def client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(transport=httpx.MockTransport(self.handler))


async def _seed_like_the_replicator(redis: Any) -> None:
    # RedisCache prefixes "schematic:" and JSON-encodes every value, the
    # lookup key's company id included.
    await redis.set(f"schematic:flags:{CACHE_VERSION}:{FLAG_KEY}", json.dumps(FLAG))
    await redis.set(f"schematic:company:{CACHE_VERSION}:comp_1", json.dumps(COMPANY))
    await redis.set(f"schematic:company:{CACHE_VERSION}:id:acme", json.dumps("comp_1"))


def _bulk_response(flags: List[CheckFlagResponseData]) -> MagicMock:
    resp = MagicMock()
    resp.data = MagicMock(flags=flags)
    return resp


API_ANSWER = CheckFlagResponseData(flag=FLAG_KEY, value=False, reason="api says no")


class ReplicatorHarness:
    def __init__(self, client: AsyncSchematic, health: HealthEndpoint) -> None:
        self.client = client
        self.health = health

    @property
    def ds(self) -> DataStreamClient:
        ds = self.client._datastream_client
        assert ds is not None
        return ds

    async def poll(self) -> None:
        await self.ds._check_replicator_health()

    def api_answers(self) -> None:
        self.client.features.check_flag = AsyncMock(return_value=MagicMock(data=API_ANSWER))
        self.client.features.check_flags = AsyncMock(return_value=_bulk_response([API_ANSWER]))

    def api_fails(self) -> None:
        self.client.features.check_flag = AsyncMock(side_effect=RuntimeError("api down"))
        self.client.features.check_flags = AsyncMock(side_effect=RuntimeError("api down"))


@pytest.fixture
async def harness() -> AsyncIterator[ReplicatorHarness]:
    redis = fakeredis.aioredis.FakeRedis()
    await _seed_like_the_replicator(redis)
    cache: RedisCache[Any] = RedisCache(redis)
    client = AsyncSchematic(
        "test_key",
        AsyncSchematicConfig(
            logger=logging.getLogger("test_replicator_cache_ready"),
            httpx_client=MagicMock(spec=httpx.AsyncClient),
            event_buffer_period=1,
            use_datastream=True,
            # The flag check cache would answer repeat checks without the API.
            cache_providers=[],
            flag_defaults={FLAG_KEY: True},
            datastream=DataStreamConfig(
                replicator_mode=True,
                replicator_health_url=HEALTH_URL,
                company_cache=cache,
                company_lookup_cache=cache,
                user_cache=cache,
                user_lookup_cache=cache,
                flag_cache=cache,
            ),
        ),
    )
    # Cache-evaluated checks enqueue flag_check events; flushing them to the
    # mocked HTTP client at teardown would only retry and time out.
    client.event_buffer.push = AsyncMock()  # type: ignore[method-assign]
    health = HealthEndpoint()
    h = ReplicatorHarness(client, health)
    h.ds._health_check_client = health.client()
    try:
        yield h
    finally:
        await client.event_buffer.stop()
        assert h.ds._health_check_client is not None
        await h.ds._health_check_client.aclose()
        await redis.aclose()


async def _single(h: ReplicatorHarness) -> CheckFlagResponseData:
    return await h.client.check_flag_with_entitlement(FLAG_KEY, company=COMPANY_KEYS)


async def _bulk(h: ReplicatorHarness) -> CheckFlagResponseData:
    results = await h.client.check_flags([FLAG_KEY], company=COMPANY_KEYS)
    assert len(results) == 1
    return results[0]


CHECKS: Dict[str, Callable[[ReplicatorHarness], Any]] = {"single": _single, "bulk": _bulk}


@pytest.mark.asyncio
class TestReplicatorNotReady:
    @pytest.mark.parametrize("check", CHECKS.values(), ids=CHECKS.keys())
    async def test_skips_the_cache_and_uses_the_api(self, harness: ReplicatorHarness, check: Any) -> None:
        await harness.poll()  # 503, ready: false
        assert not harness.ds.is_cache_ready()
        harness.ds.check_flag = AsyncMock(side_effect=AssertionError("cache must not be read"))  # type: ignore[method-assign]
        harness.api_answers()

        result = await check(harness)

        assert result.value is False
        assert result.reason == "api says no"
        harness.ds.check_flag.assert_not_called()

    @pytest.mark.parametrize("check", CHECKS.values(), ids=CHECKS.keys())
    async def test_returns_the_flag_default_when_the_api_fails(
        self, harness: ReplicatorHarness, check: Any
    ) -> None:
        await harness.poll()
        harness.api_fails()

        result = await check(harness)

        # flag_defaults sets premium to True, so the default is distinguishable
        # from the API's False.
        assert result.value is True
        assert result.reason is not None and result.reason.startswith(REASON_ERROR)

    async def test_before_any_health_response(self, harness: ReplicatorHarness) -> None:
        # No poll yet: the SDK has never seen ready: true.
        harness.api_answers()
        assert (await _single(harness)).reason == "api says no"
        assert (await _bulk(harness)).reason == "api says no"

    async def test_readiness_lost_goes_back_to_the_api(self, harness: ReplicatorHarness) -> None:
        harness.health.status, harness.health.body = 200, {"ready": True, "cache_version": CACHE_VERSION}
        await harness.poll()
        harness.health.error = httpx.ConnectError("connection refused")
        await harness.poll()
        harness.api_answers()

        assert (await _single(harness)).reason == "api says no"
        assert (await _bulk(harness)).reason == "api says no"


@pytest.mark.asyncio
class TestReplicatorReady:
    @pytest.fixture(autouse=True)
    async def ready(self, harness: ReplicatorHarness) -> None:
        await harness.ds._rules_engine.initialize()
        harness.health.status, harness.health.body = 200, {"ready": True, "cache_version": CACHE_VERSION}
        await harness.poll()
        assert harness.ds.is_cache_ready()
        harness.api_fails()

    @pytest.mark.parametrize("check", CHECKS.values(), ids=CHECKS.keys())
    async def test_evaluates_from_the_cache_without_the_api(self, harness: ReplicatorHarness, check: Any) -> None:
        result = await check(harness)

        assert result.value is True
        assert result.company_id == "comp_1"
        assert result.rule_id == "rule_1"
        harness.client.features.check_flag.assert_not_called()
        harness.client.features.check_flags.assert_not_called()

    async def test_single_and_bulk_agree(self, harness: ReplicatorHarness) -> None:
        single = await _single(harness)
        bulk = await _bulk(harness)
        assert single.model_dump() == bulk.model_dump()

    async def test_a_flag_missing_from_the_cache_still_falls_back_to_the_api(self, harness: ReplicatorHarness) -> None:
        harness.api_answers()
        missing = CheckFlagResponseData(flag="not-cached", value=True, reason="api match")
        harness.client.features.check_flag = AsyncMock(return_value=MagicMock(data=missing))
        harness.client.features.check_flags = AsyncMock(return_value=_bulk_response([missing]))

        single = await harness.client.check_flag_with_entitlement("not-cached", company=COMPANY_KEYS)
        bulk = await harness.client.check_flags(["not-cached"], company=COMPANY_KEYS)

        assert single.reason == "api match"
        assert bulk[0].reason == "api match"


@pytest.mark.asyncio
class TestReplicatorHealthPoll:
    async def test_503_sets_not_ready_and_records_the_cache_version(self, harness: ReplicatorHarness) -> None:
        harness.health.status, harness.health.body = 503, {"ready": False, "cache_version": "vX"}
        await harness.poll()

        assert not harness.ds.is_cache_ready()
        assert not harness.ds.is_connected()
        assert harness.ds.replicator_cache_version == "vX"

    async def test_200_ready_sets_ready(self, harness: ReplicatorHarness) -> None:
        harness.health.status, harness.health.body = 200, {"ready": True, "cache_version": "v2"}
        await harness.poll()

        assert harness.ds.is_cache_ready()
        # is_connected keeps reporting replicator readiness for compatibility.
        assert harness.ds.is_connected()
        assert harness.ds.replicator_cache_version == "v2"

    async def test_unreachable_sets_not_ready_and_keeps_the_cache_version(self, harness: ReplicatorHarness) -> None:
        harness.health.status, harness.health.body = 200, {"ready": True, "cache_version": "v1"}
        await harness.poll()
        assert harness.ds.is_cache_ready()

        harness.health.error = httpx.ConnectError("connection refused")
        await harness.poll()

        assert not harness.ds.is_cache_ready()
        assert harness.ds.replicator_cache_version == "v1"

    async def test_unparseable_body_sets_not_ready_and_keeps_the_cache_version(
        self, harness: ReplicatorHarness
    ) -> None:
        harness.health.status, harness.health.body = 200, {"ready": True, "cache_version": "v1"}
        await harness.poll()

        harness.health.status, harness.health.body = 502, "<html>bad gateway</html>"
        await harness.poll()

        assert not harness.ds.is_cache_ready()
        assert harness.ds.replicator_cache_version == "v1"

    async def test_empty_cache_version_keeps_the_last_one(self, harness: ReplicatorHarness) -> None:
        harness.health.status, harness.health.body = 503, {"ready": False, "cache_version": "v1"}
        await harness.poll()
        harness.health.status, harness.health.body = 503, {"ready": False, "cache_version": ""}
        await harness.poll()

        assert harness.ds.replicator_cache_version == "v1"

    async def test_health_changed_callback_fires_on_transitions(self, harness: ReplicatorHarness) -> None:
        changes: List[bool] = []
        harness.ds._on_replicator_health_changed = changes.append

        harness.health.status, harness.health.body = 200, {"ready": True, "cache_version": "v1"}
        await harness.poll()
        await harness.poll()
        harness.health.status, harness.health.body = 503, {"ready": False, "cache_version": "v2"}
        await harness.poll()

        assert changes == [True, False]

    async def test_cache_version_lookup_reads_a_503_body(self, harness: ReplicatorHarness) -> None:
        harness.health.status, harness.health.body = 503, {"ready": False, "cache_version": "v9"}
        assert await harness.ds.get_replicator_cache_version_async() == "v9"


def test_is_cache_ready_is_true_outside_replicator_mode() -> None:
    """Websocket mode fills and fetches its own cache, so it never waits on
    readiness; its flag check behavior is unchanged."""
    from schematic.datastream.datastream_client import DataStreamClientOptions

    ds = DataStreamClient(DataStreamClientOptions(api_key="k", logger=logging.getLogger("t"), base_url="ws://x"))
    assert ds.is_cache_ready()
    assert not ds.is_connected()
