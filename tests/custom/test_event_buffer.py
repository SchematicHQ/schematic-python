import unittest
from unittest.mock import MagicMock, patch

import pytest

from schematic.event_buffer import AsyncEventBuffer, EventBuffer
from schematic.types import CreateEventRequestBody


class TestEventBuffer(unittest.TestCase):

    def setUp(self):
        self.mock_api = MagicMock()
        self.mock_logger = MagicMock()
        self.event_buffer = EventBuffer(
            events_api=self.mock_api, logger=self.mock_logger, period=1, max_events=5
        )

    def tearDown(self):
        self.event_buffer.stop()

    def test_push_event(self):
        event = MagicMock(spec=CreateEventRequestBody)

        self.event_buffer.push(event)
        self.assertEqual(len(self.event_buffer.events), 1)

    def test_push_event_exceeding_max_events(self):
        event = MagicMock(spec=CreateEventRequestBody)

        with patch.object(self.event_buffer, "_flush") as mock_flush:
            for _ in range(5):
                self.event_buffer.push(event)
            self.assertEqual(len(self.event_buffer.events), 5)

            # Pushing one more event should trigger a flush
            self.event_buffer.push(event)
            mock_flush.assert_called_once()

    def test_flush(self):
        event = MagicMock(spec=CreateEventRequestBody)
        self.event_buffer.events = [event]

        self.event_buffer._flush()
        self.mock_api.create_event_batch.assert_called_once_with(events=[event])
        self.assertEqual(len(self.event_buffer.events), 0)

    def test_stop(self):
        with patch.object(self.event_buffer.flush_thread, "join"):
            self.event_buffer.stop()
            self.assertTrue(self.event_buffer.shutdown.is_set())


@pytest.mark.asyncio
class TestAsyncEventBuffer:

    @pytest.fixture(autouse=True)
    async def setup_and_teardown(self):
        self.mock_api = MagicMock()
        self.mock_logger = MagicMock()
        self.async_event_buffer = AsyncEventBuffer(
            events_api=self.mock_api, logger=self.mock_logger, period=1, max_events=5
        )
        yield
        await self.async_event_buffer.stop()

    async def test_push_event(self):
        event = MagicMock(spec=CreateEventRequestBody)

        await self.async_event_buffer.push(event)
        assert len(self.async_event_buffer.events) == 1

    async def test_push_event_exceeding_max_events(self):
        event = MagicMock(spec=CreateEventRequestBody)

        with patch.object(self.async_event_buffer, "_flush") as mock_flush:
            for _ in range(5):
                await self.async_event_buffer.push(event)
            assert len(self.async_event_buffer.events) == 5

            # Pushing one more event should trigger a flush
            await self.async_event_buffer.push(event)
            mock_flush.assert_called_once()

    async def test_flush(self):
        event = MagicMock(spec=CreateEventRequestBody)
        self.async_event_buffer.events = [event]

        await self.async_event_buffer._flush()
        self.mock_api.create_event_batch.assert_called_once_with(events=[event])
        assert len(self.async_event_buffer.events) == 0

    async def test_stop(self):
        with patch.object(self.async_event_buffer.flush_task, "cancel"):
            await self.async_event_buffer.stop()
            assert self.async_event_buffer.shutdown_event.is_set()


if __name__ == "__main__":
    unittest.main()
