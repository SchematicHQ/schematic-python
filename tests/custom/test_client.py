import asyncio
import datetime as dt
import json
import time
import unittest
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import AsyncClient, Client, MockTransport, Response
from lease_support import ScriptedDataStream, ScriptedEngine, make_fake_redis

from schematic.cache import LocalCache, RedisCache
from schematic.client import (
    INSUFFICIENT_CREDITS_REASON,
    MAX_RESERVATION_TTL,
    REASON_FLAG_NOT_FOUND,
    REASON_OFFLINE,
    RESERVATION_TTL_SKEW_ALLOWANCE,
    AsyncSchematic,
    AsyncSchematicConfig,
    CheckFlagOptions,
    CheckOptions,
    CreditLeaseConfig,
    DataStreamConfig,
    EventUsage,
    IdentifyOptions,
    Reservation,
    Schematic,
    SchematicConfig,
    TrackOptions,
    TrackWithReservationOptions,
    _is_valid_quantity,
)
from schematic.core import http_client as core_http_client
from schematic.core.api_error import ApiError as CoreApiError
from schematic.errors import PaymentRequiredError
from schematic.leases import LeaseConfigOverride
from schematic.types import (
    ApiError,
    CheckAndReserveFlagResponseData,
    CheckFlagResponseData,
    EventBodyIdentifyCompany,
    FeatureEntitlement,
    FlagCheckReservationResponseData,
    PreflightEventUsageRequestBody,
    PreflightRequestBody,
    RulesengineCheckFlagResult,
)


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
        self.assertEqual(result.reason, REASON_OFFLINE)

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

    def test_track_with_idempotency_key(self):
        """idempotency_key set via TrackOptions must land on the
        CreateEventRequestBody pushed to the event buffer so the server can
        dedupe on it."""
        with patch.object(self.schematic.event_buffer, "push") as mock_push:
            self.schematic.track(
                event="credit-consumed",
                company={"id": "company_id"},
                options=TrackOptions(idempotency_key="evt_abc123"),
            )
            mock_push.assert_called_once()
            pushed = mock_push.call_args.args[0]
            self.assertEqual(pushed.idempotency_key, "evt_abc123")

    def test_track_without_options_leaves_optional_fields_none(self):
        """Options are opt-in — omitting `options` must leave every optional
        metadata field at None on the wire."""
        with patch.object(self.schematic.event_buffer, "push") as mock_push:
            self.schematic.track(
                event="some-event",
                company={"id": "company_id"},
            )
            pushed = mock_push.call_args.args[0]
            self.assertIsNone(pushed.idempotency_key)
            self.assertIsNone(pushed.sent_at)
            self.assertIsNone(pushed.trusted_client_clock)
            self.assertIsNone(pushed.backfill)

    def test_track_with_full_options(self):
        """Every TrackOptions field should land on the CreateEventRequestBody."""
        import datetime as dt
        sent_at = dt.datetime(2026, 5, 21, 12, 0, 0, tzinfo=dt.timezone.utc)
        with patch.object(self.schematic.event_buffer, "push") as mock_push:
            self.schematic.track(
                event="historical-import",
                company={"id": "company_id"},
                options=TrackOptions(
                    idempotency_key="evt_xyz",
                    sent_at=sent_at,
                    trusted_client_clock=True,
                    backfill=True,
                ),
            )
            pushed = mock_push.call_args.args[0]
            self.assertEqual(pushed.idempotency_key, "evt_xyz")
            self.assertEqual(pushed.sent_at, sent_at)
            self.assertTrue(pushed.trusted_client_clock)
            self.assertTrue(pushed.backfill)

    def test_track_partial_options(self):
        """Unset TrackOptions fields stay None on the CreateEventRequestBody —
        we don't accidentally send explicit nulls for things the caller didn't ask for."""
        with patch.object(self.schematic.event_buffer, "push") as mock_push:
            self.schematic.track(
                event="some-event",
                company={"id": "company_id"},
                options=TrackOptions(idempotency_key="just-the-key"),
            )
            pushed = mock_push.call_args.args[0]
            self.assertEqual(pushed.idempotency_key, "just-the-key")
            self.assertIsNone(pushed.sent_at)
            self.assertIsNone(pushed.trusted_client_clock)
            self.assertIsNone(pushed.backfill)

    def test_identify_with_options(self):
        """IdentifyOptions must plumb through to the CreateEventRequestBody."""
        with patch.object(self.schematic.event_buffer, "push") as mock_push:
            self.schematic.identify(
                keys={"id": "user_id"},
                options=IdentifyOptions(idempotency_key="ident_123"),
            )
            pushed = mock_push.call_args.args[0]
            self.assertEqual(pushed.idempotency_key, "ident_123")

    def test_identify_without_options(self):
        """Existing identify callers without options keep working unchanged."""
        with patch.object(self.schematic.event_buffer, "push") as mock_push:
            self.schematic.identify(keys={"id": "user_id"}, name="User Name")
            pushed = mock_push.call_args.args[0]
            self.assertIsNone(pushed.idempotency_key)

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
        self.assertTrue(all(isinstance(r, CheckFlagResponseData) for r in results))
        self.assertEqual([r.flag for r in results], ["flag_a", "flag_b", "flag_c"])
        self.assertEqual([r.value for r in results], [True, False, False])
        self.assertEqual(results[0].reason, REASON_OFFLINE)

    def _bulk_response(self, flags):
        return MagicMock(data=MagicMock(flags=flags))

    def test_check_flags_uses_bulk_api_endpoint(self):
        """check_flags must call features.check_flags (bulk) not features.check_flag (single)."""
        self.schematic.offline = False
        self.schematic.flag_check_cache_providers = []

        bulk_resp = self._bulk_response([
            CheckFlagResponseData(value=True, flag="enabled_flag", reason="match"),
            CheckFlagResponseData(value=False, flag="disabled_flag", reason="match"),
        ])
        self.schematic.features.check_flags = MagicMock(return_value=bulk_resp)
        self.schematic.features.check_flag = MagicMock()

        results = self.schematic.check_flags(
            ["enabled_flag", "disabled_flag"],
            company={"id": "company_id"},
        )
        self.assertEqual([r.flag for r in results], ["enabled_flag", "disabled_flag"])
        self.assertEqual([r.value for r in results], [True, False])
        self.schematic.features.check_flags.assert_called_once_with(
            company={"id": "company_id"},
        )
        self.schematic.features.check_flag.assert_not_called()

    def test_check_flags_includes_missing_flags_with_default(self):
        """Flags absent from the bulk response should be filled in with defaults."""
        self.schematic.offline = False
        self.schematic.flag_check_cache_providers = []
        self.schematic.flag_defaults = {"missing_flag": True}

        bulk_resp = self._bulk_response([
            CheckFlagResponseData(value=True, flag="real_flag", reason="match"),
            CheckFlagResponseData(value=True, flag="another_real_flag", reason="match"),
        ])
        self.schematic.features.check_flags = MagicMock(return_value=bulk_resp)

        results = self.schematic.check_flags(
            ["real_flag", "missing_flag", "another_real_flag"],
        )
        self.assertEqual(
            [r.flag for r in results],
            ["real_flag", "missing_flag", "another_real_flag"],
        )
        self.assertEqual([r.value for r in results], [True, True, True])
        self.assertEqual(results[1].reason, REASON_FLAG_NOT_FOUND)

    def test_check_flags_uses_cache(self):
        """All-cache-hit should skip the bulk API call entirely."""
        self.schematic.offline = False
        mock_data = CheckFlagResponseData(value=True, flag="flag_a", reason="match")
        self.schematic.features.check_flag = MagicMock(
            return_value=MagicMock(data=mock_data)
        )
        self.schematic.features.check_flags = MagicMock()

        # Prime cache via single check_flag
        self.schematic.check_flag("flag_a")
        self.schematic.features.check_flag.reset_mock()

        results = self.schematic.check_flags(["flag_a"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].flag, "flag_a")
        self.assertTrue(results[0].value)
        self.schematic.features.check_flag.assert_not_called()
        self.schematic.features.check_flags.assert_not_called()

    def test_check_flags_partial_cache_miss_calls_bulk_api(self):
        """If any requested key isn't cached, the bulk API is called and
        cached values are merged with the fresh bulk results."""
        self.schematic.offline = False

        # Prime cache for flag_a only
        self.schematic.features.check_flag = MagicMock(
            return_value=MagicMock(data=CheckFlagResponseData(
                value=True, flag="flag_a", reason="match",
            ))
        )
        self.schematic.check_flag("flag_a")

        # Bulk API returns both flags fresh
        self.schematic.features.check_flags = MagicMock(return_value=self._bulk_response([
            CheckFlagResponseData(value=False, flag="flag_a", reason="match"),
            CheckFlagResponseData(value=True, flag="flag_b", reason="match"),
        ]))

        results = self.schematic.check_flags(["flag_a", "flag_b"])
        # Bulk API is called because flag_b is not cached
        self.schematic.features.check_flags.assert_called_once()
        # Fresh bulk values take precedence over the stale cached entry
        self.assertEqual([r.value for r in results], [False, True])

    def test_check_flags_uses_default_on_error(self):
        """Bulk API errors should fall back to per-key flag defaults."""
        self.schematic.offline = False
        self.schematic.flag_check_cache_providers = []
        self.schematic.flag_defaults = {"flag_a": True}
        self.schematic.features.check_flags = MagicMock(
            side_effect=Exception("api error")
        )
        results = self.schematic.check_flags(["flag_a", "flag_b"])
        self.assertEqual([r.flag for r in results], ["flag_a", "flag_b"])
        self.assertEqual([r.value for r in results], [True, False])

    def test_check_flags_returns_full_response_data(self):
        self.schematic.offline = False
        self.schematic.flag_check_cache_providers = []

        bulk_resp = self._bulk_response([
            CheckFlagResponseData(
                value=True, flag="flag_a", reason="rule_match",
                rule_id="rule_flag_a", company_id="comp_123",
            ),
            CheckFlagResponseData(
                value=True, flag="flag_b", reason="rule_match",
                rule_id="rule_flag_b", company_id="comp_123",
            ),
        ])
        self.schematic.features.check_flags = MagicMock(return_value=bulk_resp)

        results = self.schematic.check_flags(
            ["flag_a", "flag_b"],
            company={"id": "company_id"},
        )
        self.assertEqual([r.flag for r in results], ["flag_a", "flag_b"])
        self.assertTrue(all(isinstance(r, CheckFlagResponseData) for r in results))
        self.assertEqual(results[0].rule_id, "rule_flag_a")
        self.assertEqual(results[1].rule_id, "rule_flag_b")
        self.assertEqual(results[0].company_id, "comp_123")

    def test_check_flags_with_no_keys_returns_all_flags(self):
        """No keys passed → call bulk API and return every flag for the context."""
        self.schematic.offline = False
        self.schematic.flag_check_cache_providers = []

        bulk_resp = self._bulk_response([
            CheckFlagResponseData(value=True, flag="flag_a", reason="match"),
            CheckFlagResponseData(value=False, flag="flag_b", reason="match"),
            CheckFlagResponseData(value=True, flag="flag_c", reason="match"),
        ])
        self.schematic.features.check_flags = MagicMock(return_value=bulk_resp)

        # Both None and empty list should behave identically.
        for keys in (None, []):
            self.schematic.features.check_flags.reset_mock()
            results = self.schematic.check_flags(keys, company={"id": "co"})
            self.assertEqual(len(results), 3)
            self.assertEqual([r.flag for r in results], ["flag_a", "flag_b", "flag_c"])
            self.assertEqual([r.value for r in results], [True, False, True])
            self.schematic.features.check_flags.assert_called_once_with(
                company={"id": "co"},
            )

    def test_check_flags_filters_empty_company_and_user(self):
        """Empty company/user dicts must not be sent to features.check_flags;
        only non-empty contexts should appear as kwargs."""
        self.schematic.offline = False
        self.schematic.flag_check_cache_providers = []
        self.schematic.features.check_flags = MagicMock(return_value=self._bulk_response([
            CheckFlagResponseData(value=True, flag="flag_a", reason="match"),
        ]))

        # Passing empty dicts and None should both result in no company/user kwargs
        for empty_company, empty_user in [({}, {}), (None, None), ({}, None), (None, {})]:
            self.schematic.features.check_flags.reset_mock()
            self.schematic.check_flags(["flag_a"], company=empty_company, user=empty_user)
            self.schematic.features.check_flags.assert_called_once_with()

    def test_check_flags_offline_with_no_keys_returns_all_defaults(self):
        """Offline + no keys → one entry per configured flag default."""
        self.schematic.offline = True
        self.schematic.flag_defaults = {"flag_a": True, "flag_b": False}
        results = self.schematic.check_flags(None)
        self.assertEqual(
            sorted((r.flag, r.value) for r in results),
            [("flag_a", True), ("flag_b", False)],
        )

    def test_check_flag_raising_cache_provider_falls_back_to_api(self):
        """A cache provider that raises must be treated as a miss, not a fatal
        error — the API call should still happen and return a real value."""
        boom = MagicMock()
        boom.get = MagicMock(side_effect=Exception("redis: connection refused"))
        boom.set = MagicMock(side_effect=Exception("redis: connection refused"))

        self.schematic.offline = False
        self.schematic.flag_check_cache_providers = [boom]
        self.schematic.features.check_flag = MagicMock(
            return_value=MagicMock(data=CheckFlagResponseData(
                value=True, flag="flag_a", reason="match",
            ))
        )

        result = self.schematic.check_flag("flag_a")
        self.assertTrue(result)
        boom.get.assert_called_once()
        # set was attempted but its failure was swallowed
        boom.set.assert_called_once()
        self.schematic.features.check_flag.assert_called_once()

    def test_check_flags_raising_cache_provider_falls_back_to_api(self):
        """Same guarantee for the bulk path: a raising cache provider should
        produce real API values, not `Error occurred - using default value`."""
        boom = MagicMock()
        boom.get = MagicMock(side_effect=Exception("redis: connection refused"))
        boom.set = MagicMock(side_effect=Exception("redis: connection refused"))

        self.schematic.offline = False
        self.schematic.flag_check_cache_providers = [boom]
        self.schematic.features.check_flags = MagicMock(return_value=self._bulk_response([
            CheckFlagResponseData(value=True, flag="flag_a", reason="match"),
            CheckFlagResponseData(value=False, flag="flag_b", reason="match"),
        ]))

        results = self.schematic.check_flags(["flag_a", "flag_b"])
        self.assertEqual([r.value for r in results], [True, False])
        self.assertEqual([r.reason for r in results], ["match", "match"])
        # API was called once (not skipped), and stale-cache poisoning didn't happen
        self.schematic.features.check_flags.assert_called_once()

    def test_check_flags_partial_cache_miss_drops_stale_cached_values(self):
        """If a key was cached but the bulk API no longer returns it, treat
        the flag as deleted and return the default — never the stale cache."""
        self.schematic.offline = False

        # Prime cache with a stale entry for "deleted_flag"
        self.schematic.features.check_flag = MagicMock(
            return_value=MagicMock(data=CheckFlagResponseData(
                value=True, flag="deleted_flag", reason="match",
            ))
        )
        self.schematic.check_flag("deleted_flag")

        # Bulk API returns flag_a only — deleted_flag is gone server-side
        self.schematic.features.check_flags = MagicMock(return_value=self._bulk_response([
            CheckFlagResponseData(value=True, flag="flag_a", reason="match"),
        ]))
        self.schematic.flag_defaults = {"deleted_flag": False}

        results = self.schematic.check_flags(["deleted_flag", "flag_a"])
        self.assertEqual([r.flag for r in results], ["deleted_flag", "flag_a"])
        # deleted_flag returns the default (False), NOT the cached True
        self.assertEqual([r.value for r in results], [False, True])
        self.assertEqual(results[0].reason, REASON_FLAG_NOT_FOUND)

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
        assert result.reason == REASON_OFFLINE

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

    async def test_track_with_options(self):
        """All TrackOptions fields must plumb through async track() to the
        CreateEventRequestBody."""
        import datetime as dt
        sent_at = dt.datetime(2026, 5, 21, 12, 0, 0, tzinfo=dt.timezone.utc)
        with patch.object(self.async_schematic.event_buffer, "push") as mock_push:
            await self.async_schematic.track(
                event="credit-consumed",
                company={"id": "company_id"},
                options=TrackOptions(
                    idempotency_key="evt_abc123",
                    sent_at=sent_at,
                    trusted_client_clock=True,
                    backfill=False,
                ),
            )
            mock_push.assert_called_once()
            pushed = mock_push.call_args.args[0]
            assert pushed.idempotency_key == "evt_abc123"
            assert pushed.sent_at == sent_at
            assert pushed.trusted_client_clock is True
            # backfill=False is explicitly set; it should land on the body.
            assert pushed.backfill is False

    async def test_async_identify_with_options(self):
        """IdentifyOptions must plumb through async identify()."""
        with patch.object(self.async_schematic.event_buffer, "push") as mock_push:
            await self.async_schematic.identify(
                keys={"id": "user_id"},
                options=IdentifyOptions(idempotency_key="ident_async"),
            )
            pushed = mock_push.call_args.args[0]
            assert pushed.idempotency_key == "ident_async"

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
        assert all(isinstance(r, CheckFlagResponseData) for r in results)
        assert [r.flag for r in results] == ["flag_a", "flag_b", "flag_c"]
        assert [r.value for r in results] == [True, False, False]
        assert results[0].reason == REASON_OFFLINE

    @staticmethod
    def _bulk_response(flags):
        return MagicMock(data=MagicMock(flags=flags))

    async def test_check_flags_uses_bulk_api_endpoint(self):
        """check_flags must call features.check_flags (bulk) not features.check_flag."""
        self.async_schematic.offline = False
        self.async_schematic.flag_check_cache_providers = []

        bulk_resp = self._bulk_response([
            CheckFlagResponseData(value=True, flag="enabled_flag", reason="match"),
            CheckFlagResponseData(value=False, flag="disabled_flag", reason="match"),
        ])
        self.async_schematic.features.check_flags = AsyncMock(return_value=bulk_resp)
        self.async_schematic.features.check_flag = AsyncMock()

        results = await self.async_schematic.check_flags(
            ["enabled_flag", "disabled_flag"],
            company={"id": "company_id"},
        )
        assert [r.flag for r in results] == ["enabled_flag", "disabled_flag"]
        assert [r.value for r in results] == [True, False]
        self.async_schematic.features.check_flags.assert_called_once_with(
            company={"id": "company_id"},
        )
        self.async_schematic.features.check_flag.assert_not_called()

    async def test_check_flags_includes_missing_flags_with_default(self):
        """Flags absent from the bulk response should be filled in with defaults."""
        self.async_schematic.offline = False
        self.async_schematic.flag_check_cache_providers = []
        self.async_schematic.flag_defaults = {"missing_flag": True}

        bulk_resp = self._bulk_response([
            CheckFlagResponseData(value=True, flag="real_flag", reason="match"),
            CheckFlagResponseData(value=True, flag="another_real_flag", reason="match"),
        ])
        self.async_schematic.features.check_flags = AsyncMock(return_value=bulk_resp)

        results = await self.async_schematic.check_flags(
            ["real_flag", "missing_flag", "another_real_flag"],
        )
        assert [r.flag for r in results] == ["real_flag", "missing_flag", "another_real_flag"]
        assert [r.value for r in results] == [True, True, True]
        assert results[1].reason == REASON_FLAG_NOT_FOUND

    async def test_check_flags_partial_cache_miss_calls_bulk_api(self):
        """If any requested key isn't cached, the bulk API is called and
        cached values are merged with the fresh bulk results."""
        self.async_schematic.offline = False

        # Prime cache for flag_a only via single check_flag
        self.async_schematic.features.check_flag = AsyncMock(
            return_value=MagicMock(data=CheckFlagResponseData(
                value=True, flag="flag_a", reason="match",
            ))
        )
        await self.async_schematic.check_flag("flag_a")

        self.async_schematic.features.check_flags = AsyncMock(return_value=self._bulk_response([
            CheckFlagResponseData(value=False, flag="flag_a", reason="match"),
            CheckFlagResponseData(value=True, flag="flag_b", reason="match"),
        ]))

        results = await self.async_schematic.check_flags(["flag_a", "flag_b"])
        self.async_schematic.features.check_flags.assert_called_once()
        assert [r.value for r in results] == [False, True]

    async def test_check_flags_uses_default_on_error(self):
        """Bulk API errors should fall back to per-key flag defaults."""
        self.async_schematic.offline = False
        self.async_schematic.flag_check_cache_providers = []
        self.async_schematic.flag_defaults = {"flag_a": True}
        self.async_schematic.features.check_flags = AsyncMock(
            side_effect=Exception("api error")
        )
        results = await self.async_schematic.check_flags(["flag_a", "flag_b"])
        assert [r.flag for r in results] == ["flag_a", "flag_b"]
        assert [r.value for r in results] == [True, False]

    async def test_check_flags_returns_full_response_data(self):
        self.async_schematic.offline = False
        self.async_schematic.flag_check_cache_providers = []

        bulk_resp = self._bulk_response([
            CheckFlagResponseData(
                value=True, flag="flag_a", reason="rule_match",
                rule_id="rule_flag_a", company_id="comp_123",
            ),
            CheckFlagResponseData(
                value=True, flag="flag_b", reason="rule_match",
                rule_id="rule_flag_b", company_id="comp_123",
            ),
        ])
        self.async_schematic.features.check_flags = AsyncMock(return_value=bulk_resp)

        results = await self.async_schematic.check_flags(
            ["flag_a", "flag_b"],
            company={"id": "company_id"},
        )
        assert [r.flag for r in results] == ["flag_a", "flag_b"]
        assert all(isinstance(r, CheckFlagResponseData) for r in results)
        assert results[0].rule_id == "rule_flag_a"
        assert results[1].rule_id == "rule_flag_b"
        assert results[0].company_id == "comp_123"

    async def test_check_flags_via_datastream_skips_api(self):
        """When DataStream is enabled and connected, check_flags evaluates
        all keys locally and never touches the bulk API."""
        from schematic.types import RulesengineCheckFlagResult

        config = AsyncSchematicConfig(
            logger=MagicMock(),
            httpx_client=MagicMock(spec=AsyncClient),
            event_buffer_period=1,
            use_datastream=True,
        )
        client = AsyncSchematic("test_key", config)
        try:
            mock_ds = MagicMock()

            async def fake_ds_check(eval_ctx, flag_key):
                return RulesengineCheckFlagResult(
                    value=(flag_key == "flag_a"),
                    flag_key=flag_key,
                    reason="match",
                )

            mock_ds.check_flag = AsyncMock(side_effect=fake_ds_check)
            client._datastream_client = mock_ds
            client.features.check_flags = AsyncMock()

            results = await client.check_flags(
                ["flag_a", "flag_b"], company={"id": "co-1"},
            )
            assert [r.value for r in results] == [True, False]
            client.features.check_flags.assert_not_called()
            assert mock_ds.check_flag.call_count == 2
        finally:
            await client.event_buffer.stop()

    async def test_check_flags_with_no_keys_returns_all_flags(self):
        """No keys passed → call bulk API and return every flag for the context,
        skipping the DataStream path entirely."""
        config = AsyncSchematicConfig(
            logger=MagicMock(),
            httpx_client=MagicMock(spec=AsyncClient),
            event_buffer_period=1,
            use_datastream=True,
        )
        client = AsyncSchematic("test_key", config)
        try:
            # DataStream client is set but should NOT be invoked when keys is empty.
            mock_ds = MagicMock()
            mock_ds.is_connected = MagicMock(return_value=True)
            mock_ds.check_flag = AsyncMock()
            client._datastream_client = mock_ds
            client.flag_check_cache_providers = []

            bulk_resp = self._bulk_response([
                CheckFlagResponseData(value=True, flag="flag_a", reason="match"),
                CheckFlagResponseData(value=False, flag="flag_b", reason="match"),
            ])
            client.features.check_flags = AsyncMock(return_value=bulk_resp)

            for keys in (None, []):
                client.features.check_flags.reset_mock()
                results = await client.check_flags(keys, company={"id": "co"})
                assert [r.flag for r in results] == ["flag_a", "flag_b"]
                assert [r.value for r in results] == [True, False]
                client.features.check_flags.assert_called_once_with(
                    company={"id": "co"},
                )
            mock_ds.check_flag.assert_not_called()
        finally:
            await client.event_buffer.stop()

    async def test_check_flags_offline_with_no_keys_returns_all_defaults(self):
        """Async equivalent: offline + no keys → one entry per flag default."""
        self.async_schematic.offline = True
        self.async_schematic.flag_defaults = {"flag_a": True, "flag_b": False}
        results = await self.async_schematic.check_flags(None)
        assert sorted((r.flag, r.value) for r in results) == [
            ("flag_a", True), ("flag_b", False),
        ]

    async def test_check_flags_skips_datastream_when_not_connected(self):
        """If DataStream is configured but not connected, skip it and use the bulk API."""
        config = AsyncSchematicConfig(
            logger=MagicMock(),
            httpx_client=MagicMock(spec=AsyncClient),
            event_buffer_period=1,
            use_datastream=True,
        )
        client = AsyncSchematic("test_key", config)
        try:
            mock_ds = MagicMock()
            mock_ds.is_connected = MagicMock(return_value=False)
            mock_ds.check_flag = AsyncMock()
            client._datastream_client = mock_ds
            client.flag_check_cache_providers = []

            client.features.check_flags = AsyncMock(return_value=self._bulk_response([
                CheckFlagResponseData(value=True, flag="flag_a", reason="match"),
            ]))

            results = await client.check_flags(["flag_a"])
            assert results[0].value is True
            mock_ds.check_flag.assert_not_called()
            client.features.check_flags.assert_called_once()
        finally:
            await client.event_buffer.stop()

    async def test_check_flag_raising_cache_provider_falls_back_to_api(self):
        """Async equivalent: a raising cache provider must be treated as a miss."""
        boom = MagicMock()
        boom.get = MagicMock(side_effect=Exception("redis: connection refused"))
        boom.set = MagicMock(side_effect=Exception("redis: connection refused"))

        self.async_schematic.offline = False
        self.async_schematic.flag_check_cache_providers = [boom]
        self.async_schematic.features.check_flag = AsyncMock(
            return_value=MagicMock(data=CheckFlagResponseData(
                value=True, flag="flag_a", reason="match",
            ))
        )

        result = await self.async_schematic.check_flag("flag_a")
        assert result is True
        boom.get.assert_called_once()
        boom.set.assert_called_once()
        self.async_schematic.features.check_flag.assert_called_once()

    async def test_check_flags_raising_cache_provider_falls_back_to_api(self):
        """Async equivalent: bulk path tolerates a raising cache provider."""
        boom = MagicMock()
        boom.get = MagicMock(side_effect=Exception("redis: connection refused"))
        boom.set = MagicMock(side_effect=Exception("redis: connection refused"))

        self.async_schematic.offline = False
        self.async_schematic.flag_check_cache_providers = [boom]
        self.async_schematic.features.check_flags = AsyncMock(return_value=self._bulk_response([
            CheckFlagResponseData(value=True, flag="flag_a", reason="match"),
            CheckFlagResponseData(value=False, flag="flag_b", reason="match"),
        ]))

        results = await self.async_schematic.check_flags(["flag_a", "flag_b"])
        assert [r.value for r in results] == [True, False]
        assert [r.reason for r in results] == ["match", "match"]
        self.async_schematic.features.check_flags.assert_called_once()

    async def test_check_flags_partial_cache_miss_drops_stale_cached_values(self):
        """Async equivalent: deleted flags must not leak through from stale cache."""
        self.async_schematic.offline = False

        self.async_schematic.features.check_flag = AsyncMock(
            return_value=MagicMock(data=CheckFlagResponseData(
                value=True, flag="deleted_flag", reason="match",
            ))
        )
        await self.async_schematic.check_flag("deleted_flag")

        self.async_schematic.features.check_flags = AsyncMock(return_value=self._bulk_response([
            CheckFlagResponseData(value=True, flag="flag_a", reason="match"),
        ]))
        self.async_schematic.flag_defaults = {"deleted_flag": False}

        results = await self.async_schematic.check_flags(["deleted_flag", "flag_a"])
        assert [r.flag for r in results] == ["deleted_flag", "flag_a"]
        assert [r.value for r in results] == [False, True]
        assert results[0].reason == REASON_FLAG_NOT_FOUND

    async def test_check_flags_datastream_failure_falls_back_to_bulk_api(self):
        """If DataStream raises for any key, fall back to the bulk API for all keys."""
        config = AsyncSchematicConfig(
            logger=MagicMock(),
            httpx_client=MagicMock(spec=AsyncClient),
            event_buffer_period=1,
            use_datastream=True,
        )
        client = AsyncSchematic("test_key", config)
        try:
            mock_ds = MagicMock()
            mock_ds.check_flag = AsyncMock(side_effect=RuntimeError("ds down"))
            client._datastream_client = mock_ds

            client.features.check_flags = AsyncMock(return_value=self._bulk_response([
                CheckFlagResponseData(value=True, flag="flag_a", reason="match"),
                CheckFlagResponseData(value=False, flag="flag_b", reason="match"),
            ]))
            client.flag_check_cache_providers = []

            results = await client.check_flags(["flag_a", "flag_b"])
            assert [r.value for r in results] == [True, False]
            client.features.check_flags.assert_called_once()
        finally:
            await client.event_buffer.stop()


