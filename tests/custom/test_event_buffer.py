import unittest
from unittest.mock import MagicMock, patch, call

import pytest
import asyncio

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

    async def test_push_event(self):
        # Create a separate mock and buffer instance just for this test
        mock_api = MagicMock()
        mock_logger = MagicMock()
        task_mock = MagicMock()

        # First patch create_task to avoid running periodic flush
        with patch('asyncio.create_task', return_value=task_mock):
            # Then create the buffer, which uses create_task
            buffer = AsyncEventBuffer(
                events_api=mock_api, logger=mock_logger, period=1, max_events=5
            )

            # Test push event
            event = MagicMock(spec=CreateEventRequestBody)
            await buffer.push(event)

            # Verify event was added
            assert len(buffer.events) == 1

            # Clean up
            await buffer.stop()

    async def test_push_event_exceeding_max_events(self):
        # Create a separate mock and buffer instance just for this test
        mock_api = MagicMock()
        mock_logger = MagicMock()
        task_mock = MagicMock()

        # First patch create_task to avoid running periodic flush
        with patch('asyncio.create_task', return_value=task_mock):
            # Then create the buffer, which uses create_task
            buffer = AsyncEventBuffer(
                events_api=mock_api, logger=mock_logger, period=1, max_events=5
            )

            # Setup test
            event = MagicMock(spec=CreateEventRequestBody)

            with patch.object(buffer, "_flush") as mock_flush:
                # Add events up to max
                for _ in range(5):
                    await buffer.push(event)
                assert len(buffer.events) == 5

                # Pushing one more event should trigger a flush
                await buffer.push(event)
                mock_flush.assert_called_once()

            # Clean up
            await buffer.stop()

    async def test_flush(self):
        # Create a separate mock and buffer instance just for this test
        mock_api = MagicMock()
        mock_logger = MagicMock()
        task_mock = MagicMock()

        # First patch create_task to avoid running periodic flush
        with patch('asyncio.create_task', return_value=task_mock):
            # Also patch the max_retries to 0 to disable retry behavior for this test
            buffer = AsyncEventBuffer(
                events_api=mock_api, logger=mock_logger, period=1, max_events=5,
                max_retries=0  # Disable retries for this specific test
            )

            # Setup test
            event = MagicMock(spec=CreateEventRequestBody)
            buffer.events = [event]

            # Execute the method under test
            await buffer._flush()

            # Verify expectations
            mock_api.create_event_batch.assert_called_once_with(events=[event])
            assert len(buffer.events) == 0

            # Clean up
            await buffer.stop()


    async def test_stop(self):
        # Create a separate mock and buffer instance just for this test
        mock_api = MagicMock()
        mock_logger = MagicMock()
        task_mock = MagicMock()

        # First patch create_task to avoid running periodic flush
        with patch('asyncio.create_task', return_value=task_mock):
            # Then create the buffer, which uses create_task
            buffer = AsyncEventBuffer(
                events_api=mock_api, logger=mock_logger, period=1, max_events=5
            )

            # Test stopping the buffer
            await buffer.stop()

            # Verify shutdown was set
            assert buffer.shutdown_event.is_set()
            assert buffer.stopped is True


if __name__ == "__main__":
    unittest.main()
