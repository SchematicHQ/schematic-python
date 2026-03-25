from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, List, Optional
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from schematic.cache import AsyncCacheProvider as CacheProvider, AsyncLocalCache as LocalCache
from schematic.datastream.datastream_client import DataStreamClient, DataStreamClientOptions
from schematic.datastream.types import DataStreamResp, EntityType, MessageType
from schematic.types import CheckFlagRequestBody, RulesengineCheckFlagResult


class MockCacheProvider(CacheProvider[Any]):
    """Simple in-memory cache for testing."""

    def __init__(self) -> None:
        self._store: Dict[str, Any] = {}

    async def get(self, key: str) -> Optional[Any]:
        return self._store.get(key)

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        self._store[key] = value

    async def delete(self, key: str) -> None:
        self._store.pop(key, None)

    async def delete_missing(self, keys_to_keep: List[str], *, scan_pattern: Optional[str] = None) -> None:
        keep = set(keys_to_keep)
        to_delete = [k for k in self._store if k not in keep]
        for k in to_delete:
            del self._store[k]


@pytest.fixture
def logger() -> logging.Logger:
    return logging.getLogger("test_datastream")


class TestDataStreamClientInit:
    def test_replicator_mode_requires_cache_providers(self, logger: logging.Logger) -> None:
        with pytest.raises(ValueError, match="Replicator mode requires"):
            DataStreamClient(DataStreamClientOptions(
                api_key="test-key",
                logger=logger,
                replicator_mode=True,
            ))

    def test_replicator_mode_accepts_custom_cache(self, logger: logging.Logger) -> None:
        cache = MockCacheProvider()
        client = DataStreamClient(DataStreamClientOptions(
            api_key="test-key",
            logger=logger,
            replicator_mode=True,
            company_cache=cache,
            company_lookup_cache=cache,
            user_cache=cache,
            user_lookup_cache=cache,
            flag_cache=cache,
        ))
        assert client.is_replicator_mode()
        assert not client.is_connected()

    def test_normal_mode_defaults(self, logger: logging.Logger) -> None:
        client = DataStreamClient(DataStreamClientOptions(
            api_key="test-key",
            base_url="https://api.schematichq.com",
            logger=logger,
        ))
        assert not client.is_replicator_mode()
        assert not client.is_connected()


class TestDataStreamClientReplicatorMode:
    @pytest.fixture
    def client(self, logger: logging.Logger) -> DataStreamClient:
        cache = MockCacheProvider()
        return DataStreamClient(DataStreamClientOptions(
            api_key="test-key",
            logger=logger,
            replicator_mode=True,
            company_cache=cache,
            company_lookup_cache=cache,
            user_cache=cache,
            user_lookup_cache=cache,
            flag_cache=cache,
        ))

    async def test_get_company_raises_when_not_cached(self, client: DataStreamClient) -> None:
        with pytest.raises(RuntimeError, match="not found in cache"):
            await client.get_company({"id": "co_123"})

    async def test_get_user_raises_when_not_cached(self, client: DataStreamClient) -> None:
        with pytest.raises(RuntimeError, match="not found in cache"):
            await client.get_user({"id": "usr_123"})


