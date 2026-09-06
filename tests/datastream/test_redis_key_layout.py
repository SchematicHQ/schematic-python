"""Replicator Redis key layout contract.

``redis_key_layout.json`` is a copy of schematic-replicator/testdata/redis_key_layout.json:
the keys the replicator writes. In replicator mode this SDK reads them, so the
Redis provider prefix plus the datastream key must reproduce them exactly. The
C# and Ruby SDKs doubled the prefix for a year with no test on either side
(SCH-7070); this is that test.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict

import pytest
from .test_datastream_client import MockCacheProvider

from schematic.cache.redis import RedisCache
from schematic.datastream.datastream_client import DataStreamClient, DataStreamClientOptions

CACHE_VERSION = "v-test"
FIXTURE = json.loads((Path(__file__).parent / "redis_key_layout.json").read_text())


@pytest.fixture
def client() -> DataStreamClient:
    cache = MockCacheProvider()
    c = DataStreamClient(
        DataStreamClientOptions(
            api_key="test-key",
            logger=logging.getLogger("test_redis_key_layout"),
            replicator_mode=True,
            company_cache=cache,
            company_lookup_cache=cache,
            user_cache=cache,
            user_lookup_cache=cache,
            flag_cache=cache,
        )
    )
    # Set from the replicator's health response in production.
    c._replicator_cache_version = CACHE_VERSION
    return c


def _build(client: DataStreamClient, kind: str, inp: Dict[str, str]) -> str:
    if kind == "flag":
        return client._flag_cache_key(inp["key"])
    if kind == "company_id":
        return client._resource_id_cache_key("company", inp["id"])
    if kind == "company_lookup":
        return client._resource_key_to_cache_key("company", inp["key"], inp["value"])
    if kind == "user_id":
        return client._resource_id_cache_key("user", inp["id"])
    if kind == "user_lookup":
        return client._resource_key_to_cache_key("user", inp["key"], inp["value"])
    raise AssertionError(f"fixture case kind {kind!r} has no builder here")


@pytest.mark.parametrize("case", FIXTURE["cases"], ids=[c["kind"] for c in FIXTURE["cases"]])
def test_redis_key_matches_replicator_layout(client: DataStreamClient, case: Dict[str, Any]) -> None:
    # RedisCache's default prefix is what the testapp and docs use; the
    # replicator's fixed prefix must be the same string.
    redis: RedisCache[Any] = RedisCache(client=None)
    assert redis._prefix == FIXTURE["prefix"]
    key = redis._prefixed(_build(client, case["kind"], case["input"]))
    assert key == case["key"].replace("<VERSION>", CACHE_VERSION)
