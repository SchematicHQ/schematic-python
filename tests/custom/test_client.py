import time
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import AsyncClient, Client

from schematic.cache import LocalCache
from schematic.client import (
    AsyncSchematic,
    AsyncSchematicConfig,
    CheckFlagOptions,
    Schematic,
    SchematicConfig,
)
from schematic.types import CheckFlagResponseData, FeatureEntitlement


class TestSchematic(unittest.TestCase):

    def setUp(self):
        config = SchematicConfig(
            event_buffer_period=1,
            logger=MagicMock(),
            httpx_client=MagicMock(spec=Client),
        )
        self.schematic = Schematic("api_key", config)

    def test_check_flag_offline(self):
        self.schematic.offline = True
        self.schematic.flag_defaults = {"test_flag": True}
        result = self.schematic.check_flag(
            "test_flag",
            company={"id": "company_id"},
            user={"id": "user_id"},
        )
        self.assertTrue(result)

    def test_check_flag_online(self):
        self.schematic.offline = False
        self.schematic.features.check_flag = MagicMock(
            return_value=MagicMock(data=MagicMock(value=True))
        )
        result = self.schematic.check_flag(
            "test_flag",
            company={"id": "company_id"},
            user={"id": "user_id"},
        )
        self.assertTrue(result)

    def test_check_flag_with_entitlement_offline(self):
        self.schematic.offline = True
        self.schematic.flag_defaults = {"test_flag": True}
        result = self.schematic.check_flag_with_entitlement(
            "test_flag",
            company={"id": "company_id"},
            user={"id": "user_id"},
        )
        self.assertIsInstance(result, CheckFlagResponseData)
        self.assertTrue(result.value)
        self.assertEqual(result.flag, "test_flag")
        self.assertEqual(result.reason, "flag default")

    def test_check_flag_with_entitlement_online(self):
        self.schematic.offline = False
        mock_data = CheckFlagResponseData(
            value=True,
            company_id="comp_123",
            entitlement=None,
            error=None,
            flag="test_flag",
            flag_id="flag_123",
            reason="rule_match",
            rule_id="rule_123",
            rule_type="override",
            user_id="user_123",
        )
        self.schematic.features.check_flag = MagicMock(
            return_value=MagicMock(data=mock_data)
        )
        result = self.schematic.check_flag_with_entitlement(
            "test_flag",
            company={"id": "company_id"},
            user={"id": "user_id"},
        )
        self.assertIsInstance(result, CheckFlagResponseData)
        self.assertTrue(result.value)
        self.assertEqual(result.company_id, "comp_123")
        self.assertEqual(result.reason, "rule_match")
        self.assertEqual(result.rule_id, "rule_123")

    def test_check_flag_with_options_default_value(self):
        self.schematic.offline = True
        options = CheckFlagOptions(default_value=True)
        result = self.schematic.check_flag("missing_flag", options=options)
        self.assertTrue(result)

    def test_check_flag_with_options_callable_default(self):
        self.schematic.offline = True
        options = CheckFlagOptions(default_value=lambda: True)
        result = self.schematic.check_flag("missing_flag", options=options)
        self.assertTrue(result)

    def test_check_flag_caches_full_response(self):
        """Verify that cache stores the full response, not just a bool."""
        self.schematic.offline = False
        mock_data = CheckFlagResponseData(
            value=True,
            company_id="comp_123",
            entitlement=None,
            error=None,
            flag="test_flag",
            flag_id="flag_123",
            reason="rule_match",
            rule_id="rule_123",
            rule_type=None,
            user_id=None,
        )
        self.schematic.features.check_flag = MagicMock(
            return_value=MagicMock(data=mock_data)
        )

        # First call populates cache
        result1 = self.schematic.check_flag_with_entitlement("test_flag")
        self.assertEqual(result1.company_id, "comp_123")

        # Second call should hit cache
        result2 = self.schematic.check_flag_with_entitlement("test_flag")
        self.assertEqual(result2.company_id, "comp_123")

        # API should only have been called once
        self.schematic.features.check_flag.assert_called_once()

    def test_identify(self):
        with patch.object(self.schematic.event_buffer, "push") as mock_push:
            self.schematic.identify(
                keys={"id": "user_id"},
                name="User Name",
            )
            mock_push.assert_called_once()

    def test_track(self):
        with patch.object(self.schematic.event_buffer, "push") as mock_push:
            self.schematic.track(
                event="some-event",
                company={"id": "company_id"},
                user={"id": "user_id"},
            )
            mock_push.assert_called_once()

    def test_track_with_quantity(self):
        with patch.object(self.schematic.event_buffer, "push") as mock_push:
            self.schematic.track(
                event="api-call",
                company={"id": "company_id"},
                quantity=5,
            )
            mock_push.assert_called_once()

    def test_check_flag_with_no_cache(self):
        """Verify that when cache_providers is empty, every call hits the API."""
        config = SchematicConfig(
            event_buffer_period=1,
            logger=MagicMock(),
            httpx_client=MagicMock(spec=Client),
            cache_providers=[],
        )
        client = Schematic("api_key", config)
        try:
            mock_data = CheckFlagResponseData(
                value=True,
                flag="test_flag",
                reason="match",
            )
            client.features.check_flag = MagicMock(
                return_value=MagicMock(data=mock_data)
            )

            result1 = client.check_flag("test_flag")
            result2 = client.check_flag("test_flag")
            self.assertTrue(result1)
            self.assertTrue(result2)
            self.assertEqual(client.features.check_flag.call_count, 2)
        finally:
            client.event_buffer.stop()

    def test_check_flag_with_cache_ttl_expiry(self):
        """Verify cache expires after TTL."""
        short_ttl_cache = LocalCache(max_size=1000, ttl=50)  # 50ms TTL
        config = SchematicConfig(
            event_buffer_period=1,
            logger=MagicMock(),
            httpx_client=MagicMock(spec=Client),
            cache_providers=[short_ttl_cache],
        )
        client = Schematic("api_key", config)
        try:
            mock_data = CheckFlagResponseData(
                value=True,
                flag="test_flag",
                reason="match",
            )
            client.features.check_flag = MagicMock(
                return_value=MagicMock(data=mock_data)
            )

            # First call hits API and caches
            self.assertTrue(client.check_flag("test_flag"))
            # Second call should hit cache
            self.assertTrue(client.check_flag("test_flag"))
            self.assertEqual(client.features.check_flag.call_count, 1)

            # Wait for TTL to expire
            time.sleep(0.1)

            # Third call should miss cache and hit API again
            self.assertTrue(client.check_flag("test_flag"))
            self.assertEqual(client.features.check_flag.call_count, 2)
        finally:
            client.event_buffer.stop()

    def test_check_flag_returns_default_on_api_error(self):
        """Verify that API errors return the flag default value."""
        self.schematic.flag_defaults = {"test_flag": True}
        self.schematic.flag_check_cache_providers = []
        self.schematic.features.check_flag = MagicMock(
            side_effect=Exception("api error")
        )
        result = self.schematic.check_flag("test_flag")
        self.assertTrue(result)

    def test_check_flag_returns_false_on_error_no_default(self):
        """Verify that API errors with no default return False."""
        self.schematic.flag_check_cache_providers = []
        self.schematic.features.check_flag = MagicMock(
            side_effect=Exception("connection refused")
        )
        result = self.schematic.check_flag("test_flag")
        self.assertFalse(result)

    def test_check_flag_offline_no_default(self):
        """Verify that offline mode with no default returns False."""
        self.schematic.offline = True
        result = self.schematic.check_flag("test_flag")
        self.assertFalse(result)

    def test_check_flag_with_company_context_only(self):
        """Verify flag check passes company context correctly."""
        self.schematic.flag_check_cache_providers = []
        mock_data = CheckFlagResponseData(
            value=True,
            flag="test_flag",
            reason="match",
        )
        self.schematic.features.check_flag = MagicMock(
            return_value=MagicMock(data=mock_data)
        )
        result = self.schematic.check_flag(
            "test_flag",
            company={"company-id": "comp-123"},
        )
        self.assertTrue(result)
        call_kwargs = self.schematic.features.check_flag.call_args
        self.assertEqual(call_kwargs.kwargs["company"], {"company-id": "comp-123"})
        self.assertIsNone(call_kwargs.kwargs["user"])

    def test_check_flag_with_user_context_only(self):
        """Verify flag check passes user context correctly."""
        self.schematic.flag_check_cache_providers = []
        mock_data = CheckFlagResponseData(
            value=True,
            flag="test_flag",
            reason="match",
        )
        self.schematic.features.check_flag = MagicMock(
            return_value=MagicMock(data=mock_data)
        )
        result = self.schematic.check_flag(
            "test_flag",
            user={"user-id": "user-123"},
        )
        self.assertTrue(result)
        call_kwargs = self.schematic.features.check_flag.call_args
        self.assertIsNone(call_kwargs.kwargs["company"])
        self.assertEqual(call_kwargs.kwargs["user"], {"user-id": "user-123"})

    def test_check_flag_with_both_contexts(self):
        """Verify flag check passes both company and user context."""
        self.schematic.flag_check_cache_providers = []
        mock_data = CheckFlagResponseData(
            value=True,
            flag="test_flag",
            reason="match",
        )
        self.schematic.features.check_flag = MagicMock(
            return_value=MagicMock(data=mock_data)
        )
        result = self.schematic.check_flag(
            "test_flag",
            company={"company-id": "comp-123"},
            user={"user-id": "user-123"},
        )
        self.assertTrue(result)
        call_kwargs = self.schematic.features.check_flag.call_args
        self.assertEqual(call_kwargs.kwargs["company"], {"company-id": "comp-123"})
        self.assertEqual(call_kwargs.kwargs["user"], {"user-id": "user-123"})

    def test_check_flag_with_entitlement_nil_entitlement(self):
        """Verify handling of API response with no entitlement."""
        self.schematic.flag_check_cache_providers = []
        mock_data = CheckFlagResponseData(
            value=False,
            flag="test_flag",
            reason="no matching rules",
            entitlement=None,
            rule_type=None,
        )
        self.schematic.features.check_flag = MagicMock(
            return_value=MagicMock(data=mock_data)
        )
        result = self.schematic.check_flag_with_entitlement("test_flag")
        self.assertIsInstance(result, CheckFlagResponseData)
        self.assertFalse(result.value)
        self.assertIsNone(result.entitlement)
        self.assertIsNone(result.rule_type)

    def test_check_flag_with_entitlement_cache_preserves_entitlement(self):
        """Verify cache hit preserves full entitlement data."""
        entitlement = FeatureEntitlement(
            feature_id="feat-123",
            feature_key="test-feature",
            value_type="numeric",
            allocation=100,
            usage=50,
        )
        mock_data = CheckFlagResponseData(
            value=True,
            flag="test_flag",
            reason="entitlement matched",
            company_id="comp-123",
            flag_id="flag-456",
            rule_id="rule-789",
            rule_type="plan_entitlement",
            user_id="user-321",
            entitlement=entitlement,
        )
        self.schematic.features.check_flag = MagicMock(
            return_value=MagicMock(data=mock_data)
        )

        # First call hits API
        result1 = self.schematic.check_flag_with_entitlement("test_flag")
        self.assertTrue(result1.value)
        self.assertIsNotNone(result1.entitlement)
        self.assertEqual(result1.entitlement.feature_id, "feat-123")

        # Second call should hit cache and preserve entitlement
        result2 = self.schematic.check_flag_with_entitlement("test_flag")
        self.assertTrue(result2.value)
        self.assertEqual(result2.reason, "entitlement matched")
        self.assertEqual(result2.company_id, "comp-123")
        self.assertEqual(result2.flag_id, "flag-456")
        self.assertEqual(result2.rule_id, "rule-789")
        self.assertEqual(result2.rule_type, "plan_entitlement")
        self.assertEqual(result2.user_id, "user-321")
        self.assertIsNotNone(result2.entitlement)
        self.assertEqual(result2.entitlement.feature_id, "feat-123")
        self.assertEqual(result2.entitlement.feature_key, "test-feature")
        self.assertEqual(result2.entitlement.allocation, 100)

        # API should only have been called once
        self.schematic.features.check_flag.assert_called_once()

    def test_check_flag_with_entitlement_reason_strings(self):
        """Corresponds to Go TestCheckFlagWithEntitlement_ReasonStrings.

        Verify that reason, rule_type, and other string fields are preserved.
        """
        self.schematic.flag_check_cache_providers = []
        mock_data = CheckFlagResponseData(
            value=True,
            flag="test_flag",
            reason="match",
            company_id="comp-123",
            flag_id="flag-456",
            rule_id="rule-789",
            rule_type="override",
            entitlement=None,
        )
        self.schematic.features.check_flag = MagicMock(
            return_value=MagicMock(data=mock_data)
        )
        result = self.schematic.check_flag_with_entitlement(
            "test_flag",
            company={"company-id": "comp-123"},
        )
        self.assertIsInstance(result, CheckFlagResponseData)
        self.assertTrue(result.value)
        self.assertEqual(result.reason, "match")
        self.assertEqual(result.company_id, "comp-123")
        self.assertEqual(result.flag_id, "flag-456")
        self.assertEqual(result.rule_id, "rule-789")
        self.assertEqual(result.rule_type, "override")
        self.assertIsNone(result.entitlement)

    def tearDown(self):
        self.schematic.event_buffer.stop()