TTL_SECONDS = 120.0

CREDIT_ENTITLEMENT = FeatureEntitlement(
    feature_id="feat",
    feature_key="inference",
    value_type="credit",
)


def _held_reservation(**overrides) -> FlagCheckReservationResponseData:
    fields = dict(
        id="rsv_1",
        company_id="co_1",
        credit_type_id="bilcr_inference",
        consumption_rate=10.0,
        credits_reserved=500.0,
        quantity_reserved=50.0,
        event_subtype="inference_tokens",
        expires_at=dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=TTL_SECONDS),
    )
    fields.update(overrides)
    return FlagCheckReservationResponseData(**fields)  # type: ignore[arg-type]


def _reserve_response(**overrides):
    fields = dict(
        flag="inference",
        flag_id="flag_1",
        value=True,
        reason="matched",
        company_id="co_1",
        user_id="user_1",
        rule_id="rule_1",
        entitlement=CREDIT_ENTITLEMENT,
        reservation=_held_reservation(),
    )
    fields.update(overrides)
    return MagicMock(data=CheckAndReserveFlagResponseData(**fields))  # type: ignore[arg-type]


class TestSchematicPreflight(unittest.TestCase):
    """Preflight options on the sync REST check path."""

    def setUp(self):
        config = SchematicConfig(
            event_buffer_period=1,
            logger=MagicMock(),
            httpx_client=MagicMock(spec=Client),
        )
        self.schematic = Schematic("api_key", config)
        self.data = CheckFlagResponseData(value=True, flag="inference", reason="matched")
        self.schematic.features.check_flag = MagicMock(return_value=MagicMock(data=self.data))

    def tearDown(self):
        self.schematic.event_buffer.stop()

    def test_plain_check_sends_no_preflight_kwarg(self):
        self.schematic.check_flag("inference", company={"id": "co_1"})
        self.assertNotIn("preflight", self.schematic.features.check_flag.call_args.kwargs)

    def test_usage_is_forwarded_as_preflight(self):
        self.schematic.check_flag("inference", company={"id": "co_1"}, options=CheckFlagOptions(usage=5))
        preflight = self.schematic.features.check_flag.call_args.kwargs["preflight"]
        self.assertEqual(preflight, PreflightRequestBody(usage=5))

    def test_event_usage_and_credit_cost_are_forwarded_as_preflight(self):
        self.schematic.check_flag(
            "inference",
            company={"id": "co_1"},
            options=CheckFlagOptions(
                event_usage=EventUsage(event_subtype="inference_tokens", quantity=7),
                credit_cost={"bilcr_inference": 12.5},
            ),
        )
        preflight = self.schematic.features.check_flag.call_args.kwargs["preflight"]
        self.assertEqual(
            preflight,
            PreflightRequestBody(
                credit_cost={"bilcr_inference": 12.5},
                event_usage=PreflightEventUsageRequestBody(event_subtype="inference_tokens", quantity=7),
            ),
        )

    def test_preflighted_check_neither_reads_nor_writes_the_cache(self):
        company = {"id": "co_1"}
        options = CheckFlagOptions(usage=5)

        # Two preflighted checks both hit the API: the answer is specific to
        # the simulated usage, so it is never served from the cache.
        self.schematic.check_flag("inference", company=company, options=options)
        self.schematic.check_flag("inference", company=company, options=options)
        self.assertEqual(self.schematic.features.check_flag.call_count, 2)

        # And nothing they returned was written to the cache: the first plain
        # check still has to ask the API.
        self.schematic.check_flag("inference", company=company)
        self.assertEqual(self.schematic.features.check_flag.call_count, 3)

    def test_plain_check_still_caches(self):
        company = {"id": "co_1"}
        self.schematic.check_flag("inference", company=company)
        self.schematic.check_flag("inference", company=company)
        self.assertEqual(self.schematic.features.check_flag.call_count, 1)


