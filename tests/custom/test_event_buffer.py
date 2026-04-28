import threading
import time
import unittest
from unittest.mock import AsyncMock, MagicMock, patch, call

import pytest
import asyncio

from schematic.event_buffer import AsyncEventBuffer, EventBuffer
from schematic.types import CreateEventRequestBody


class TestEventBuffer(unittest.TestCase):

    def setUp(self):
        self.mock_sender = MagicMock()
        self.mock_logger = MagicMock()
        self.event_buffer = EventBuffer(
            event_sender=self.mock_sender, logger=self.mock_logger, period=1, max_events=5
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
        self.mock_sender.send_batch.assert_called_once_with([event])
        self.assertEqual(len(self.event_buffer.events), 0)


    def test_stop(self):
        with patch.object(self.event_buffer.flush_thread, "join"):
            self.event_buffer.stop()
            self.assertTrue(self.event_buffer.shutdown.is_set())

    def test_shutdown_flushes_remaining(self):
        """Corresponds to Go TestEventBuffer_ShutdownFlushesRemaining.

        Verify that stop() flushes buffered events even if batch isn't full.
        """
        mock_sender = MagicMock()
        mock_logger = MagicMock()
        buffer = EventBuffer(
            event_sender=mock_sender,
            logger=mock_logger,
            period=10,  # Long period so periodic flush won't trigger
            max_events=100,  # Large batch so auto-flush won't trigger
        )

        # Push several events (fewer than max_events so no auto-flush)
        for i in range(5):
            event = MagicMock(spec=CreateEventRequestBody)
            buffer.push(event)

        # No flush should have happened yet
        mock_sender.send_batch.assert_not_called()

        # Stop the buffer, which should flush remaining events
        buffer.stop()

        # Verify all events were flushed
        mock_sender.send_batch.assert_called_once()
        flushed_events = mock_sender.send_batch.call_args.args[0]
        self.assertEqual(len(flushed_events), 5)

    def test_push_after_shutdown_rejected(self):
        """Push after stop() should be a silent no-op (events not added).

        Mirrors Go/Node behavior — after shutdown, the buffer logs an error
        and refuses to accept new events rather than queuing them.
        """
        mock_sender = MagicMock()
        mock_logger = MagicMock()
        buffer = EventBuffer(
            event_sender=mock_sender,
            logger=mock_logger,
            period=10,
            max_events=100,
        )

        buffer.stop()

        event = MagicMock(spec=CreateEventRequestBody)
        buffer.push(event)

        self.assertEqual(len(buffer.events), 0)
        # Verify the rejection was logged at error level
        mock_logger.error.assert_called_with(
            "Event buffer is stopped, not accepting new events"
        )
        # And no API call should have been issued for the rejected event
        mock_sender.send_batch.assert_not_called()

    def test_concurrent_push(self):
        """Corresponds to Go TestEventBuffer_ConcurrentPush.

        Verify no events are lost when pushing from multiple threads.
        """
        mock_sender = MagicMock()
        mock_logger = MagicMock()
        buffer = EventBuffer(
            event_sender=mock_sender,
            logger=mock_logger,
            period=10,  # Long period to avoid periodic flush during test
            max_events=1000,  # Large batch to avoid auto-flush
        )

        num_threads = 10
        events_per_thread = 20
        total_expected = num_threads * events_per_thread
        errors = []

        def worker():
            try:
                for _ in range(events_per_thread):
                    event = MagicMock(spec=CreateEventRequestBody)
                    buffer.push(event)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker) for _ in range(num_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(errors), 0, f"Concurrent push errors: {errors}")

        # Stop to flush remaining events
        buffer.stop()

        # Count total events sent
        total_sent = sum(
            len(c.args[0])
            for c in mock_sender.send_batch.call_args_list
        )
        self.assertEqual(total_sent, total_expected)