class TestDataStreamClientMessageHandling:
    @pytest.fixture
    def client_with_cache(self, logger: logging.Logger) -> tuple[DataStreamClient, MockCacheProvider, MockCacheProvider, MockCacheProvider]:
        company_cache = MockCacheProvider()
        user_cache = MockCacheProvider()
        flag_cache = MockCacheProvider()
        lookup_cache = MockCacheProvider()
        client = DataStreamClient(DataStreamClientOptions(
            api_key="test-key",
            logger=logger,
            replicator_mode=True,
            company_cache=company_cache,
            company_lookup_cache=lookup_cache,
            user_cache=user_cache,
            user_lookup_cache=lookup_cache,
            flag_cache=flag_cache,
        ))
        return client, company_cache, user_cache, flag_cache

    async def test_handle_company_message_caches_data(
        self,
        client_with_cache: tuple[DataStreamClient, MockCacheProvider, MockCacheProvider, MockCacheProvider],
    ) -> None:
        client, company_cache, _, _ = client_with_cache
        msg = DataStreamResp(
            data={
                "id": "co_123",
                "keys": {"slug": "acme"},
                "account_id": "acc_1",
                "environment_id": "env_1",
                "billing_product_ids": [],
                "credit_balances": {},
                "metrics": [],
                "plan_ids": [],
                "plan_version_ids": [],
                "rules": [],
                "traits": [],
            },
            entity_type=EntityType.COMPANY.value,
            message_type=MessageType.FULL.value,
        )
        await client._handle_message(msg)

        # Company should be retrievable from cache
        company = await client._get_company_from_cache({"slug": "acme"})
        assert company is not None
        assert company.id == "co_123"

    async def test_handle_user_message_caches_data(
        self,
        client_with_cache: tuple[DataStreamClient, MockCacheProvider, MockCacheProvider, MockCacheProvider],
    ) -> None:
        client, _, user_cache, _ = client_with_cache
        msg = DataStreamResp(
            data={
                "id": "usr_456",
                "keys": {"email": "test@example.com"},
                "account_id": "acc_1",
                "environment_id": "env_1",
                "rules": [],
                "traits": [],
            },
            entity_type=EntityType.USER.value,
            message_type=MessageType.FULL.value,
        )
        await client._handle_message(msg)

        user = await client._get_user_from_cache({"email": "test@example.com"})
        assert user is not None
        assert user.id == "usr_456"

    async def test_handle_flags_message_caches_all_flags(
        self,
        client_with_cache: tuple[DataStreamClient, MockCacheProvider, MockCacheProvider, MockCacheProvider],
    ) -> None:
        client, _, _, flag_cache = client_with_cache
        flags = [
            {"key": "flag-a", "id": "f1", "default_value": True, "rules": [], "account_id": "acc_1", "environment_id": "env_1"},
            {"key": "flag-b", "id": "f2", "default_value": False, "rules": [], "account_id": "acc_1", "environment_id": "env_1"},
        ]
        msg = DataStreamResp(
            data=flags,
            entity_type=EntityType.FLAGS.value,
            message_type=MessageType.FULL.value,
        )
        await client._handle_message(msg)

        flag_a = await client.get_flag("flag-a")
        flag_b = await client.get_flag("flag-b")
        assert flag_a is not None
        assert flag_a.key == "flag-a"
        assert flag_b is not None
        assert flag_b.key == "flag-b"

    async def test_handle_flag_delete(
        self,
        client_with_cache: tuple[DataStreamClient, MockCacheProvider, MockCacheProvider, MockCacheProvider],
    ) -> None:
        client, _, _, flag_cache = client_with_cache

        # First add a flag
        msg = DataStreamResp(
            data={"key": "flag-x", "id": "fx", "default_value": True, "rules": [], "account_id": "acc_1", "environment_id": "env_1"},
            entity_type=EntityType.FLAG.value,
            message_type=MessageType.FULL.value,
        )
        await client._handle_message(msg)
        assert await client.get_flag("flag-x") is not None

        # Then delete it
        msg = DataStreamResp(
            data={"key": "flag-x", "id": "fx", "default_value": False, "rules": [], "account_id": "acc_1", "environment_id": "env_1"},
            entity_type=EntityType.FLAG.value,
            message_type=MessageType.DELETE.value,
        )
        await client._handle_message(msg)
        assert await client.get_flag("flag-x") is None

    async def test_handle_company_delete(
        self,
        client_with_cache: tuple[DataStreamClient, MockCacheProvider, MockCacheProvider, MockCacheProvider],
    ) -> None:
        client, company_cache, _, _ = client_with_cache

        # Add company
        msg = DataStreamResp(
            data={
                "id": "co_del",
                "keys": {"slug": "delete-me"},
                "account_id": "acc_1",
                "environment_id": "env_1",
                "billing_product_ids": [],
                "credit_balances": {},
                "metrics": [],
                "plan_ids": [],
                "plan_version_ids": [],
                "rules": [],
                "traits": [],
            },
            entity_type=EntityType.COMPANY.value,
            message_type=MessageType.FULL.value,
        )
        await client._handle_message(msg)
        assert await client._get_company_from_cache({"slug": "delete-me"}) is not None

        # Delete company
        msg = DataStreamResp(
            data={
                "id": "co_del",
                "keys": {"slug": "delete-me"},
                "account_id": "acc_1",
                "environment_id": "env_1",
                "billing_product_ids": [],
                "credit_balances": {},
                "metrics": [],
                "plan_ids": [],
                "plan_version_ids": [],
                "rules": [],
                "traits": [],
            },
            entity_type=EntityType.COMPANY.value,
            message_type=MessageType.DELETE.value,
        )
        await client._handle_message(msg)
        assert await client._get_company_from_cache({"slug": "delete-me"}) is None

    async def test_handle_error_message(
        self,
        client_with_cache: tuple[DataStreamClient, MockCacheProvider, MockCacheProvider, MockCacheProvider],
    ) -> None:
        client, _, _, _ = client_with_cache
        msg = DataStreamResp(
            data={"error": "test error", "keys": {"id": "co_err"}, "entity_type": EntityType.COMPANY.value},
            entity_type=EntityType.COMPANY.value,
            message_type=MessageType.ERROR.value,
        )
        # Should not raise
        await client._handle_message(msg)