class TestQuantityValidation(unittest.TestCase):
    """What a usage, or a settled quantity, has to be to size a credit hold."""

    def test_accepts_finite_non_negative_numbers(self):
        for value in (0, 50, 100.0, 0.5):
            with self.subTest(value=value):
                self.assertTrue(_is_valid_quantity(value))

    def test_rejects_bools_negatives_and_non_finite_floats(self):
        for value in (True, -1, float("nan"), float("inf")):
            with self.subTest(value=value):
                self.assertFalse(_is_valid_quantity(value))


class TestSchematicServerReservation(unittest.TestCase):
    """check() and track_with_reservation() against the server hold path."""

    def setUp(self):
        self.schematic = self._client()

    def tearDown(self):
        self.schematic.event_buffer.stop()

    def _client(self, **config_overrides) -> Schematic:
        config_kwargs = dict(
            event_buffer_period=1,
            logger=MagicMock(),
            httpx_client=MagicMock(spec=Client),
            credit_leases=CreditLeaseConfig(mode="server", default_reservation_ttl=TTL_SECONDS),
        )
        config_kwargs.update(config_overrides)
        client = Schematic("api_key", SchematicConfig(**config_kwargs))  # type: ignore[arg-type]
        client.features.check_and_reserve_flag = MagicMock(return_value=_reserve_response())
        client.features.check_flag = MagicMock(
            return_value=MagicMock(data=CheckFlagResponseData(value=True, flag="inference", reason="plain check"))
        )
        client.credits.release_credit_reservation = MagicMock()
        client.flag_check_cache_providers = []
        return client

    def test_returns_a_reservation_handle_built_from_the_response(self):
        before = dt.datetime.now(dt.timezone.utc)
        with patch.object(self.schematic.event_buffer, "push") as mock_push:
            result = self.schematic.check(
                "inference",
                company={"id": "co_1"},
                user={"id": "user_1"},
                options=CheckOptions(usage=50, event_subtype="inference_tokens"),
            )
        after = dt.datetime.now(dt.timezone.utc)

        self.assertTrue(result.allowed)
        self.assertTrue(result.value)
        self.assertEqual(result.reason, "matched")
        self.assertEqual(result.flag_key, "inference")
        self.assertEqual(result.flag_id, "flag_1")
        self.assertEqual(result.entitlement, CREDIT_ENTITLEMENT)

        assert result.reservation is not None
        self.assertEqual(result.reservation.id, "rsv_1")
        # No lease exists server side; the handle mirrors the id.
        self.assertEqual(result.reservation.lease_id, "rsv_1")
        self.assertEqual(result.reservation.mode, "server")
        self.assertEqual(result.reservation.company_id, "co_1")
        self.assertEqual(result.reservation.credit_type_id, "bilcr_inference")
        self.assertEqual(result.reservation.event_subtype, "inference_tokens")
        self.assertEqual(result.reservation.quantity_reserved, 50.0)
        self.assertEqual(result.reservation.credits_reserved, 500.0)
        self.assertEqual(result.reservation.consumption_rate, 10.0)
        self.assertEqual(result.reservation.company, {"id": "co_1"})
        self.assertEqual(result.reservation.user, {"id": "user_1"})

        kwargs = self.schematic.features.check_and_reserve_flag.call_args.kwargs
        self.assertEqual(self.schematic.features.check_and_reserve_flag.call_args.args, ("inference",))
        self.assertEqual(kwargs["quantity"], 50)
        self.assertEqual(kwargs["company"], {"id": "co_1"})
        self.assertEqual(kwargs["user"], {"id": "user_1"})
        self.assertEqual(
            kwargs["preflight"],
            PreflightRequestBody(
                event_usage=PreflightEventUsageRequestBody(event_subtype="inference_tokens", quantity=50)
            ),
        )
        ttl = dt.timedelta(seconds=TTL_SECONDS)
        self.assertGreaterEqual(kwargs["expires_at"], before + ttl)
        self.assertLessEqual(kwargs["expires_at"], after + ttl)
        self.assertEqual(kwargs["request_options"], {})
        self.assertTrue(kwargs["idempotency_key"])

        # The server logs the flag check for check-and-reserve itself.
        mock_push.assert_not_called()

    def test_sends_the_generic_usage_preflight_without_an_event_subtype(self):
        self.schematic.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50))
        kwargs = self.schematic.features.check_and_reserve_flag.call_args.kwargs
        self.assertEqual(kwargs["preflight"], PreflightRequestBody(usage=50))

    def test_forwards_the_per_check_timeout(self):
        self.schematic.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50, timeout=2.5))
        kwargs = self.schematic.features.check_and_reserve_flag.call_args.kwargs
        self.assertEqual(kwargs["request_options"], {"timeout": 2.5})

    def test_leaves_the_default_retry_policy_in_place(self):
        # The idempotency key is what makes a retried 5xx safe, so the call no
        # longer opts out of retries.
        self.schematic.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50))
        kwargs = self.schematic.features.check_and_reserve_flag.call_args.kwargs
        self.assertNotIn("max_retries", kwargs["request_options"])

    def test_mints_a_fresh_idempotency_key_per_check(self):
        self.schematic.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50))
        first = self.schematic.features.check_and_reserve_flag.call_args.kwargs["idempotency_key"]
        self.schematic.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50))
        second = self.schematic.features.check_and_reserve_flag.call_args.kwargs["idempotency_key"]
        self.assertNotEqual(first, second)

    def test_a_fractional_usage_sizes_the_hold_and_rounds_the_preflight_up(self):
        self.schematic.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=0.5))
        kwargs = self.schematic.features.check_and_reserve_flag.call_args.kwargs
        self.assertEqual(kwargs["quantity"], 0.5)
        # The hold takes the fraction; the preflight's usage is an integer, and
        # rounding it down would ask about less usage than is about to land.
        self.assertEqual(kwargs["preflight"], PreflightRequestBody(usage=1))

    def test_an_integral_float_usage_reaches_the_preflight_unchanged(self):
        self.schematic.check(
            "inference",
            company={"id": "co_1"},
            options=CheckOptions(usage=100.0, event_subtype="inference_tokens"),
        )
        kwargs = self.schematic.features.check_and_reserve_flag.call_args.kwargs
        self.assertEqual(kwargs["quantity"], 100.0)
        self.assertEqual(
            kwargs["preflight"],
            PreflightRequestBody(
                event_usage=PreflightEventUsageRequestBody(event_subtype="inference_tokens", quantity=100)
            ),
        )

    def test_a_reservation_ttl_above_the_cap_is_clamped(self):
        client = self._client(credit_leases=CreditLeaseConfig(default_reservation_ttl=7200.0))
        try:
            # Short of the cap by the skew allowance, so a client running
            # slightly fast still asks for something the server accepts.
            self.assertEqual(client._reservation_ttl, MAX_RESERVATION_TTL - RESERVATION_TTL_SKEW_ALLOWANCE)
            warning = " ".join(str(call.args[0]) for call in client.logger.warning.call_args_list)
            self.assertIn("one hour cap", warning)
            self.assertIn(
                f"server-mode holds will be clamped to {MAX_RESERVATION_TTL - RESERVATION_TTL_SKEW_ALLOWANCE}s",
                warning,
            )
        finally:
            client.event_buffer.stop()

    def test_denies_without_a_reservation_when_credits_are_short(self):
        self.schematic.features.check_and_reserve_flag.return_value = _reserve_response(
            value=False, reason="Insufficient credits", reservation=None,
        )
        result = self.schematic.check(
            "inference", company={"id": "co_1"}, options=CheckOptions(usage=50, event_subtype="inference_tokens"),
        )
        self.assertFalse(result.allowed)
        self.assertFalse(result.value)
        self.assertEqual(result.reason, "Insufficient credits")
        self.assertIsNone(result.reservation)
        self.schematic.credits.release_credit_reservation.assert_not_called()

    def test_allows_without_a_reservation_when_the_feature_is_not_credit_metered(self):
        self.schematic.features.check_and_reserve_flag.return_value = _reserve_response(
            reason="company entitlement",
            reservation=None,
            entitlement=FeatureEntitlement(feature_id="feat", feature_key="inference", value_type="boolean"),
        )
        result = self.schematic.check(
            "inference", company={"id": "co_1"}, options=CheckOptions(usage=50, event_subtype="inference_tokens"),
        )
        self.assertTrue(result.allowed)
        self.assertIsNone(result.reservation)
        self.assertEqual(result.reason, "company entitlement")

    def test_payment_required_denies_even_with_fail_open(self):
        self.schematic.features.check_and_reserve_flag.side_effect = PaymentRequiredError(
            body=ApiError(error="credit balance exhausted")
        )
        result = self.schematic.check(
            "inference",
            company={"id": "co_1"},
            options=CheckOptions(usage=50, on_acquire_failure="fail-open", default_value=True),
        )
        self.assertFalse(result.allowed)
        self.assertFalse(result.value)
        self.assertEqual(result.reason, INSUFFICIENT_CREDITS_REASON)
        self.assertEqual(result.error, "credit balance exhausted")
        self.assertIsNone(result.reservation)

    def test_a_402_api_error_denies_even_with_fail_open(self):
        # The generated features client has no 402 branch, so a real 402 from
        # check-and-reserve arrives as the base ApiError.
        self.schematic.features.check_and_reserve_flag.side_effect = CoreApiError(
            status_code=402, body={"error": "credit balance exhausted"},
        )
        result = self.schematic.check(
            "inference",
            company={"id": "co_1"},
            options=CheckOptions(usage=50, on_acquire_failure="fail-open", default_value=True),
        )
        self.assertFalse(result.allowed)
        self.assertFalse(result.value)
        self.assertEqual(result.reason, INSUFFICIENT_CREDITS_REASON)
        self.assertEqual(result.error, "credit balance exhausted")
        self.assertIsNone(result.reservation)

    def test_fails_closed_when_check_and_reserve_errors(self):
        self.schematic.features.check_and_reserve_flag.side_effect = Exception("ECONNRESET")
        result = self.schematic.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50))
        self.assertFalse(result.allowed)
        self.assertFalse(result.value)
        self.assertEqual(result.reason, "server_reservation_failed")
        self.assertEqual(result.error, "server_reservation_failed")
        self.assertIsNone(result.reservation)

    def test_fails_open_to_the_per_check_default_value(self):
        self.schematic.features.check_and_reserve_flag.side_effect = Exception("ECONNRESET")
        result = self.schematic.check(
            "inference",
            company={"id": "co_1"},
            options=CheckOptions(usage=50, on_acquire_failure="fail-open", default_value=True),
        )
        self.assertTrue(result.allowed)
        self.assertTrue(result.value)
        self.assertEqual(result.reason, "server_reservation_failed_fail_open")
        self.assertEqual(result.error, "server_reservation_failed")

    def test_fails_open_to_the_client_level_flag_default(self):
        client = self._client(flag_defaults={"inference": True})
        try:
            client.features.check_and_reserve_flag.side_effect = Exception("ECONNRESET")
            result = client.check(
                "inference", company={"id": "co_1"}, options=CheckOptions(usage=50, on_acquire_failure="fail-open"),
            )
            self.assertTrue(result.allowed)
            self.assertEqual(result.reason, "server_reservation_failed_fail_open")
        finally:
            client.event_buffer.stop()

        # The same client with no configured default stays denied.
        self.schematic.features.check_and_reserve_flag.side_effect = Exception("ECONNRESET")
        denied = self.schematic.check(
            "inference", company={"id": "co_1"}, options=CheckOptions(usage=50, on_acquire_failure="fail-open"),
        )
        self.assertFalse(denied.allowed)

    def test_zero_usage_falls_back_to_a_plain_check(self):
        result = self.schematic.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=0))
        self.schematic.features.check_and_reserve_flag.assert_not_called()
        self.schematic.features.check_flag.assert_called_once()
        self.assertTrue(result.allowed)
        self.assertEqual(result.reason, "plain check")
        self.assertIsNone(result.reservation)

    def test_invalid_usage_resolves_through_the_failure_contract(self):
        for usage in (-5, float("nan"), float("inf"), True):
            with self.subTest(usage=usage):
                denied = self.schematic.check(
                    "inference", company={"id": "co_1"}, options=CheckOptions(usage=usage),  # type: ignore[arg-type]
                )
                self.assertFalse(denied.allowed)
                self.assertEqual(denied.reason, "invalid_usage")
                self.assertEqual(denied.error, "invalid_usage")

        opened = self.schematic.check(
            "inference",
            company={"id": "co_1"},
            options=CheckOptions(usage=-5, on_acquire_failure="fail-open", default_value=True),
        )
        self.assertTrue(opened.allowed)
        self.assertEqual(opened.reason, "invalid_usage_fail_open")

        self.schematic.features.check_and_reserve_flag.assert_not_called()
        self.schematic.features.check_flag.assert_not_called()

    def test_releases_a_hold_that_names_no_event_subtype(self):
        self.schematic.features.check_and_reserve_flag.return_value = _reserve_response(
            reservation=_held_reservation(id="rsv_orphan", event_subtype=None),
        )
        result = self.schematic.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50))
        self.schematic.credits.release_credit_reservation.assert_called_once_with("rsv_orphan")
        self.assertFalse(result.allowed)
        self.assertEqual(result.reason, "missing_event_subtype")
        self.assertIsNone(result.reservation)

    def test_a_failed_release_is_swallowed(self):
        self.schematic.features.check_and_reserve_flag.return_value = _reserve_response(
            reservation=_held_reservation(id="rsv_orphan", event_subtype=None),
        )
        self.schematic.credits.release_credit_reservation.side_effect = Exception("boom")
        result = self.schematic.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50))
        self.assertEqual(result.reason, "missing_event_subtype")
        self.schematic.logger.warning.assert_called()

    def test_a_released_hold_keeps_the_server_verdict_when_failing_open(self):
        self.schematic.features.check_and_reserve_flag.return_value = _reserve_response(
            reservation=_held_reservation(id="rsv_orphan", event_subtype=None),
        )
        result = self.schematic.check(
            "inference", company={"id": "co_1"}, options=CheckOptions(usage=50, on_acquire_failure="fail-open"),
        )
        self.schematic.credits.release_credit_reservation.assert_called_once_with("rsv_orphan")
        # The server evaluated the flag and allowed it; only the settle is
        # impossible, and fail-open assumes the credits are there.
        self.assertTrue(result.allowed)
        self.assertTrue(result.value)
        self.assertEqual(result.reason, "matched")
        self.assertEqual(result.flag_id, "flag_1")
        self.assertEqual(result.entitlement, CREDIT_ENTITLEMENT)
        self.assertEqual(result.error, "missing_event_subtype")
        self.assertIsNone(result.reservation)

    def test_no_credit_lease_config_falls_back_to_a_plain_check(self):
        client = self._client(credit_leases=None)
        try:
            result = client.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50))
            client.features.check_and_reserve_flag.assert_not_called()
            client.features.check_flag.assert_called_once()
            self.assertIsNone(result.reservation)
            # The preflight still rides along on the plain check.
            self.assertEqual(
                client.features.check_flag.call_args.kwargs["preflight"], PreflightRequestBody(usage=50),
            )
        finally:
            client.event_buffer.stop()

    def test_client_mode_falls_back_and_warns_at_construction(self):
        client = self._client(credit_leases=CreditLeaseConfig(mode="client"))
        try:
            warning = " ".join(str(call.args[0]) for call in client.logger.warning.call_args_list)
            self.assertIn("'client'", warning)
            result = client.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50))
            client.features.check_and_reserve_flag.assert_not_called()
            client.features.check_flag.assert_called_once()
            self.assertIsNone(result.reservation)
        finally:
            client.event_buffer.stop()

    def test_offline_check_returns_the_flag_default(self):
        client = self._client(offline=True, flag_defaults={"inference": True})
        try:
            result = client.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50))
            client.features.check_and_reserve_flag.assert_not_called()
            self.assertTrue(result.allowed)
            self.assertEqual(result.reason, REASON_OFFLINE)
            self.assertIsNone(result.reservation)
        finally:
            client.event_buffer.stop()

    def _reservation_handle(self) -> Reservation:
        result = self.schematic.check(
            "inference",
            company={"id": "co_1"},
            user={"id": "user_1"},
            options=CheckOptions(usage=50, event_subtype="inference_tokens"),
        )
        assert result.reservation is not None
        return result.reservation

    def test_track_with_reservation_settles_by_reservation_id(self):
        reservation = self._reservation_handle()
        with patch.object(self.schematic.event_buffer, "push") as mock_push:
            self.schematic.track_with_reservation(
                reservation, 20, TrackWithReservationOptions(traits={"model": "opus"}),
            )

        pushed = mock_push.call_args.args[0]
        self.assertEqual(pushed.event_type, "track")
        self.assertEqual(pushed.body.event, "inference_tokens")
        self.assertEqual(pushed.body.quantity, 20)
        self.assertEqual(pushed.body.reservation_id, "rsv_1")
        # The server prefers lease_id when both are set, and there is no lease.
        self.assertIsNone(pushed.body.lease_id)
        self.assertEqual(pushed.body.company, {"id": "co_1"})
        self.assertEqual(pushed.body.user, {"id": "user_1"})
        self.assertEqual(pushed.body.traits, {"model": "opus"})
        self.assertEqual(pushed.idempotency_key, "lease-reservation:rsv_1")
        self.schematic.credits.release_credit_reservation.assert_not_called()

    def test_track_with_reservation_skips_an_invalid_quantity(self):
        reservation = self._reservation_handle()
        with patch.object(self.schematic.event_buffer, "push") as mock_push:
            for quantity in (-1, float("nan"), float("inf"), True):
                self.schematic.track_with_reservation(reservation, quantity)  # type: ignore[arg-type]
        mock_push.assert_not_called()

    def test_track_with_reservation_settles_a_fractional_quantity_as_a_whole_unit(self):
        reservation = self._reservation_handle()
        with patch.object(self.schematic.event_buffer, "push") as mock_push:
            self.schematic.track_with_reservation(reservation, 0.5)
        # A track event's quantity is an integer, so a partial unit bills as one.
        self.assertEqual(mock_push.call_args.args[0].body.quantity, 1)

    def test_track_with_reservation_without_a_hold_says_to_use_track(self):
        with patch.object(self.schematic.event_buffer, "push") as mock_push:
            self.schematic.track_with_reservation(None, 5)
        mock_push.assert_not_called()
        self.assertIn("track()", str(self.schematic.logger.error.call_args.args[0]))

    def test_track_with_reservation_is_a_no_op_when_offline(self):
        reservation = self._reservation_handle()
        self.schematic.offline = True
        with patch.object(self.schematic.event_buffer, "push") as mock_push:
            self.schematic.track_with_reservation(reservation, 20)
        mock_push.assert_not_called()