@pytest.mark.asyncio
class TestAsyncEventBuffer:

    async def test_push_event(self):
        # Create a separate mock and buffer instance just for this test
        mock_sender = AsyncMock()
        mock_logger = MagicMock()
        task_mock = MagicMock()

        # First patch create_task to avoid running periodic flush
        with patch('asyncio.create_task', return_value=task_mock):
            # Then create the buffer, which uses create_task
            buffer = AsyncEventBuffer(
                event_sender=mock_sender, logger=mock_logger, period=1, max_events=5
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
        mock_sender = AsyncMock()
        mock_logger = MagicMock()
        task_mock = MagicMock()

        # First patch create_task to avoid running periodic flush
        with patch('asyncio.create_task', return_value=task_mock):
            # Then create the buffer, which uses create_task
            buffer = AsyncEventBuffer(
                event_sender=mock_sender, logger=mock_logger, period=1, max_events=5
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
        mock_sender = AsyncMock()
        mock_logger = MagicMock()
        task_mock = MagicMock()

        # First patch create_task to avoid running periodic flush
        with patch('asyncio.create_task', return_value=task_mock):
            # Also patch the max_retries to 0 to disable retry behavior for this test
            buffer = AsyncEventBuffer(
                event_sender=mock_sender, logger=mock_logger, period=1, max_events=5,
                max_retries=0  # Disable retries for this specific test
            )

            # Setup test
            event = MagicMock(spec=CreateEventRequestBody)
            buffer.events = [event]

            # Execute the method under test
            await buffer._flush()

            # Verify expectations
            mock_sender.send_batch.assert_called_once_with([event])
            assert len(buffer.events) == 0

            # Clean up
            await buffer.stop()


    async def test_stop(self):
        # Create a separate mock and buffer instance just for this test
        mock_sender = AsyncMock()
        mock_logger = MagicMock()
        task_mock = MagicMock()

        # First patch create_task to avoid running periodic flush
        with patch('asyncio.create_task', return_value=task_mock):
            # Then create the buffer, which uses create_task
            buffer = AsyncEventBuffer(
                event_sender=mock_sender, logger=mock_logger, period=1, max_events=5
            )

            # Test stopping the buffer
            await buffer.stop()

            # Verify shutdown was set
            assert buffer.shutdown_event.is_set()
            assert buffer.stopped is True

    async def test_shutdown_flushes_remaining(self):
        """Corresponds to Go TestEventBuffer_ShutdownFlushesRemaining (async)."""
        mock_sender = AsyncMock()
        mock_logger = MagicMock()
        task_mock = MagicMock()

        with patch('asyncio.create_task', return_value=task_mock):
            buffer = AsyncEventBuffer(
                event_sender=mock_sender,
                logger=mock_logger,
                period=10,
                max_events=100,
                max_retries=0,
            )

            # Push events (fewer than max_events)
            for _ in range(5):
                event = MagicMock(spec=CreateEventRequestBody)
                await buffer.push(event)

            mock_sender.send_batch.assert_not_called()

            # Stop should flush remaining events
            await buffer.stop()

            mock_sender.send_batch.assert_called_once()
            flushed = mock_sender.send_batch.call_args.args[0]
            assert len(flushed) == 5


    async def test_push_after_shutdown_rejected(self):
        """Async equivalent of TestEventBuffer.test_push_after_shutdown_rejected."""
        mock_sender = AsyncMock()
        mock_logger = MagicMock()
        task_mock = MagicMock()

        with patch('asyncio.create_task', return_value=task_mock):
            buffer = AsyncEventBuffer(
                event_sender=mock_sender,
                logger=mock_logger,
                period=10,
                max_events=100,
                max_retries=0,
            )

            await buffer.stop()

            event = MagicMock(spec=CreateEventRequestBody)
            await buffer.push(event)

            assert len(buffer.events) == 0
            mock_logger.error.assert_called_with(
                "Event buffer is stopped, not accepting new events"
            )
            mock_sender.send_batch.assert_not_called()


if __name__ == "__main__":
    unittest.main()
