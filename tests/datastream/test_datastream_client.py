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
        await client.close()  # Should not raise


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

    async def test_flag_evaluation_with_cached_company(self, logger: logging.Logger) -> None:
        """Spec test #6: Flag evaluation with cached company."""
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

        # Cache a company via full message
        await client._handle_message(DataStreamResp(
            data={
                "id": "co_eval",
                "keys": {"slug": "eval-co"},
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
        ))

        # Cache a flag
        await client._handle_message(DataStreamResp(
            data={"key": "co-flag", "id": "f1", "default_value": True, "rules": [], "account_id": "acc_1", "environment_id": "env_1"},
            entity_type=EntityType.FLAG.value,
            message_type=MessageType.FULL.value,
        ))

        result = await client.check_flag(
            CheckFlagRequestBody(company={"slug": "eval-co"}),
            "co-flag",
        )
        assert isinstance(result, RulesengineCheckFlagResult)
        assert result.company_id == "co_eval"
        assert result.flag_key == "co-flag"

    async def test_flag_evaluation_with_cached_user(self, logger: logging.Logger) -> None:
        """Spec test #7: Flag evaluation with cached user."""
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

        # Cache a user
        await client._handle_message(DataStreamResp(
            data={
                "id": "usr_eval",
                "keys": {"email": "eval@test.com"},
                "account_id": "acc_1",
                "environment_id": "env_1",
                "rules": [],
                "traits": [],
            },
            entity_type=EntityType.USER.value,
            message_type=MessageType.FULL.value,
        ))

        # Cache a flag
        await client._handle_message(DataStreamResp(
            data={"key": "usr-flag", "id": "f2", "default_value": False, "rules": [], "account_id": "acc_1", "environment_id": "env_1"},
            entity_type=EntityType.FLAG.value,
            message_type=MessageType.FULL.value,
        ))

        result = await client.check_flag(
            CheckFlagRequestBody(user={"email": "eval@test.com"}),
            "usr-flag",
        )
        assert isinstance(result, RulesengineCheckFlagResult)
        assert result.user_id == "usr_eval"
        assert result.flag_key == "usr-flag"


class TestDataStreamClientPartialMerge:
    """Spec test #4: Partial entity message merges into cache."""

    @pytest.fixture
    def client_with_cache(self, logger: logging.Logger) -> tuple[DataStreamClient, MockCacheProvider]:
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
        return client, cache

    async def test_partial_company_merges_keys(
        self,
        client_with_cache: tuple[DataStreamClient, MockCacheProvider],
    ) -> None:
        client, _ = client_with_cache

        # Add full company
        await client._handle_message(DataStreamResp(
            data={
                "id": "co_partial",
                "keys": {"slug": "original"},
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
        ))

        # Partial update adds a new key. Wire shape: data is the wrapped
        # partial payload (no top-level id); cache lookup uses entity_id from
        # the envelope.
        await client._handle_message(DataStreamResp(
            data={"keys": {"domain": "example.com"}},
            entity_id="co_partial",
            entity_type=EntityType.COMPANY.value,
            message_type=MessageType.PARTIAL.value,
        ))

        company = await client._get_company_from_cache({"slug": "original"})
        assert company is not None
        assert company.keys == {"slug": "original", "domain": "example.com"}

    async def test_partial_user_merges_keys(
        self,
        client_with_cache: tuple[DataStreamClient, MockCacheProvider],
    ) -> None:
        client, _ = client_with_cache

        # Add full user
        await client._handle_message(DataStreamResp(
            data={
                "id": "usr_partial",
                "keys": {"email": "orig@test.com"},
                "account_id": "acc_1",
                "environment_id": "env_1",
                "rules": [],
                "traits": [],
            },
            entity_type=EntityType.USER.value,
            message_type=MessageType.FULL.value,
        ))

        # Partial update adds a new key. Wire shape: data is the wrapped
        # partial payload (no top-level id); cache lookup uses entity_id from
        # the envelope.
        await client._handle_message(DataStreamResp(
            data={"keys": {"slack_id": "U123"}},
            entity_id="usr_partial",
            entity_type=EntityType.USER.value,
            message_type=MessageType.PARTIAL.value,
        ))

        user = await client._get_user_from_cache({"email": "orig@test.com"})
        assert user is not None
        assert user.keys == {"email": "orig@test.com", "slack_id": "U123"}


class TestDataStreamClientDeepCopy:
    """Spec test #12: Deep copy prevents mutation of cached entities."""

    async def test_cached_company_mutation_does_not_affect_cache(self, logger: logging.Logger) -> None:
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

        await client._handle_message(DataStreamResp(
            data={
                "id": "co_mut",
                "keys": {"slug": "mutable"},
                "account_id": "acc_1",
                "environment_id": "env_1",
                "billing_product_ids": ["bp-1"],
                "credit_balances": {},
                "metrics": [],
                "plan_ids": [],
                "plan_version_ids": [],
                "rules": [],
                "traits": [],
            },
            entity_type=EntityType.COMPANY.value,
            message_type=MessageType.FULL.value,
        ))

        # Retrieve and mutate
        company = await client._get_company_from_cache({"slug": "mutable"})
        assert company is not None
        original_ids = list(company.billing_product_ids)
        company.billing_product_ids.append("bp-INJECTED")

        # Re-retrieve — cache should be unaffected
        fresh = await client._get_company_from_cache({"slug": "mutable"})
        assert fresh is not None
        assert fresh.billing_product_ids == original_ids

    async def test_cached_user_mutation_does_not_affect_cache(self, logger: logging.Logger) -> None:
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

        await client._handle_message(DataStreamResp(
            data={
                "id": "usr_mut",
                "keys": {"email": "mut@test.com"},
                "account_id": "acc_1",
                "environment_id": "env_1",
                "rules": [],
                "traits": [],
            },
            entity_type=EntityType.USER.value,
            message_type=MessageType.FULL.value,
        ))

        user = await client._get_user_from_cache({"email": "mut@test.com"})
        assert user is not None
        user.keys["injected"] = "bad"

        fresh = await client._get_user_from_cache({"email": "mut@test.com"})
        assert fresh is not None
        assert "injected" not in fresh.keys


class TestDataStreamClientMissingEntityTimeout:
    """Spec test #8: Missing company triggers fetch/wait (times out without WS)."""

    async def test_get_company_times_out_without_connection(self, logger: logging.Logger) -> None:
        client = DataStreamClient(DataStreamClientOptions(
            api_key="test-key",
            base_url="https://api.schematichq.com",
            logger=logger,
        ))
        with pytest.raises(RuntimeError, match="not connected"):
            await client.get_company({"slug": "missing"})

    async def test_get_user_times_out_without_connection(self, logger: logging.Logger) -> None:
        client = DataStreamClient(DataStreamClientOptions(
            api_key="test-key",
            base_url="https://api.schematichq.com",
            logger=logger,
        ))
        with pytest.raises(RuntimeError, match="not connected"):
            await client.get_user({"email": "missing@test.com"})


class TestDataStreamClientMissingCompanyFetch:
    """Spec DataStream checklist item 8: Missing company triggers fetch/wait.

    When get_company is called and the company is not in cache, the client
    must send a request over the WebSocket and resolve when the response
    populates the cache.
    """

    async def test_get_company_sends_request_when_not_cached(
        self, logger: logging.Logger
    ) -> None:
        client = DataStreamClient(DataStreamClientOptions(
            api_key="test-key",
            base_url="https://api.schematichq.com",
            logger=logger,
        ))

        # Inject a fake connected WS client that captures send_message calls.
        sent_requests: List[Any] = []

        fake_ws = MagicMock()
        fake_ws.is_connected = MagicMock(return_value=True)
        fake_ws.send_message = AsyncMock(side_effect=lambda req: sent_requests.append(req))
        client._ws_client = fake_ws

        from schematic.types import RulesengineCompany

        # Schedule a task that, after the request is "sent", simulates the
        # WebSocket response by populating the cache and resolving pending futures.
        async def simulate_response() -> None:
            # Wait for the request to be issued
            for _ in range(50):
                if sent_requests:
                    break
                await asyncio.sleep(0.01)
            company = RulesengineCompany(
                id="co_fetch", account_id="a", environment_id="e",
                keys={"slug": "fetch-me"}, billing_product_ids=[], credit_balances={},
                metrics=[], plan_ids=[], plan_version_ids=[], rules=[], traits=[],
            )
            await client._cache_company(company)
            client._notify_pending_company({"slug": "fetch-me"}, company)

        responder = asyncio.create_task(simulate_response())
        try:
            result = await client.get_company({"slug": "fetch-me"})
        finally:
            await responder

        assert result.id == "co_fetch"
        assert len(sent_requests) == 1
        # Verify the request payload targeted the company entity
        sent = sent_requests[0]
        assert sent.data.entity_type == EntityType.COMPANY
        assert sent.data.keys == {"slug": "fetch-me"}

    async def test_get_company_times_out_when_no_response(
        self, logger: logging.Logger
    ) -> None:
        """If the simulated WS never responds, get_company should raise TimeoutError."""
        client = DataStreamClient(DataStreamClientOptions(
            api_key="test-key",
            base_url="https://api.schematichq.com",
            logger=logger,
        ))

        fake_ws = MagicMock()
        fake_ws.is_connected = MagicMock(return_value=True)
        fake_ws.send_message = AsyncMock()
        client._ws_client = fake_ws

        # Patch RESOURCE_TIMEOUT_MS to a tiny value to keep the test fast
        with patch("schematic.datastream.datastream_client.RESOURCE_TIMEOUT_MS", 50):
            with pytest.raises(TimeoutError, match="Timeout while waiting for company"):
                await client.get_company({"slug": "never-arrives"})


class TestDataStreamClientReplicatorHealthCheck:
    """Spec §Replicator Mode: health check polling against replicator_health_url."""

    async def test_health_check_marks_replicator_ready_on_success(
        self, logger: logging.Logger
    ) -> None:
        cache = MockCacheProvider()
        client = DataStreamClient(DataStreamClientOptions(
            api_key="test-key",
            logger=logger,
            replicator_mode=True,
            replicator_health_url="http://localhost:8090/ready",
            company_cache=cache, company_lookup_cache=cache,
            user_cache=cache, user_lookup_cache=cache, flag_cache=cache,
        ))

        # Mock the httpx AsyncClient so we never make a real network call.
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json = MagicMock(return_value={"ready": True, "cache_version": "v1"})

        mock_http = MagicMock()
        mock_http.get = AsyncMock(return_value=mock_response)
        client._health_check_client = mock_http

        assert not client.is_replicator_ready()
        await client._check_replicator_health()

        assert client.is_replicator_ready()
        assert client.replicator_cache_version == "v1"
        mock_http.get.assert_called_once_with("http://localhost:8090/ready")

    async def test_health_check_invokes_callback_on_state_change(
        self, logger: logging.Logger
    ) -> None:
        cache = MockCacheProvider()
        callbacks: List[bool] = []
        client = DataStreamClient(DataStreamClientOptions(
            api_key="test-key",
            logger=logger,
            replicator_mode=True,
            company_cache=cache, company_lookup_cache=cache,
            user_cache=cache, user_lookup_cache=cache, flag_cache=cache,
            on_replicator_health_changed=callbacks.append,
        ))

        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json = MagicMock(return_value={"ready": True})

        mock_http = MagicMock()
        mock_http.get = AsyncMock(return_value=mock_response)
        client._health_check_client = mock_http

        await client._check_replicator_health()
        assert callbacks == [True]


class TestDataStreamClientReplicatorUnhealthyFallback:
    """Spec §Replicator Mode: failed health check sets replicator_ready=False
    and fires the on_replicator_health_changed(False) callback.
    """

    async def test_health_check_failure_marks_replicator_not_ready(
        self, logger: logging.Logger
    ) -> None:
        cache = MockCacheProvider()
        callbacks: List[bool] = []
        client = DataStreamClient(DataStreamClientOptions(
            api_key="test-key",
            logger=logger,
            replicator_mode=True,
            company_cache=cache, company_lookup_cache=cache,
            user_cache=cache, user_lookup_cache=cache, flag_cache=cache,
            on_replicator_health_changed=callbacks.append,
        ))
        # Force ready=True so the failure produces a state transition
        client._replicator_ready = True

        mock_http = MagicMock()
        mock_http.get = AsyncMock(side_effect=Exception("connection refused"))
        client._health_check_client = mock_http

        await client._check_replicator_health()

        assert not client.is_replicator_ready()
        assert callbacks == [False]

    async def test_health_check_http_error_marks_not_ready(
        self, logger: logging.Logger
    ) -> None:
        """A non-2xx response (raise_for_status) should also mark unhealthy."""
        cache = MockCacheProvider()
        client = DataStreamClient(DataStreamClientOptions(
            api_key="test-key",
            logger=logger,
            replicator_mode=True,
            company_cache=cache, company_lookup_cache=cache,
            user_cache=cache, user_lookup_cache=cache, flag_cache=cache,
        ))
        client._replicator_ready = True

        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock(side_effect=Exception("503 Service Unavailable"))

        mock_http = MagicMock()
        mock_http.get = AsyncMock(return_value=mock_response)
        client._health_check_client = mock_http

        await client._check_replicator_health()
        assert not client.is_replicator_ready()


class TestDataStreamClientDefaultReplicatorHealthUrl:
    """Verify replicator_health_url defaults to spec canonical value."""

    def test_default_health_url(self, logger: logging.Logger) -> None:
        opts = DataStreamClientOptions(
            api_key="test-key",
            logger=logger,
        )
        assert opts.replicator_health_url == "http://localhost:8090/ready"

    def test_custom_health_url_overrides_default(self, logger: logging.Logger) -> None:
        opts = DataStreamClientOptions(
            api_key="test-key",
            logger=logger,
            replicator_health_url="http://custom:9090/health",
        )
        assert opts.replicator_health_url == "http://custom:9090/health"