def _async_server_client(**config_overrides) -> AsyncSchematic:
    config_kwargs = dict(
        event_buffer_period=1,
        logger=MagicMock(),
        httpx_client=MagicMock(spec=AsyncClient),
        credit_leases=CreditLeaseConfig(mode="server", default_reservation_ttl=TTL_SECONDS),
    )
    config_kwargs.update(config_overrides)
    client = AsyncSchematic("test_key", AsyncSchematicConfig(**config_kwargs))  # type: ignore[arg-type]
    client.features.check_and_reserve_flag = AsyncMock(return_value=_reserve_response())
    client.features.check_flag = AsyncMock(
        return_value=MagicMock(data=CheckFlagResponseData(value=True, flag="inference", reason="plain check"))
    )
    client.credits.release_credit_reservation = AsyncMock()
    client.flag_check_cache_providers = []
    return client


@pytest.mark.asyncio
class TestAsyncSchematicPreflight:
    """Preflight options on the async check paths."""

    @pytest.fixture(autouse=True)
    async def setup_and_teardown(self):
        config = AsyncSchematicConfig(
            logger=MagicMock(),
            httpx_client=MagicMock(spec=AsyncClient),
            event_buffer_period=1,
        )
        self.client = AsyncSchematic("test_key", config)
        self.client.features.check_flag = AsyncMock(
            return_value=MagicMock(data=CheckFlagResponseData(value=True, flag="inference", reason="matched"))
        )
        yield
        await self.client.event_buffer.stop()

    async def test_plain_check_sends_no_preflight_kwarg(self):
        await self.client.check_flag("inference", company={"id": "co_1"})
        assert "preflight" not in self.client.features.check_flag.call_args.kwargs

    async def test_usage_is_forwarded_as_preflight(self):
        await self.client.check_flag("inference", company={"id": "co_1"}, options=CheckFlagOptions(usage=5))
        assert self.client.features.check_flag.call_args.kwargs["preflight"] == PreflightRequestBody(usage=5)

    async def test_preflighted_check_neither_reads_nor_writes_the_cache(self):
        company = {"id": "co_1"}
        options = CheckFlagOptions(usage=5)

        await self.client.check_flag("inference", company=company, options=options)
        await self.client.check_flag("inference", company=company, options=options)
        assert self.client.features.check_flag.call_count == 2

        await self.client.check_flag("inference", company=company)
        assert self.client.features.check_flag.call_count == 3

    async def test_plain_check_still_caches(self):
        company = {"id": "co_1"}
        await self.client.check_flag("inference", company=company)
        await self.client.check_flag("inference", company=company)
        assert self.client.features.check_flag.call_count == 1

    async def test_datastream_check_receives_the_options(self):
        ds_result = RulesengineCheckFlagResult(value=True, flag_key="inference", reason="matched")
        mock_ds = MagicMock()
        mock_ds.check_flag = AsyncMock(return_value=ds_result)
        self.client._datastream_client = mock_ds

        options = CheckFlagOptions(usage=5)
        await self.client.check_flag("inference", company={"id": "co_1"}, options=options)

        assert mock_ds.check_flag.call_args.kwargs["options"] is options
        self.client.features.check_flag.assert_not_called()

    async def test_check_threads_its_preflight_through_the_datastream_fallback(self):
        ds_result = RulesengineCheckFlagResult(value=True, flag_key="inference", reason="matched")
        mock_ds = MagicMock()
        mock_ds.check_flag = AsyncMock(return_value=ds_result)
        self.client._datastream_client = mock_ds

        # No credit leases configured, so check() is a plain check that still
        # carries the caller's preflight.
        result = await self.client.check(
            "inference", company={"id": "co_1"}, options=CheckOptions(usage=5, event_subtype="inference_tokens"),
        )

        assert result.allowed is True
        assert result.reservation is None
        threaded = mock_ds.check_flag.call_args.kwargs["options"]
        assert threaded.event_usage == EventUsage(event_subtype="inference_tokens", quantity=5)


