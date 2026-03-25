import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import AsyncClient, Client

from schematic.client import (
    AsyncSchematic,
    AsyncSchematicConfig,
    CheckFlagOptions,
    Schematic,
    SchematicConfig,
)
from schematic.types import CheckFlagResponseData


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


if __name__ == "__main__":
    unittest.main()
