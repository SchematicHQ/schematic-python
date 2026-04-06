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
    FlagCheck,
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

    def test_check_flags_offline_uses_defaults(self):
        self.schematic.offline = True
        self.schematic.flag_defaults = {"flag_a": True, "flag_b": False}
        results = self.schematic.check_flags(
            ["flag_a", "flag_b", "flag_c"],
            company={"id": "company_id"},
        )
        self.assertEqual(len(results), 3)
        self.assertTrue(all(isinstance(r, FlagCheck) for r in results))
        self.assertEqual([r.flag for r in results], ["flag_a", "flag_b", "flag_c"])
        self.assertEqual([r.value for r in results], [True, False, False])
        self.assertEqual(results[0].reason, "flag default")

    def test_check_flags_returns_values_for_each_key(self):
        self.schematic.offline = False
        self.schematic.flag_check_cache_providers = []

        def fake_check_flag(flag_key, company=None, user=None):
            return MagicMock(data=CheckFlagResponseData(
                value=(flag_key == "enabled_flag"),
                flag=flag_key,
                reason="match",
            ))

        self.schematic.features.check_flag = MagicMock(side_effect=fake_check_flag)
        results = self.schematic.check_flags(
            ["enabled_flag", "disabled_flag"],
            company={"id": "company_id"},
        )
        self.assertEqual(
            [(r.flag, r.value, r.reason) for r in results],
            [("enabled_flag", True, "match"), ("disabled_flag", False, "match")],
        )
        self.assertEqual(self.schematic.features.check_flag.call_count, 2)

    def test_check_flags_includes_missing_flags_with_default(self):
        """Flags that don't exist should be included with the default value."""
        self.schematic.offline = False
        self.schematic.flag_check_cache_providers = []
        self.schematic.flag_defaults = {"missing_flag": True}

        def fake_check_flag(flag_key, company=None, user=None):
            if flag_key == "missing_flag":
                return MagicMock(data=MagicMock(value=None))
            return MagicMock(data=CheckFlagResponseData(value=True, flag=flag_key, reason="match"))

        self.schematic.features.check_flag = MagicMock(side_effect=fake_check_flag)
        results = self.schematic.check_flags(
            ["real_flag", "missing_flag", "another_real_flag"],
        )
        self.assertEqual(
            [r.flag for r in results],
            ["real_flag", "missing_flag", "another_real_flag"],
        )
        self.assertEqual([r.value for r in results], [True, True, True])
        # missing_flag uses the default with reason "flag default"
        self.assertEqual(results[1].reason, "flag default")

    def test_check_flags_uses_cache(self):
        """Cached values should be returned without calling the API."""
        self.schematic.offline = False
        mock_data = CheckFlagResponseData(value=True, flag="flag_a", reason="match")
        self.schematic.features.check_flag = MagicMock(
            return_value=MagicMock(data=mock_data)
        )

        # Prime cache
        self.schematic.check_flag("flag_a")
        self.schematic.features.check_flag.reset_mock()

        results = self.schematic.check_flags(["flag_a"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].flag, "flag_a")
        self.assertTrue(results[0].value)
        self.schematic.features.check_flag.assert_not_called()

    def test_check_flags_uses_default_on_error(self):
        """API errors should fall back to the flag default value."""
        self.schematic.offline = False
        self.schematic.flag_check_cache_providers = []
        self.schematic.flag_defaults = {"flag_a": True}
        self.schematic.features.check_flag = MagicMock(
            side_effect=Exception("api error")
        )
        results = self.schematic.check_flags(["flag_a", "flag_b"])
        self.assertEqual([r.flag for r in results], ["flag_a", "flag_b"])
        self.assertEqual([r.value for r in results], [True, False])

    def test_check_flags_with_entitlement_returns_full_response(self):
        self.schematic.offline = False
        self.schematic.flag_check_cache_providers = []

        def fake_check_flag(flag_key, company=None, user=None):
            return MagicMock(data=CheckFlagResponseData(
                value=True,
                flag=flag_key,
                reason="rule_match",
                rule_id=f"rule_{flag_key}",
                company_id="comp_123",
            ))

        self.schematic.features.check_flag = MagicMock(side_effect=fake_check_flag)
        results = self.schematic.check_flags_with_entitlement(
            ["flag_a", "flag_b"],
            company={"id": "company_id"},
        )
        self.assertEqual([r.flag for r in results], ["flag_a", "flag_b"])
        self.assertTrue(all(isinstance(r, CheckFlagResponseData) for r in results))
        self.assertEqual(results[0].rule_id, "rule_flag_a")
        self.assertEqual(results[1].rule_id, "rule_flag_b")
        self.assertEqual(results[0].company_id, "comp_123")

    def test_check_flags_with_entitlement_includes_missing_flags(self):
        self.schematic.offline = False
        self.schematic.flag_check_cache_providers = []

        def fake_check_flag(flag_key, company=None, user=None):
            if flag_key == "missing_flag":
                return MagicMock(data=MagicMock(value=None))
            return MagicMock(data=CheckFlagResponseData(
                value=True, flag=flag_key, reason="match",
            ))

        self.schematic.features.check_flag = MagicMock(side_effect=fake_check_flag)
        results = self.schematic.check_flags_with_entitlement(
            ["real_flag", "missing_flag"],
        )
        self.assertEqual([r.flag for r in results], ["real_flag", "missing_flag"])
        self.assertEqual(results[1].reason, "flag default")
        self.assertFalse(results[1].value)

    def test_check_flags_with_entitlement_offline(self):
        self.schematic.offline = True
        self.schematic.flag_defaults = {"flag_a": True}
        results = self.schematic.check_flags_with_entitlement(["flag_a", "flag_b"])
        self.assertEqual([r.flag for r in results], ["flag_a", "flag_b"])
        self.assertTrue(results[0].value)
        self.assertEqual(results[0].reason, "flag default")
        self.assertFalse(results[1].value)

    def test_check_flags_delegates_to_with_entitlement(self):
        """check_flags should return slim FlagCheck objects derived from check_flags_with_entitlement."""
        self.schematic.offline = True
        self.schematic.flag_defaults = {"flag_a": True, "flag_b": False}
        slim = self.schematic.check_flags(["flag_a", "flag_b"])
        full = self.schematic.check_flags_with_entitlement(["flag_a", "flag_b"])
        self.assertEqual(
            [(r.flag, r.value, r.reason) for r in slim],
            [(r.flag, r.value, r.reason) for r in full],
        )

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

    async def test_check_flag_datastream_local_evaluation_skips_api(self):
        """Spec checklist item 13: when DataStream is connected and evaluates
        successfully, the API check_flag must NOT be called.

        This is the happy-path counterpart to test_check_flag_datastream_fallback_to_api.
        """
        from schematic.types import RulesengineCheckFlagResult

        config = AsyncSchematicConfig(
            logger=MagicMock(),
            httpx_client=MagicMock(spec=AsyncClient),
            event_buffer_period=1,
            use_datastream=True,
        )
        client = AsyncSchematic("test_key", config)
        try:
            ds_result = RulesengineCheckFlagResult(
                value=True,
                flag_key="test_flag",
                flag_id="flag-1",
                reason="match",
                rule_id="rule-1",
                rule_type="override",
                company_id="comp-1",
            )
            mock_ds = MagicMock()
            mock_ds.check_flag = AsyncMock(return_value=ds_result)
            client._datastream_client = mock_ds

            client.features.check_flag = AsyncMock()  # should not be called

            result = await client.check_flag("test_flag", company={"id": "comp-1"})
            assert result is True

            mock_ds.check_flag.assert_called_once()
            client.features.check_flag.assert_not_called()
        finally:
            await client.event_buffer.stop()

    async def test_check_flag_falls_back_to_api_when_flag_not_in_datastream_cache(self):
        """Spec checklist item 9 (DataStream): when the requested flag is not
        cached locally by the DataStream client, the wrapper must fall back
        to a direct API call rather than returning the default.
        """
        config = AsyncSchematicConfig(
            logger=MagicMock(),
            httpx_client=MagicMock(spec=AsyncClient),
            event_buffer_period=1,
            use_datastream=True,
        )
        client = AsyncSchematic("test_key", config)
        try:
            # DataStream raises the same error its real check_flag raises when
            # the flag is missing from the local cache.
            mock_ds = MagicMock()
            mock_ds.check_flag = AsyncMock(
                side_effect=RuntimeError("Flag not found: test_flag")
            )
            client._datastream_client = mock_ds

            mock_data = CheckFlagResponseData(
                value=True,
                flag="test_flag",
                reason="match",
            )
            client.features.check_flag = AsyncMock(
                return_value=MagicMock(data=mock_data)
            )
            client.flag_check_cache_providers = []

            result = await client.check_flag("test_flag", company={"id": "co-1"})
            assert result is True

            mock_ds.check_flag.assert_called_once()
            client.features.check_flag.assert_called_once()
        finally:
            await client.event_buffer.stop()

    async def test_offline_mode_drops_events_silently(self):
        """Spec §Offline Mode + §Event Submission: events submitted while offline
        must be silently dropped, not queued.
        """
        self.async_schematic.offline = True
        with patch.object(self.async_schematic.event_buffer, "push") as mock_push:
            await self.async_schematic.identify(keys={"id": "user_id"})
            await self.async_schematic.track(
                event="some-event",
                company={"id": "company_id"},
            )
            mock_push.assert_not_called()

    async def test_check_flags_offline_uses_defaults(self):
        self.async_schematic.offline = True
        self.async_schematic.flag_defaults = {"flag_a": True, "flag_b": False}
        results = await self.async_schematic.check_flags(
            ["flag_a", "flag_b", "flag_c"],
            company={"id": "company_id"},
        )
        assert all(isinstance(r, FlagCheck) for r in results)
        assert [r.flag for r in results] == ["flag_a", "flag_b", "flag_c"]
        assert [r.value for r in results] == [True, False, False]

    async def test_check_flags_returns_values_for_each_key(self):
        self.async_schematic.offline = False
        self.async_schematic.flag_check_cache_providers = []

        def fake_check_flag(flag_key, company=None, user=None):
            return MagicMock(data=CheckFlagResponseData(
                value=(flag_key == "enabled_flag"),
                flag=flag_key,
                reason="match",
            ))

        self.async_schematic.features.check_flag = AsyncMock(side_effect=fake_check_flag)
        results = await self.async_schematic.check_flags(
            ["enabled_flag", "disabled_flag"],
        )
        assert [(r.flag, r.value, r.reason) for r in results] == [
            ("enabled_flag", True, "match"),
            ("disabled_flag", False, "match"),
        ]
        assert self.async_schematic.features.check_flag.call_count == 2

    async def test_check_flags_includes_missing_flags_with_default(self):
        """Flags that don't exist should be included with the default value."""
        self.async_schematic.offline = False
        self.async_schematic.flag_check_cache_providers = []
        self.async_schematic.flag_defaults = {"missing_flag": True}

        def fake_check_flag(flag_key, company=None, user=None):
            if flag_key == "missing_flag":
                return MagicMock(data=MagicMock(value=None))
            return MagicMock(data=CheckFlagResponseData(value=True, flag=flag_key, reason="match"))

        self.async_schematic.features.check_flag = AsyncMock(side_effect=fake_check_flag)
        results = await self.async_schematic.check_flags(
            ["real_flag", "missing_flag", "another_real_flag"],
        )
        assert [r.flag for r in results] == ["real_flag", "missing_flag", "another_real_flag"]
        assert [r.value for r in results] == [True, True, True]
        assert results[1].reason == "flag default"

    async def test_check_flags_uses_default_on_error(self):
        """API errors should fall back to the flag default value."""
        self.async_schematic.offline = False
        self.async_schematic.flag_check_cache_providers = []
        self.async_schematic.flag_defaults = {"flag_a": True}
        self.async_schematic.features.check_flag = AsyncMock(
            side_effect=Exception("api error")
        )
        results = await self.async_schematic.check_flags(["flag_a", "flag_b"])
        assert [r.flag for r in results] == ["flag_a", "flag_b"]
        assert [r.value for r in results] == [True, False]

    async def test_check_flags_with_entitlement_returns_full_response(self):
        self.async_schematic.offline = False
        self.async_schematic.flag_check_cache_providers = []

        def fake_check_flag(flag_key, company=None, user=None):
            return MagicMock(data=CheckFlagResponseData(
                value=True,
                flag=flag_key,
                reason="rule_match",
                rule_id=f"rule_{flag_key}",
                company_id="comp_123",
            ))

        self.async_schematic.features.check_flag = AsyncMock(side_effect=fake_check_flag)
        results = await self.async_schematic.check_flags_with_entitlement(
            ["flag_a", "flag_b"],
            company={"id": "company_id"},
        )
        assert [r.flag for r in results] == ["flag_a", "flag_b"]
        assert all(isinstance(r, CheckFlagResponseData) for r in results)
        assert results[0].rule_id == "rule_flag_a"
        assert results[1].rule_id == "rule_flag_b"
        assert results[0].company_id == "comp_123"

    async def test_check_flags_with_entitlement_includes_missing_flags(self):
        self.async_schematic.offline = False
        self.async_schematic.flag_check_cache_providers = []

        def fake_check_flag(flag_key, company=None, user=None):
            if flag_key == "missing_flag":
                return MagicMock(data=MagicMock(value=None))
            return MagicMock(data=CheckFlagResponseData(
                value=True, flag=flag_key, reason="match",
            ))

        self.async_schematic.features.check_flag = AsyncMock(side_effect=fake_check_flag)
        results = await self.async_schematic.check_flags_with_entitlement(
            ["real_flag", "missing_flag"],
        )
        assert [r.flag for r in results] == ["real_flag", "missing_flag"]
        assert results[1].reason == "flag default"
        assert results[1].value is False

    async def test_check_flags_with_entitlement_offline(self):
        self.async_schematic.offline = True
        self.async_schematic.flag_defaults = {"flag_a": True}
        results = await self.async_schematic.check_flags_with_entitlement(["flag_a", "flag_b"])
        assert [r.flag for r in results] == ["flag_a", "flag_b"]
        assert results[0].value is True
        assert results[0].reason == "flag default"
        assert results[1].value is False

    async def test_check_flags_delegates_to_with_entitlement(self):
        self.async_schematic.offline = True
        self.async_schematic.flag_defaults = {"flag_a": True, "flag_b": False}
        slim = await self.async_schematic.check_flags(["flag_a", "flag_b"])
        full = await self.async_schematic.check_flags_with_entitlement(["flag_a", "flag_b"])
        assert [(r.flag, r.value, r.reason) for r in slim] == [
            (r.flag, r.value, r.reason) for r in full
        ]


if __name__ == "__main__":
    unittest.main()