@pytest.mark.asyncio
class TestAsyncSchematicServerReservation:
    """check() and track_with_reservation() on the async client."""

    @pytest.fixture(autouse=True)
    async def setup_and_teardown(self):
        self.client = _async_server_client()
        yield
        await self.client.event_buffer.stop()

    async def test_returns_a_reservation_handle_built_from_the_response(self):
        before = dt.datetime.now(dt.timezone.utc)
        with patch.object(self.client.event_buffer, "push", new=AsyncMock()) as mock_push:
            result = await self.client.check(
                "inference",
                company={"id": "co_1"},
                user={"id": "user_1"},
                options=CheckOptions(usage=50, event_subtype="inference_tokens"),
            )
        after = dt.datetime.now(dt.timezone.utc)

        assert result.allowed is True
        assert result.value is True
        assert result.reason == "matched"
        assert result.flag_key == "inference"
        assert result.flag_id == "flag_1"
        assert result.entitlement == CREDIT_ENTITLEMENT

        assert result.reservation is not None
        assert result.reservation.id == "rsv_1"
        assert result.reservation.lease_id == "rsv_1"
        assert result.reservation.mode == "server"
        assert result.reservation.company_id == "co_1"
        assert result.reservation.credit_type_id == "bilcr_inference"
        assert result.reservation.event_subtype == "inference_tokens"
        assert result.reservation.quantity_reserved == 50.0
        assert result.reservation.credits_reserved == 500.0
        assert result.reservation.consumption_rate == 10.0
        assert result.reservation.company == {"id": "co_1"}
        assert result.reservation.user == {"id": "user_1"}

        kwargs = self.client.features.check_and_reserve_flag.call_args.kwargs
        assert kwargs["quantity"] == 50
        assert kwargs["company"] == {"id": "co_1"}
        assert kwargs["user"] == {"id": "user_1"}
        assert kwargs["preflight"] == PreflightRequestBody(
            event_usage=PreflightEventUsageRequestBody(event_subtype="inference_tokens", quantity=50)
        )
        ttl = dt.timedelta(seconds=TTL_SECONDS)
        assert before + ttl <= kwargs["expires_at"] <= after + ttl
        assert kwargs["request_options"] == {}
        assert kwargs["idempotency_key"]

        # The server logs the flag check for check-and-reserve itself.
        mock_push.assert_not_called()

    async def test_sends_the_generic_usage_preflight_without_an_event_subtype(self):
        await self.client.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50))
        kwargs = self.client.features.check_and_reserve_flag.call_args.kwargs
        assert kwargs["preflight"] == PreflightRequestBody(usage=50)

    async def test_forwards_the_per_check_timeout(self):
        await self.client.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50, timeout=2.5))
        kwargs = self.client.features.check_and_reserve_flag.call_args.kwargs
        assert kwargs["request_options"] == {"timeout": 2.5}

    async def test_leaves_the_default_retry_policy_in_place(self):
        # The idempotency key is what makes a retried 5xx safe, so the call no
        # longer opts out of retries.
        await self.client.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50))
        kwargs = self.client.features.check_and_reserve_flag.call_args.kwargs
        assert "max_retries" not in kwargs["request_options"]

    async def test_mints_a_fresh_idempotency_key_per_check(self):
        await self.client.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50))
        first = self.client.features.check_and_reserve_flag.call_args.kwargs["idempotency_key"]
        await self.client.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50))
        second = self.client.features.check_and_reserve_flag.call_args.kwargs["idempotency_key"]
        assert first != second

    async def test_a_fractional_usage_sizes_the_hold_and_rounds_the_preflight_up(self):
        await self.client.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=0.5))
        kwargs = self.client.features.check_and_reserve_flag.call_args.kwargs
        assert kwargs["quantity"] == 0.5
        assert kwargs["preflight"] == PreflightRequestBody(usage=1)

    async def test_a_reservation_ttl_above_the_cap_is_clamped(self):
        client = _async_server_client(credit_leases=CreditLeaseConfig(default_reservation_ttl=7200.0))
        try:
            assert client._reservation_ttl == MAX_RESERVATION_TTL - RESERVATION_TTL_SKEW_ALLOWANCE
            warning = " ".join(str(call.args[0]) for call in client.logger.warning.call_args_list)
            assert "one hour cap" in warning
            assert (
                f"server-mode holds will be clamped to {MAX_RESERVATION_TTL - RESERVATION_TTL_SKEW_ALLOWANCE}s"
                in warning
            )
        finally:
            await client.event_buffer.stop()

    async def test_denies_without_a_reservation_when_credits_are_short(self):
        self.client.features.check_and_reserve_flag.return_value = _reserve_response(
            value=False, reason="Insufficient credits", reservation=None,
        )
        result = await self.client.check(
            "inference", company={"id": "co_1"}, options=CheckOptions(usage=50, event_subtype="inference_tokens"),
        )
        assert result.allowed is False
        assert result.reason == "Insufficient credits"
        assert result.reservation is None
        self.client.credits.release_credit_reservation.assert_not_called()

    async def test_payment_required_denies_even_with_fail_open(self):
        self.client.features.check_and_reserve_flag.side_effect = PaymentRequiredError(
            body=ApiError(error="credit balance exhausted")
        )
        result = await self.client.check(
            "inference",
            company={"id": "co_1"},
            options=CheckOptions(usage=50, on_acquire_failure="fail-open", default_value=True),
        )
        assert result.allowed is False
        assert result.reason == INSUFFICIENT_CREDITS_REASON
        assert result.error == "credit balance exhausted"

    async def test_a_402_api_error_denies_even_with_fail_open(self):
        # The generated features client has no 402 branch, so a real 402 from
        # check-and-reserve arrives as the base ApiError.
        self.client.features.check_and_reserve_flag.side_effect = CoreApiError(
            status_code=402, body={"error": "credit balance exhausted"},
        )
        result = await self.client.check(
            "inference",
            company={"id": "co_1"},
            options=CheckOptions(usage=50, on_acquire_failure="fail-open", default_value=True),
        )
        assert result.allowed is False
        assert result.value is False
        assert result.reason == INSUFFICIENT_CREDITS_REASON
        assert result.error == "credit balance exhausted"
        assert result.reservation is None

    async def test_fails_closed_when_check_and_reserve_errors(self):
        self.client.features.check_and_reserve_flag.side_effect = Exception("ECONNRESET")
        result = await self.client.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50))
        assert result.allowed is False
        assert result.reason == "server_reservation_failed"
        assert result.error == "server_reservation_failed"

    async def test_fails_open_to_the_per_check_default_value(self):
        self.client.features.check_and_reserve_flag.side_effect = Exception("ECONNRESET")
        result = await self.client.check(
            "inference",
            company={"id": "co_1"},
            options=CheckOptions(usage=50, on_acquire_failure="fail-open", default_value=True),
        )
        assert result.allowed is True
        assert result.reason == "server_reservation_failed_fail_open"
        assert result.error == "server_reservation_failed"

    async def test_fails_open_to_the_client_level_flag_default(self):
        client = _async_server_client(flag_defaults={"inference": True})
        try:
            client.features.check_and_reserve_flag.side_effect = Exception("ECONNRESET")
            result = await client.check(
                "inference", company={"id": "co_1"}, options=CheckOptions(usage=50, on_acquire_failure="fail-open"),
            )
            assert result.allowed is True
            assert result.reason == "server_reservation_failed_fail_open"
        finally:
            await client.event_buffer.stop()

        self.client.features.check_and_reserve_flag.side_effect = Exception("ECONNRESET")
        denied = await self.client.check(
            "inference", company={"id": "co_1"}, options=CheckOptions(usage=50, on_acquire_failure="fail-open"),
        )
        assert denied.allowed is False

    async def test_zero_usage_falls_back_to_a_plain_check(self):
        result = await self.client.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=0))
        self.client.features.check_and_reserve_flag.assert_not_called()
        self.client.features.check_flag.assert_called_once()
        assert result.allowed is True
        assert result.reason == "plain check"
        assert result.reservation is None

    async def test_invalid_usage_resolves_through_the_failure_contract(self):
        for usage in (-5, float("nan"), float("inf"), True):
            denied = await self.client.check(
                "inference", company={"id": "co_1"}, options=CheckOptions(usage=usage),  # type: ignore[arg-type]
            )
            assert denied.allowed is False
            assert denied.reason == "invalid_usage"
            assert denied.error == "invalid_usage"

        opened = await self.client.check(
            "inference",
            company={"id": "co_1"},
            options=CheckOptions(usage=-5, on_acquire_failure="fail-open", default_value=True),
        )
        assert opened.allowed is True
        assert opened.reason == "invalid_usage_fail_open"

        self.client.features.check_and_reserve_flag.assert_not_called()
        self.client.features.check_flag.assert_not_called()

    async def test_releases_a_hold_that_names_no_event_subtype(self):
        self.client.features.check_and_reserve_flag.return_value = _reserve_response(
            reservation=_held_reservation(id="rsv_orphan", event_subtype=None),
        )
        result = await self.client.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50))
        self.client.credits.release_credit_reservation.assert_awaited_once_with("rsv_orphan")
        assert result.allowed is False
        assert result.reason == "missing_event_subtype"
        assert result.reservation is None

    async def test_a_failed_release_is_swallowed(self):
        self.client.features.check_and_reserve_flag.return_value = _reserve_response(
            reservation=_held_reservation(id="rsv_orphan", event_subtype=None),
        )
        self.client.credits.release_credit_reservation.side_effect = Exception("boom")
        result = await self.client.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50))
        assert result.reason == "missing_event_subtype"
        self.client.logger.warning.assert_called()

    async def test_a_released_hold_keeps_the_server_verdict_when_failing_open(self):
        self.client.features.check_and_reserve_flag.return_value = _reserve_response(
            reservation=_held_reservation(id="rsv_orphan", event_subtype=None),
        )
        result = await self.client.check(
            "inference", company={"id": "co_1"}, options=CheckOptions(usage=50, on_acquire_failure="fail-open"),
        )
        self.client.credits.release_credit_reservation.assert_awaited_once_with("rsv_orphan")
        # The server evaluated the flag and allowed it; only the settle is
        # impossible, and fail-open assumes the credits are there.
        assert result.allowed is True
        assert result.value is True
        assert result.reason == "matched"
        assert result.flag_id == "flag_1"
        assert result.entitlement == CREDIT_ENTITLEMENT
        assert result.error == "missing_event_subtype"
        assert result.reservation is None

    async def test_no_credit_lease_config_falls_back_to_a_plain_check(self):
        client = _async_server_client(credit_leases=None)
        try:
            result = await client.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50))
            client.features.check_and_reserve_flag.assert_not_called()
            client.features.check_flag.assert_called_once()
            assert result.reservation is None
            assert client.features.check_flag.call_args.kwargs["preflight"] == PreflightRequestBody(usage=50)
        finally:
            await client.event_buffer.stop()

    async def test_client_mode_falls_back_and_warns_at_construction(self):
        client = _async_server_client(credit_leases=CreditLeaseConfig(mode="client"))
        try:
            warning = " ".join(str(call.args[0]) for call in client.logger.warning.call_args_list)
            assert "'client'" in warning
            result = await client.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50))
            client.features.check_and_reserve_flag.assert_not_called()
            client.features.check_flag.assert_called_once()
            assert result.reservation is None
        finally:
            await client.event_buffer.stop()

    async def test_offline_check_returns_the_flag_default(self):
        client = _async_server_client(offline=True, flag_defaults={"inference": True})
        try:
            result = await client.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50))
            client.features.check_and_reserve_flag.assert_not_called()
            assert result.allowed is True
            assert result.reason == REASON_OFFLINE
            assert result.reservation is None
        finally:
            await client.event_buffer.stop()

    async def _reservation_handle(self) -> Reservation:
        result = await self.client.check(
            "inference",
            company={"id": "co_1"},
            user={"id": "user_1"},
            options=CheckOptions(usage=50, event_subtype="inference_tokens"),
        )
        assert result.reservation is not None
        return result.reservation

    async def test_track_with_reservation_settles_by_reservation_id(self):
        reservation = await self._reservation_handle()
        with patch.object(self.client.event_buffer, "push", new=AsyncMock()) as mock_push:
            await self.client.track_with_reservation(
                reservation, 20, TrackWithReservationOptions(traits={"model": "opus"}),
            )

        pushed = mock_push.call_args.args[0]
        assert pushed.event_type == "track"
        assert pushed.body.event == "inference_tokens"
        assert pushed.body.quantity == 20
        assert pushed.body.reservation_id == "rsv_1"
        assert pushed.body.lease_id is None
        assert pushed.body.company == {"id": "co_1"}
        assert pushed.body.user == {"id": "user_1"}
        assert pushed.body.traits == {"model": "opus"}
        assert pushed.idempotency_key == "lease-reservation:rsv_1"

    async def test_track_with_reservation_updates_datastream_company_metrics(self):
        reservation = await self._reservation_handle()
        mock_ds = MagicMock()
        mock_ds.is_connected = MagicMock(return_value=True)
        mock_ds.update_company_metrics = AsyncMock()
        self.client._datastream_client = mock_ds

        with patch.object(self.client.event_buffer, "push", new=AsyncMock()):
            await self.client.track_with_reservation(reservation, 20)

        mock_ds.update_company_metrics.assert_awaited_once_with({"id": "co_1"}, "inference_tokens", 20)

    async def test_track_with_reservation_skips_an_invalid_quantity(self):
        reservation = await self._reservation_handle()
        with patch.object(self.client.event_buffer, "push", new=AsyncMock()) as mock_push:
            for quantity in (-1, float("nan"), float("inf"), True):
                await self.client.track_with_reservation(reservation, quantity)  # type: ignore[arg-type]
        mock_push.assert_not_called()

    async def test_track_with_reservation_settles_a_fractional_quantity_as_a_whole_unit(self):
        reservation = await self._reservation_handle()
        with patch.object(self.client.event_buffer, "push", new=AsyncMock()) as mock_push:
            await self.client.track_with_reservation(reservation, 0.5)
        # A track event's quantity is an integer, so a partial unit bills as one.
        assert mock_push.call_args.args[0].body.quantity == 1

    async def test_track_with_reservation_without_a_hold_says_to_use_track(self):
        with patch.object(self.client.event_buffer, "push", new=AsyncMock()) as mock_push:
            await self.client.track_with_reservation(None, 5)
        mock_push.assert_not_called()
        assert "track()" in str(self.client.logger.error.call_args.args[0])

    async def test_track_with_reservation_is_a_no_op_when_offline(self):
        reservation = await self._reservation_handle()
        self.client.offline = True
        with patch.object(self.client.event_buffer, "push", new=AsyncMock()) as mock_push:
            await self.client.track_with_reservation(reservation, 20)
        mock_push.assert_not_called()