@pytest.mark.asyncio
class TestAsyncSchematic:

    @pytest.fixture(autouse=True)
    async def setup_and_teardown(self):
        config = AsyncSchematicConfig(
            logger=MagicMock(),
            httpx_client=MagicMock(spec=AsyncClient),
            event_buffer_period=1,
        )
        self.async_schematic = AsyncSchematic("test_key", config)
        yield
        await self.async_schematic.event_buffer.stop()

    async def test_check_flag_offline(self):
        self.async_schematic.offline = True
        self.async_schematic.flag_defaults = {"test_flag": True}
        result = await self.async_schematic.check_flag(
            "test_flag",
            company={"id": "company_id"},
            user={"id": "user_id"},
        )
        assert result

    async def test_check_flag_online(self):
        self.async_schematic.offline = False
        self.async_schematic.flag_defaults = {"test_flag": True}
        self.async_schematic.features.check_flag = MagicMock(
            return_value=MagicMock(data=MagicMock(value=True))
        )
        result = await self.async_schematic.check_flag(
            "test_flag",
            company={"id": "company_id"},
            user={"id": "user_id"},
        )
        assert result

    async def test_check_flag_with_entitlement_offline(self):
        self.async_schematic.offline = True
        self.async_schematic.flag_defaults = {"test_flag": True}
        result = await self.async_schematic.check_flag_with_entitlement(
            "test_flag",
            company={"id": "company_id"},
        )
        assert isinstance(result, CheckFlagResponseData)
        assert result.value is True
        assert result.flag == "test_flag"
        assert result.reason == "flag default"

    async def test_check_flag_with_entitlement_online(self):
        self.async_schematic.offline = False
        mock_data = CheckFlagResponseData(
            value=True,
            company_id="comp_123",
            entitlement=None,
            error=None,
            flag="test_flag",
            flag_id="flag_123",
            reason="rule_match",
            rule_id="rule_123",
            rule_type="override",
            user_id="user_123",
        )
        self.async_schematic.features.check_flag = AsyncMock(
            return_value=MagicMock(data=mock_data)
        )
        result = await self.async_schematic.check_flag_with_entitlement(
            "test_flag",
            company={"id": "company_id"},
        )
        assert isinstance(result, CheckFlagResponseData)
        assert result.value is True
        assert result.company_id == "comp_123"
        assert result.reason == "rule_match"

    async def test_check_flag_with_options(self):
        self.async_schematic.offline = True
        options = CheckFlagOptions(default_value=True)
        result = await self.async_schematic.check_flag("missing_flag", options=options)
        assert result is True

    async def test_identify(self):
        with patch.object(self.async_schematic.event_buffer, "push") as mock_push:
            await self.async_schematic.identify(
                keys={"id": "user_id"},
                name="User Name",
            )
            mock_push.assert_called_once()

    async def test_track(self):
        with patch.object(self.async_schematic.event_buffer, "push") as mock_push:
            await self.async_schematic.track(
                event="some-event",
                company={"id": "company_id"},
                user={"id": "user_id"},
            )
            mock_push.assert_called_once()

    async def test_check_flag_with_no_cache(self):
        """Verify that when cache_providers is empty, every call hits the API."""
        config = AsyncSchematicConfig(
            event_buffer_period=1,
            logger=MagicMock(),
            httpx_client=MagicMock(spec=AsyncClient),
            cache_providers=[],
        )
        client = AsyncSchematic("test_key", config)
        try:
            mock_data = CheckFlagResponseData(
                value=True,
                flag="test_flag",
                reason="match",
            )
            client.features.check_flag = AsyncMock(
                return_value=MagicMock(data=mock_data)
            )

            result1 = await client.check_flag("test_flag")
            result2 = await client.check_flag("test_flag")
            assert result1 is True
            assert result2 is True
            assert client.features.check_flag.call_count == 2
        finally:
            await client.event_buffer.stop()

    async def test_check_flag_returns_default_on_api_error(self):
        """Verify that API errors return the flag default value."""
        self.async_schematic.flag_defaults = {"test_flag": True}
        self.async_schematic.flag_check_cache_providers = []
        self.async_schematic.features.check_flag = AsyncMock(
            side_effect=Exception("api error")
        )
        result = await self.async_schematic.check_flag("test_flag")
        assert result is True

    async def test_check_flag_returns_false_on_error_no_default(self):
        """Verify that API errors with no default return False."""
        self.async_schematic.flag_check_cache_providers = []
        self.async_schematic.features.check_flag = AsyncMock(
            side_effect=Exception("connection refused")
        )
        result = await self.async_schematic.check_flag("test_flag")
        assert result is False

    async def test_check_flag_offline_no_default(self):
        """Verify that offline mode with no default returns False."""
        self.async_schematic.offline = True
        result = await self.async_schematic.check_flag("test_flag")
        assert result is False

    async def test_check_flag_with_company_context_only(self):
        """Verify flag check passes company context correctly."""
        self.async_schematic.flag_check_cache_providers = []
        mock_data = CheckFlagResponseData(
            value=True,
            flag="test_flag",
            reason="match",
        )
        self.async_schematic.features.check_flag = AsyncMock(
            return_value=MagicMock(data=mock_data)
        )
        result = await self.async_schematic.check_flag(
            "test_flag",
            company={"company-id": "comp-123"},
        )
        assert result is True
        call_kwargs = self.async_schematic.features.check_flag.call_args
        assert call_kwargs.kwargs["company"] == {"company-id": "comp-123"}
        assert call_kwargs.kwargs["user"] is None

    async def test_check_flag_with_user_context_only(self):
        """Verify flag check passes user context correctly."""
        self.async_schematic.flag_check_cache_providers = []
        mock_data = CheckFlagResponseData(
            value=True,
            flag="test_flag",
            reason="match",
        )
        self.async_schematic.features.check_flag = AsyncMock(
            return_value=MagicMock(data=mock_data)
        )
        result = await self.async_schematic.check_flag(
            "test_flag",
            user={"user-id": "user-123"},
        )
        assert result is True
        call_kwargs = self.async_schematic.features.check_flag.call_args
        assert call_kwargs.kwargs["company"] is None
        assert call_kwargs.kwargs["user"] == {"user-id": "user-123"}

    async def test_check_flag_with_both_contexts(self):
        """Verify flag check passes both company and user context."""
        self.async_schematic.flag_check_cache_providers = []
        mock_data = CheckFlagResponseData(
            value=True,
            flag="test_flag",
            reason="match",
        )
        self.async_schematic.features.check_flag = AsyncMock(
            return_value=MagicMock(data=mock_data)
        )
        result = await self.async_schematic.check_flag(
            "test_flag",
            company={"company-id": "comp-123"},
            user={"user-id": "user-123"},
        )
        assert result is True
        call_kwargs = self.async_schematic.features.check_flag.call_args
        assert call_kwargs.kwargs["company"] == {"company-id": "comp-123"}
        assert call_kwargs.kwargs["user"] == {"user-id": "user-123"}

    async def test_check_flag_with_entitlement_nil_entitlement(self):
        """Verify handling of API response with no entitlement."""
        self.async_schematic.flag_check_cache_providers = []
        mock_data = CheckFlagResponseData(
            value=False,
            flag="test_flag",
            reason="no matching rules",
            entitlement=None,
            rule_type=None,
        )
        self.async_schematic.features.check_flag = AsyncMock(
            return_value=MagicMock(data=mock_data)
        )
        result = await self.async_schematic.check_flag_with_entitlement("test_flag")
        assert isinstance(result, CheckFlagResponseData)
        assert result.value is False
        assert result.entitlement is None
        assert result.rule_type is None

    async def test_check_flag_with_entitlement_cache_preserves_entitlement(self):
        """Verify cache hit preserves full entitlement data."""
        entitlement = FeatureEntitlement(
            feature_id="feat-123",
            feature_key="test-feature",
            value_type="numeric",
            allocation=100,
            usage=50,
        )
        mock_data = CheckFlagResponseData(
            value=True,
            flag="test_flag",
            reason="entitlement matched",
            company_id="comp-123",
            flag_id="flag-456",
            rule_id="rule-789",
            rule_type="plan_entitlement",
            user_id="user-321",
            entitlement=entitlement,
        )
        self.async_schematic.features.check_flag = AsyncMock(
            return_value=MagicMock(data=mock_data)
        )

        # First call hits API
        result1 = await self.async_schematic.check_flag_with_entitlement("test_flag")
        assert result1.value is True
        assert result1.entitlement is not None
        assert result1.entitlement.feature_id == "feat-123"

        # Second call should hit cache and preserve entitlement
        result2 = await self.async_schematic.check_flag_with_entitlement("test_flag")
        assert result2.value is True
        assert result2.reason == "entitlement matched"
        assert result2.company_id == "comp-123"
        assert result2.flag_id == "flag-456"
        assert result2.rule_id == "rule-789"
        assert result2.rule_type == "plan_entitlement"
        assert result2.user_id == "user-321"
        assert result2.entitlement is not None
        assert result2.entitlement.feature_id == "feat-123"
        assert result2.entitlement.feature_key == "test-feature"
        assert result2.entitlement.allocation == 100

        # API should only have been called once
        self.async_schematic.features.check_flag.assert_called_once()

    async def test_check_flag_with_entitlement_reason_strings(self):
        """Corresponds to Go TestCheckFlagWithEntitlement_ReasonStrings (async)."""
        self.async_schematic.flag_check_cache_providers = []
        mock_data = CheckFlagResponseData(
            value=True,
            flag="test_flag",
            reason="match",
            company_id="comp-123",
            flag_id="flag-456",
            rule_id="rule-789",
            rule_type="override",
            entitlement=None,
        )
        self.async_schematic.features.check_flag = AsyncMock(
            return_value=MagicMock(data=mock_data)
        )
        result = await self.async_schematic.check_flag_with_entitlement(
            "test_flag",
            company={"company-id": "comp-123"},
        )
        assert isinstance(result, CheckFlagResponseData)
        assert result.value is True
        assert result.reason == "match"
        assert result.company_id == "comp-123"
        assert result.flag_id == "flag-456"
        assert result.rule_id == "rule-789"
        assert result.rule_type == "override"
        assert result.entitlement is None

    async def test_check_flag_datastream_fallback_to_api(self):
        """Corresponds to Go TestCheckFlagDatastreamFallbackToAPI.

        When datastream is configured but fails, should fall back to API.
        """
        config = AsyncSchematicConfig(
            logger=MagicMock(),
            httpx_client=MagicMock(spec=AsyncClient),
            event_buffer_period=1,
            use_datastream=True,
        )
        client = AsyncSchematic("test_key", config)
        try:
            # Mock the datastream client to raise an error
            mock_ds = MagicMock()
            mock_ds.check_flag = AsyncMock(side_effect=Exception("datastream failed"))
            client._datastream_client = mock_ds

            # Mock the API to return a valid response
            mock_data = CheckFlagResponseData(
                value=True,
                flag="test_flag",
                reason="match",
            )
            client.features.check_flag = AsyncMock(
                return_value=MagicMock(data=mock_data)
            )
            client.flag_check_cache_providers = []

            result = await client.check_flag("test_flag", company={"id": "test-company"})
            assert result is True

            # API should have been called as fallback
            client.features.check_flag.assert_called_once()
        finally:
            await client.event_buffer.stop()


if __name__ == "__main__":
    unittest.main()