class TestDataStreamClientClose:
    async def test_close_cleans_up(self, logger: logging.Logger) -> None:
        cache = MockCacheProvider()
        client = DataStreamClient(DataStreamClientOptions(
            api_key="test-key",
            logger=logger,
            replicator_mode=True,
            company_cache=cache,
            company_lookup_cache=cache,
            user_cache=cache,
            user_lookup_cache=cache,
            flag_cache=cache,
        ))
        client.close()  # Should not raise


class TestDataStreamClientCacheKeys:
    def test_flag_cache_key_uses_version(self, logger: logging.Logger) -> None:
        client = DataStreamClient(DataStreamClientOptions(
            api_key="test-key",
            base_url="https://api.schematichq.com",
            logger=logger,
        ))
        key = client._flag_cache_key("Premium-Feature")
        # Should be lowercased and include version key
        assert "premium-feature" in key
        assert key.startswith("flags:")

    def test_resource_key_to_cache_key_lowercases(self, logger: logging.Logger) -> None:
        client = DataStreamClient(DataStreamClientOptions(
            api_key="test-key",
            base_url="https://api.schematichq.com",
            logger=logger,
        ))
        key = client._resource_key_to_cache_key("company", "Slug", "AcmeCorp")
        assert "slug" in key
        assert "acmecorp" in key


class TestDataStreamClientFlagEvaluation:
    async def test_evaluate_flag_returns_default_when_engine_unavailable(self, logger: logging.Logger) -> None:
        from schematic.types import RulesengineFlag

        cache = MockCacheProvider()
        client = DataStreamClient(DataStreamClientOptions(
            api_key="test-key",
            logger=logger,
            replicator_mode=True,
            company_cache=cache,
            company_lookup_cache=cache,
            user_cache=cache,
            user_lookup_cache=cache,
            flag_cache=cache,
        ))
        flag = RulesengineFlag(
            id="f1", key="test", account_id="a", environment_id="e",
            default_value=True, rules=[],
        )
        result = client._evaluate_flag(flag, None, None)
        assert isinstance(result, RulesengineCheckFlagResult)
        assert result.value is True
        assert result.reason == "RULES_ENGINE_UNAVAILABLE"
        assert result.flag_key == "test"

    async def test_check_flag_raises_when_flag_not_found(self, logger: logging.Logger) -> None:
        cache = MockCacheProvider()
        client = DataStreamClient(DataStreamClientOptions(
            api_key="test-key",
            logger=logger,
            replicator_mode=True,
            company_cache=cache,
            company_lookup_cache=cache,
            user_cache=cache,
            user_lookup_cache=cache,
            flag_cache=cache,
        ))
        with pytest.raises(RuntimeError, match="Flag not found"):
            await client.check_flag(CheckFlagRequestBody(), "nonexistent-flag")