LEASE_PROBE = {
    "value": True,
    "reason": "probe",
    "entitlement": {
        "value_type": "credit",
        "credit_id": "bilcr_inference",
        "consumption_rate": 10,
        "event_subtype": "inference_tokens",
    },
}
LEASE_GATE = {"value": True, "reason": "matched"}


def _lease_datastream(results: list, **overrides) -> ScriptedDataStream:
    """A DataStream stub carrying a scripted engine, wired for the client."""
    datastream = ScriptedDataStream(
        ScriptedEngine(results, "inference"),
        "inference",
        {"id": "co_1", "credit_balances": {"bilcr_inference": 5000}},
        **overrides,
    )
    datastream.is_connected = MagicMock(return_value=True)  # type: ignore[attr-defined]
    datastream.close = AsyncMock()  # type: ignore[attr-defined]
    datastream.update_company_metrics = AsyncMock()  # type: ignore[attr-defined]
    return datastream


def _lease_grant(lease_id: str = "lse_1", granted_amount: float = 1000.0) -> MagicMock:
    return MagicMock(
        data=MagicMock(
            id=lease_id,
            company_id="co_1",
            credit_type_id="bilcr_inference",
            granted_amount=granted_amount,
            expires_at=dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=300),
        )
    )


def _async_lease_client(**config_overrides) -> AsyncSchematic:
    config_kwargs = dict(
        event_buffer_period=1,
        logger=MagicMock(),
        httpx_client=MagicMock(spec=AsyncClient),
        use_datastream=True,
        credit_leases=CreditLeaseConfig(default_lease_size=1000.0, sweep_interval=60.0),
    )
    config_kwargs.update(config_overrides)
    client = AsyncSchematic("test_key", AsyncSchematicConfig(**config_kwargs))  # type: ignore[arg-type]
    client.features.check_and_reserve_flag = AsyncMock(return_value=_reserve_response())
    client.features.check_flag = AsyncMock(
        return_value=MagicMock(data=CheckFlagResponseData(value=True, flag="inference", reason="plain check"))
    )
    client.credits.acquire_credit_lease = AsyncMock(return_value=_lease_grant())
    client.credits.extend_credit_lease = AsyncMock(return_value=_lease_grant())
    client.credits.release_credit_lease = AsyncMock()
    client.flag_check_cache_providers = []
    return client


@pytest.mark.asyncio
class TestAsyncSchematicClientLeases:
    """Routing, settling, prewarming, and shutdown with client-mode leases."""

    async def _drain(self, client: AsyncSchematic) -> None:
        if client._lease_manager is not None:
            await client._lease_manager._drain_background()
        await client.event_buffer.stop()

    async def _check(self, client: AsyncSchematic, **option_overrides) -> Any:
        options = CheckOptions(usage=50, event_subtype="inference_tokens")
        for name, value in option_overrides.items():
            setattr(options, name, value)
        return await client.check("inference", company={"id": "co_1"}, options=options)

    async def test_auto_with_datastream_gates_on_a_local_lease(self):
        client = _async_lease_client()
        client._datastream_client = _lease_datastream([LEASE_PROBE, LEASE_GATE])
        try:
            result = await self._check(client)
            assert result.allowed is True
            assert result.reservation is not None
            assert result.reservation.mode == "client"
            assert result.reservation.lease_id == "lse_1"
            assert result.reservation.credits_reserved == 500
            client.credits.acquire_credit_lease.assert_awaited_once()
            client.features.check_and_reserve_flag.assert_not_called()
        finally:
            await self._drain(client)

    async def test_auto_falls_back_to_server_mode_when_datastream_fails_to_start(self):
        client = _async_lease_client()
        client._datastream_client.start = AsyncMock(side_effect=RuntimeError("no socket"))  # type: ignore[union-attr]
        try:
            await client.initialize()
            assert client._datastream_client is None
            result = await self._check(client)
            # The plumbing is built but unusable without DataStream, so the
            # check gates over the API rather than going ungated.
            client.features.check_and_reserve_flag.assert_awaited_once()
            client.credits.acquire_credit_lease.assert_not_awaited()
            assert result.reservation is not None
            assert result.reservation.mode == "server"
        finally:
            await self._drain(client)

    async def test_client_mode_without_datastream_checks_plainly_and_warns(self):
        client = _async_lease_client(use_datastream=False, credit_leases=CreditLeaseConfig(mode="client"))
        try:
            warnings = " ".join(str(call.args[0]) for call in client.logger.warning.call_args_list)
            assert "DataStream is not enabled" in warnings
            result = await self._check(client)
            assert result.reservation is None
            client.credits.acquire_credit_lease.assert_not_awaited()
            client.features.check_and_reserve_flag.assert_not_called()
            client.features.check_flag.assert_awaited_once()
        finally:
            await self._drain(client)

    async def test_server_mode_warns_about_the_client_only_options(self):
        client = _async_lease_client(
            use_datastream=False,
            credit_leases=CreditLeaseConfig(
                mode="server",
                default_lease_size=500.0,
                overrides={"bilcr_inference": LeaseConfigOverride(lease_size=10.0)},
            ),
        )
        try:
            warnings = " ".join(str(call.args[0]) for call in client.logger.warning.call_args_list)
            assert "default_lease_size" in warnings
            assert "overrides" in warnings
            assert client._lease_manager is None
            assert client._lease_store is None
        finally:
            await self._drain(client)

    async def test_auto_without_datastream_warns_about_the_client_only_options(self):
        client = _async_lease_client(
            use_datastream=False,
            credit_leases=CreditLeaseConfig(default_lease_size=500.0, sweep_interval=60.0),
        )
        try:
            warnings = " ".join(str(call.args[0]) for call in client.logger.warning.call_args_list)
            assert "resolves to server mode" in warnings
            assert "default_lease_size" in warnings
        finally:
            await self._drain(client)

    async def test_auto_with_datastream_keeps_the_client_only_options(self):
        client = _async_lease_client()
        try:
            warnings = " ".join(str(call.args[0]) for call in client.logger.warning.call_args_list)
            assert "resolves to server mode" not in warnings
        finally:
            await self._drain(client)

    async def test_no_shared_backend_warns_that_gating_is_per_process(self):
        client = _async_lease_client()
        try:
            warnings = " ".join(str(call.args[0]) for call in client.logger.warning.call_args_list)
            assert "without a shared Redis backend" in warnings
        finally:
            await self._drain(client)

    async def test_track_with_reservation_settles_the_local_hold(self):
        client = _async_lease_client()
        client._datastream_client = _lease_datastream([LEASE_PROBE, LEASE_GATE])
        try:
            result = await self._check(client)
            assert result.reservation is not None
            with patch.object(client.event_buffer, "push", new=AsyncMock()) as mock_push:
                await client.track_with_reservation(result.reservation, 20)

            pushed = mock_push.call_args.args[0]
            assert pushed.body.event == "inference_tokens"
            assert pushed.body.quantity == 20
            assert pushed.body.lease_id == "lse_1"
            assert pushed.body.reservation_id is None
            assert pushed.idempotency_key == f"lease-reservation:{result.reservation.id}"
            # 1000 granted, 500 held, 200 of it actually consumed.
            entry = await client._lease_store.get("co_1", "bilcr_inference")
            assert entry is not None and entry.local_remaining_credits == 800
        finally:
            await self._drain(client)

    async def test_track_with_reservation_emits_even_when_the_settle_raises(self):
        client = _async_lease_client()
        client._datastream_client = _lease_datastream([LEASE_PROBE, LEASE_GATE])
        try:
            result = await self._check(client)
            assert result.reservation is not None
            client._reservations.consume = AsyncMock(side_effect=RuntimeError("redis down"))
            with patch.object(client.event_buffer, "push", new=AsyncMock()) as mock_push:
                await client.track_with_reservation(result.reservation, 7)

            # The server is the source of truth for consumption, so the usage
            # is billed whatever the local bookkeeping did.
            pushed = mock_push.call_args.args[0]
            assert pushed.body.quantity == 7
            assert pushed.body.lease_id == "lse_1"
            assert pushed.idempotency_key == f"lease-reservation:{result.reservation.id}"
        finally:
            await self._drain(client)

    async def test_an_unconfigured_client_still_bills_a_client_mode_handle(self):
        client = _async_lease_client(credit_leases=None)
        reservation = Reservation(
            id="res_orphan",
            lease_id="lse_x",
            mode="client",
            company_id="co_1",
            credit_type_id="bilcr_inference",
            event_subtype="inference_tokens",
            quantity_reserved=10,
            credits_reserved=100,
            consumption_rate=10,
            expires_at=dt.datetime.now(dt.timezone.utc),
            company={"id": "co_1"},
        )
        try:
            with patch.object(client.event_buffer, "push", new=AsyncMock()) as mock_push:
                await client.track_with_reservation(reservation, 7)
            pushed = mock_push.call_args.args[0]
            assert pushed.body.lease_id == "lse_x"
            assert pushed.idempotency_key == "lease-reservation:res_orphan"
        finally:
            await self._drain(client)

    async def test_prewarm_acquires_a_lease_per_credit_type(self):
        client = _async_lease_client()
        client._datastream_client = _lease_datastream([])
        try:
            await client.prewarm({"id": "co_1"}, ["bilcr_inference"])
            client.credits.acquire_credit_lease.assert_awaited_once()
            assert client.credits.acquire_credit_lease.call_args.kwargs["credit_type_id"] == "bilcr_inference"
        finally:
            await self._drain(client)

    async def test_prewarm_resolves_a_company_that_carries_only_secondary_keys(self):
        client = _async_lease_client()
        client._datastream_client = _lease_datastream([])
        try:
            await client.prewarm({"external_id": "ext-co-1"}, ["bilcr_inference"])
            client.credits.acquire_credit_lease.assert_awaited_once()
            assert client.credits.acquire_credit_lease.call_args.kwargs["company_id"] == "co_1"
        finally:
            await self._drain(client)

    async def test_prewarm_gives_up_when_the_company_never_surfaces(self):
        client = _async_lease_client(
            credit_leases=CreditLeaseConfig(default_lease_size=1000.0, prewarm_resolve_timeout=0.05)
        )
        client._datastream_client = _lease_datastream(
            [], company_error=RuntimeError("DataStream client is not connected")
        )
        try:
            await client.prewarm({"external_id": "ext-co-missing"}, ["bilcr_inference"])
            client.credits.acquire_credit_lease.assert_not_awaited()
        finally:
            await self._drain(client)

    async def test_prewarm_with_no_wait_still_warms_a_cached_company(self):
        client = _async_lease_client(
            credit_leases=CreditLeaseConfig(default_lease_size=1000.0, prewarm_resolve_timeout=0)
        )
        # The fetch would fail, so only the cache can answer here.
        client._datastream_client = _lease_datastream(
            [], company_cached=True, company_error=RuntimeError("DataStream client is not connected")
        )
        try:
            await client.prewarm({"external_id": "ext-co-1"}, ["bilcr_inference"])
            client.credits.acquire_credit_lease.assert_awaited_once()
            assert client.credits.acquire_credit_lease.call_args.kwargs["company_id"] == "co_1"
        finally:
            await self._drain(client)

    async def test_prewarm_with_no_wait_gives_up_on_an_uncached_company(self):
        client = _async_lease_client(
            credit_leases=CreditLeaseConfig(default_lease_size=1000.0, prewarm_resolve_timeout=0)
        )
        client._datastream_client = _lease_datastream([])
        try:
            await client.prewarm({"external_id": "ext-co-1"}, ["bilcr_inference"])
            client.credits.acquire_credit_lease.assert_not_awaited()
        finally:
            await self._drain(client)

    async def test_prewarm_resolves_an_account_defined_id_key_through_the_cache(self):
        # The account's own identifier happens to live under a key named `id`.
        # It is an ordinary entity key, so the lookup decides.
        client = _async_lease_client(
            credit_leases=CreditLeaseConfig(default_lease_size=1000.0, prewarm_resolve_timeout=0)
        )
        client._datastream_client = _lease_datastream([], company_cached=True)
        try:
            await client.prewarm({"id": "acme"}, ["bilcr_inference"])
            client.credits.acquire_credit_lease.assert_awaited_once()
            assert client.credits.acquire_credit_lease.call_args.kwargs["company_id"] == "co_1"
        finally:
            await self._drain(client)

    async def test_prewarm_falls_back_to_a_comp_prefixed_value_when_the_keys_miss(self):
        client = _async_lease_client(
            credit_leases=CreditLeaseConfig(default_lease_size=1000.0, prewarm_resolve_timeout=0)
        )
        client._datastream_client = _lease_datastream([])
        try:
            await client.prewarm({"account_id": "comp_1"}, ["bilcr_inference"])
            client.credits.acquire_credit_lease.assert_awaited_once()
            assert client.credits.acquire_credit_lease.call_args.kwargs["company_id"] == "comp_1"
        finally:
            await self._drain(client)

    async def test_prewarm_resolves_nothing_when_the_keys_miss_and_carry_no_schematic_id(self):
        client = _async_lease_client(
            credit_leases=CreditLeaseConfig(default_lease_size=1000.0, prewarm_resolve_timeout=0)
        )
        client._datastream_client = _lease_datastream([])
        try:
            await client.prewarm({"id": "acme"}, ["bilcr_inference"])
            client.credits.acquire_credit_lease.assert_not_awaited()
        finally:
            await self._drain(client)

    async def test_prewarm_is_a_no_op_in_server_mode(self):
        client = _async_server_client()
        try:
            await client.prewarm({"id": "co_1"}, ["bilcr_inference"])
            debug = " ".join(str(call.args[0]) for call in client.logger.debug.call_args_list)
            assert "no-op in server mode" in debug
        finally:
            await client.event_buffer.stop()

    async def test_identify_kicks_off_a_prewarm(self):
        client = _async_lease_client()
        client.prewarm = AsyncMock()  # type: ignore[method-assign]
        try:
            with patch.object(client.event_buffer, "push", new=AsyncMock()):
                await client.identify(
                    {"id": "user_1"},
                    company=EventBodyIdentifyCompany(keys={"id": "co_1"}),
                    options=IdentifyOptions(prewarm=["bilcr_inference"]),
                )
            await asyncio.sleep(0)
            await asyncio.sleep(0)
            client.prewarm.assert_awaited_once_with({"id": "co_1"}, ["bilcr_inference"])
        finally:
            await self._drain(client)

    async def test_identify_without_prewarm_warms_nothing(self):
        client = _async_lease_client()
        client.prewarm = AsyncMock()  # type: ignore[method-assign]
        try:
            with patch.object(client.event_buffer, "push", new=AsyncMock()):
                await client.identify({"id": "user_1"}, company=EventBodyIdentifyCompany(keys={"id": "co_1"}))
            await asyncio.sleep(0)
            client.prewarm.assert_not_awaited()
        finally:
            await self._drain(client)

    async def test_identify_flushes_the_buffer_before_prewarming(self):
        client = _async_lease_client()
        client.prewarm = AsyncMock()  # type: ignore[method-assign]
        try:
            with patch.object(client.event_buffer, "push", new=AsyncMock()):
                with patch.object(client.event_buffer, "flush", new=AsyncMock()) as mock_flush:
                    await client.identify(
                        {"id": "user_1"},
                        company=EventBodyIdentifyCompany(keys={"id": "co_1"}),
                        options=IdentifyOptions(prewarm=["bilcr_inference"]),
                    )
                    # The prewarm polls for the company this identify creates,
                    # so the identify has to be on the wire before it starts.
                    mock_flush.assert_awaited_once()
                    client.prewarm.assert_not_awaited()
            await asyncio.sleep(0)
            await asyncio.sleep(0)
            client.prewarm.assert_awaited_once_with({"id": "co_1"}, ["bilcr_inference"])
        finally:
            await self._drain(client)

    async def test_identify_prewarms_even_when_the_flush_fails(self):
        client = _async_lease_client()
        client.prewarm = AsyncMock()  # type: ignore[method-assign]
        try:
            with patch.object(client.event_buffer, "push", new=AsyncMock()):
                with patch.object(
                    client.event_buffer, "flush", new=AsyncMock(side_effect=RuntimeError("api down"))
                ):
                    await client.identify(
                        {"id": "user_1"},
                        company=EventBodyIdentifyCompany(keys={"id": "co_1"}),
                        options=IdentifyOptions(prewarm=["bilcr_inference"]),
                    )
            await asyncio.sleep(0)
            await asyncio.sleep(0)
            client.prewarm.assert_awaited_once_with({"id": "co_1"}, ["bilcr_inference"])
        finally:
            await self._drain(client)

    async def test_a_lease_gated_check_reports_one_flag_check_event(self):
        client = _async_lease_client()
        client._datastream_client = _lease_datastream([LEASE_PROBE, LEASE_GATE])
        try:
            with patch.object(client.event_buffer, "push", new=AsyncMock()) as mock_push:
                result = await self._check(client)
            assert result.allowed is True
            events = [call.args[0] for call in mock_push.call_args_list]
            assert [event.event_type for event in events] == ["flag_check"]
            body = events[0].body
            assert body.flag_key == "inference"
            assert body.value is True
            assert body.reason == "matched"
            assert body.company_id == "co_1"
            assert body.req_company == {"id": "co_1"}
        finally:
            await self._drain(client)

    async def test_client_mode_keeps_a_reservation_ttl_past_the_server_cap(self):
        client = _async_lease_client(
            credit_leases=CreditLeaseConfig(
                mode="client", default_lease_size=1000.0, default_reservation_ttl=7200.0
            )
        )
        try:
            # The TTL only drives the local sweeper here, so the server's cap
            # does not apply and nothing is clamped or warned about.
            assert client._reservation_ttl == 7200.0
            assert client._lease_manager.resolve_config("bilcr_inference").reservation_ttl == 7200.0
            warning = " ".join(str(call.args[0]) for call in client.logger.warning.call_args_list)
            assert "one hour cap" not in warning
        finally:
            await self._drain(client)

    async def test_shutdown_stops_the_sweep_and_releases_a_per_process_lease(self):
        client = _async_lease_client()
        client._datastream_client = _lease_datastream([LEASE_PROBE, LEASE_GATE])
        await self._check(client)
        client._lease_manager.start_sweep()
        assert client._lease_manager._sweep_task is not None

        await client.shutdown()

        assert client._lease_manager._sweep_task is None
        client.credits.release_credit_lease.assert_awaited_once_with("lse_1", request_options=None)

    async def test_shutdown_releases_a_lease_an_in_flight_prewarm_installs(self):
        # The prewarm's acquire is on the wire when shutdown starts. Cancelling
        # the prewarm cancels its shield, not the acquire, so the lease still
        # lands: shutdown has to drain it before listing the store, or nothing
        # releases it and the credits stay held until server-side expiry.
        client = _async_lease_client()
        client._datastream_client = _lease_datastream([])
        on_the_wire = asyncio.Event()

        async def slow_acquire(**kwargs):
            on_the_wire.set()
            await asyncio.sleep(0.05)
            return _lease_grant()

        client.credits.acquire_credit_lease = AsyncMock(side_effect=slow_acquire)

        client._spawn_prewarm({"id": "co_1"}, ["bilcr_inference"])
        await asyncio.wait_for(on_the_wire.wait(), 1)
        await client.shutdown()
        # An untracked acquire would install here, behind the release.
        await asyncio.sleep(0.1)

        assert client._lease_store.list_leases() == []
        client.credits.release_credit_lease.assert_awaited_once_with("lse_1", request_options=None)

    async def test_prewarm_started_during_shutdown_acquires_nothing(self):
        client = _async_lease_client()
        client._datastream_client = _lease_datastream([])
        try:
            client._is_shutting_down = True
            await client.prewarm({"id": "co_1"}, ["bilcr_inference"])
            client.credits.acquire_credit_lease.assert_not_awaited()
        finally:
            await self._drain(client)

    async def test_shutdown_returns_within_the_budget_when_a_release_never_lands(self):
        client = _async_lease_client()
        await client._lease_store.replace(
            lease_id="lse_1",
            company_id="co_1",
            credit_type_id="bilcr_inference",
            granted_amount=1000,
            expires_at=time.time() + 300,
        )

        async def never(*args, **kwargs):
            await asyncio.Event().wait()

        client.credits.release_credit_lease = AsyncMock(side_effect=never)

        with patch("schematic.client.SHUTDOWN_DRAIN_TIMEOUT", 0.05):
            started = time.monotonic()
            await client.shutdown()

        # The drain and the release share one budget, so a wire call that never
        # lands cannot hold a closing client open.
        assert time.monotonic() - started < 1


    async def test_shutdown_leaves_a_shared_lease_for_the_pods_still_drawing_on_it(self):
        redis_client = make_fake_redis()
        client = _async_lease_client(
            credit_leases=CreditLeaseConfig(default_lease_size=1000.0, redis_client=redis_client)
        )
        assert client._lease_backend_shared is True
        await client._lease_store.replace(
            lease_id="lse_shared",
            company_id="co_1",
            credit_type_id="bilcr_inference",
            granted_amount=1000,
            expires_at=time.time() + 300,
        )

        await client.shutdown()

        client.credits.release_credit_lease.assert_not_awaited()
        survivor = await client._lease_store.get("co_1", "bilcr_inference")
        assert survivor is not None and survivor.lease_id == "lse_shared"

    async def test_a_redis_backed_datastream_cache_backs_the_leases_too(self):
        redis_client = make_fake_redis()
        client = _async_lease_client(
            datastream=DataStreamConfig(company_cache=RedisCache(redis_client, prefix="acme")),
        )
        try:
            assert client._lease_backend_shared is True
            assert type(client._lease_store).__name__ == "RedisLeaseStore"
            assert type(client._reservations).__name__ == "RedisReservationStore"
        finally:
            await self._drain(client)


class TestSchematicClientModeWarning(unittest.TestCase):
    """The sync client cannot run client mode, and says so."""

    def test_client_mode_points_at_the_async_client(self):
        logger = MagicMock()
        client = Schematic(
            "api_key",
            SchematicConfig(
                event_buffer_period=1,
                logger=logger,
                httpx_client=MagicMock(spec=Client),
                credit_leases=CreditLeaseConfig(mode="client"),
            ),
        )
        try:
            warnings = " ".join(str(call.args[0]) for call in logger.warning.call_args_list)
            self.assertIn("AsyncSchematic", warnings)
            self.assertIsNone(client._effective_lease_mode())
        finally:
            client.event_buffer.stop()


    def test_auto_warns_about_the_client_only_options_too(self):
        # Every 'auto' on the sync client resolves to server mode, so the
        # client-only knobs are just as ignored as under an explicit 'server'.
        logger = MagicMock()
        client = Schematic(
            "api_key",
            SchematicConfig(
                event_buffer_period=1,
                logger=logger,
                httpx_client=MagicMock(spec=Client),
                credit_leases=CreditLeaseConfig(default_lease_size=500.0),
            ),
        )
        try:
            warnings = " ".join(str(call.args[0]) for call in logger.warning.call_args_list)
            self.assertIn("resolves to server mode", warnings)
            self.assertIn("default_lease_size", warnings)
        finally:
            client.event_buffer.stop()


class _ReserveTransport(MockTransport):
    """Replays a queue of status codes in order, recording each request body."""

    def __init__(self, statuses):
        self.bodies = []
        self._statuses = list(statuses)
        super().__init__(self._handle)

    def _handle(self, request):
        self.bodies.append(json.loads(request.content) if request.content else {})
        status = self._statuses.pop(0) if self._statuses else 200
        if status >= 400:
            return Response(status, json={"error": "upstream is unhappy"})
        return Response(status, json=_reserve_body())


def _reserve_body():
    expires_at = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=TTL_SECONDS)).isoformat()
    return {
        "data": {
            "flag": "inference",
            "flag_id": "flag_1",
            "value": True,
            "reason": "matched",
            "company_id": "co_1",
            "entitlement": {"feature_id": "feat", "feature_key": "inference", "value_type": "credit"},
            "reservation": {
                "id": "rsv_1",
                "company_id": "co_1",
                "credit_type_id": "bilcr_inference",
                "consumption_rate": 10.0,
                "credits_reserved": 500.0,
                "quantity_reserved": 50.0,
                "event_subtype": "inference_tokens",
                "expires_at": expires_at,
            },
        },
        "params": {},
    }


class TestServerReservationRetries(unittest.TestCase):
    """check() in server mode across the SDK's own retry policy.

    These drive the generated features client over a mock transport rather
    than a stubbed method, because what they pin is the retry loop itself:
    which body each attempt carries, and what the check makes of the attempt
    that finally succeeds.
    """

    def setUp(self):
        # The retry policy sleeps a second before its first retry, which no
        # test needs to sit through.
        self._delay = patch.object(core_http_client, "INITIAL_RETRY_DELAY_SECONDS", 0.001)
        self._delay.start()
        self.addCleanup(self._delay.stop)

    def _client(self, transport) -> Schematic:
        client = Schematic(
            "api_key",
            SchematicConfig(
                event_buffer_period=1,
                logger=MagicMock(),
                httpx_client=Client(transport=transport),
                credit_leases=CreditLeaseConfig(mode="server", default_reservation_ttl=TTL_SECONDS),
            ),
        )
        self.addCleanup(client.event_buffer.stop)
        client.flag_check_cache_providers = []
        return client

    def test_a_retried_check_repeats_its_key_and_holds_once(self):
        transport = _ReserveTransport([502, 200])
        client = self._client(transport)

        result = client.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50))

        self.assertEqual(len(transport.bodies), 2)
        keys = [body["idempotency_key"] for body in transport.bodies]
        self.assertEqual(keys[0], keys[1])
        self.assertTrue(result.allowed)
        assert result.reservation is not None
        self.assertEqual(result.reservation.id, "rsv_1")

    def test_the_next_check_carries_a_different_key(self):
        transport = _ReserveTransport([502, 200, 200])
        client = self._client(transport)

        client.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50))
        client.check("inference", company={"id": "co_1"}, options=CheckOptions(usage=50))

        keys = [body["idempotency_key"] for body in transport.bodies]
        self.assertEqual(len(keys), 3)
        self.assertEqual(keys[0], keys[1])
        self.assertNotEqual(keys[1], keys[2])


if __name__ == "__main__":
    unittest.main()
