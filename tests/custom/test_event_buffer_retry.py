import unittest
from unittest.mock import MagicMock, patch, AsyncMock

import pytest
import asyncio

from schematic.event_buffer import AsyncEventBuffer, EventBuffer, DEFAULT_MAX_RETRIES
from schematic.types import CreateEventRequestBody


class TestEventBufferRetry(unittest.TestCase):
    """Test the retry mechanism in the synchronous EventBuffer."""

    def setUp(self):
        self.mock_api = MagicMock()
        self.mock_logger = MagicMock()
        self.event_buffer = EventBuffer(
            events_api=self.mock_api, logger=self.mock_logger, period=1, max_events=5
        )

    def tearDown(self):
        self.event_buffer.stop()

    def test_flush_with_retry(self):
        """Test that the EventBuffer retries failed API calls."""
        event = MagicMock(spec=CreateEventRequestBody)
        self.event_buffer.events = [event]

        # Configure mock to fail twice then succeed on third attempt
        self.mock_api.create_event_batch.side_effect = [
            Exception("API failure 1"),
            Exception("API failure 2"),
            None  # Success
        ]

        with patch("time.sleep") as mock_sleep:  # Mock sleep to speed up test
            self.event_buffer._flush()

            # Verify retry attempts
            self.assertEqual(self.mock_api.create_event_batch.call_count, 3)
            self.assertEqual(mock_sleep.call_count, 2)  # Sleep called twice (between retries)

            # Verify events are cleared after success
            self.assertEqual(len(self.event_buffer.events), 0)

            # Verify logging
            self.mock_logger.warning.assert_called()
            self.mock_logger.info.assert_called_with("Event batch submission succeeded after 2 retries")

    def test_exponential_backoff_timing(self):
        """Verify retry delays follow exponential backoff: delay * 2^(attempt-1) + jitter.

        With initial_retry_delay=1 and max_retries=3, expected delays are:
            attempt 1: base=1.0,  jitter ∈ [0, 0.1]
            attempt 2: base=2.0,  jitter ∈ [0, 0.2]
            attempt 3: base=4.0,  jitter ∈ [0, 0.4]

        Mirrors the spec's "Event buffer exponential backoff timing is correct"
        check item — currently missing in every SDK.
        """
        mock_api = MagicMock()
        mock_logger = MagicMock()
        buffer = EventBuffer(
            events_api=mock_api,
            logger=mock_logger,
            period=10,
            max_events=100,
            max_retries=3,
            initial_retry_delay=1,
        )

        try:
            event = MagicMock(spec=CreateEventRequestBody)
            buffer.events = [event]
            mock_api.create_event_batch.side_effect = Exception("always fails")

            sleeps = []
            with patch("time.sleep", side_effect=sleeps.append):
                buffer._flush()

            # 3 retries → 3 sleeps
            self.assertEqual(len(sleeps), 3)

            expected_bases = [1.0, 2.0, 4.0]
            for i, (sleep_duration, base) in enumerate(zip(sleeps, expected_bases)):
                # delay = base + jitter, jitter ∈ [0, 0.1 * base]
                self.assertGreaterEqual(
                    sleep_duration, base,
                    f"Attempt {i+1}: sleep {sleep_duration} should be >= base {base}",
                )
                self.assertLessEqual(
                    sleep_duration, base * 1.1,
                    f"Attempt {i+1}: sleep {sleep_duration} should be <= base*1.1 {base * 1.1}",
                )
        finally:
            buffer.stop()

    def test_flush_with_max_retries_exhausted(self):
        """Test that the EventBuffer gives up after max_retries attempts."""
        event = MagicMock(spec=CreateEventRequestBody)
        self.event_buffer.events = [event]

        # Configure mock to always fail
        self.mock_api.create_event_batch.side_effect = Exception("API failure")

        with patch("time.sleep") as mock_sleep:  # Mock sleep to speed up test
            self.event_buffer._flush()

            # Verify all retry attempts were made
            self.assertEqual(self.mock_api.create_event_batch.call_count, DEFAULT_MAX_RETRIES + 1)
            self.assertEqual(mock_sleep.call_count, DEFAULT_MAX_RETRIES)

            # Verify events are cleared even after failure
            self.assertEqual(len(self.event_buffer.events), 0)

            # Verify error is logged
            self.mock_logger.error.assert_called()


@pytest.mark.asyncio
class TestAsyncEventBufferRetry:
    """Test the retry mechanism in the asynchronous AsyncEventBuffer."""

    @pytest.fixture
    async def buffer_with_mock_periodic_flush(self):
        """Setup an AsyncEventBuffer with a mocked _periodic_flush function."""
        mock_api = AsyncMock()
        mock_logger = MagicMock()
        
        # Create the buffer
        buffer = AsyncEventBuffer(
            events_api=mock_api, logger=mock_logger, period=1, max_events=5
        )
        
        # Replace the _periodic_flush with a dummy coro that just returns immediately
        async def dummy_periodic_flush():
            pass
        
        # Patch the method and cancel the task
        with patch.object(buffer, '_periodic_flush', dummy_periodic_flush):
            buffer.flush_task.cancel()  # Cancel the original task to avoid warnings
            try:
                await buffer.flush_task
            except asyncio.CancelledError:
                pass
            
            # Create a new task with our dummy function
            buffer.flush_task = asyncio.create_task(dummy_periodic_flush())
            
            yield buffer, mock_api, mock_logger
            
            # Clean up after test
            buffer.flush_task.cancel()
            await buffer.stop()

    async def test_flush_with_retry(self, buffer_with_mock_periodic_flush):
        """Test that the AsyncEventBuffer retries failed API calls."""
        buffer, mock_api, mock_logger = buffer_with_mock_periodic_flush
        
        # Setup test data
        event = MagicMock(spec=CreateEventRequestBody)
        buffer.events = [event]
        
        # Configure mock to fail twice then succeed on third attempt
        mock_api.create_event_batch.side_effect = [
            Exception("API failure 1"),
            Exception("API failure 2"),
            None  # Success
        ]
        
        # Execute with mocked sleep
        with patch("asyncio.sleep", return_value=None) as mock_sleep:
            await buffer._flush()
            
            # Verify retry attempts
            assert mock_api.create_event_batch.call_count == 3
            assert mock_sleep.call_count == 2  # Sleep called twice (between retries)
            
            # Verify events are cleared after success
            assert len(buffer.events) == 0
            
            # Verify logging
            mock_logger.warning.assert_called()
            mock_logger.info.assert_called_with("Event batch submission succeeded after 2 retries")

    async def test_exponential_backoff_timing(self, buffer_with_mock_periodic_flush):
        """Async equivalent of TestEventBufferRetry.test_exponential_backoff_timing."""
        buffer, mock_api, _ = buffer_with_mock_periodic_flush
        # Use canonical defaults: initial_retry_delay=1, max_retries=3
        buffer.initial_retry_delay = 1
        buffer.max_retries = 3

        event = MagicMock(spec=CreateEventRequestBody)
        buffer.events = [event]
        mock_api.create_event_batch.side_effect = Exception("always fails")

        sleeps = []

        async def fake_sleep(delay):
            sleeps.append(delay)

        with patch("asyncio.sleep", side_effect=fake_sleep):
            await buffer._flush()

        assert len(sleeps) == 3
        expected_bases = [1.0, 2.0, 4.0]
        for i, (sleep_duration, base) in enumerate(zip(sleeps, expected_bases)):
            assert sleep_duration >= base, (
                f"Attempt {i+1}: sleep {sleep_duration} should be >= base {base}"
            )
            assert sleep_duration <= base * 1.1, (
                f"Attempt {i+1}: sleep {sleep_duration} should be <= base*1.1 {base * 1.1}"
            )

    async def test_flush_with_max_retries_exhausted(self, buffer_with_mock_periodic_flush):
        """Test that the AsyncEventBuffer gives up after max_retries attempts."""
        buffer, mock_api, mock_logger = buffer_with_mock_periodic_flush
        
        # Setup test data
        event = MagicMock(spec=CreateEventRequestBody)
        buffer.events = [event]
        
        # Configure mock to always fail
        mock_api.create_event_batch.side_effect = Exception("API failure")
        
        with patch("asyncio.sleep", return_value=None) as mock_sleep:
            await buffer._flush()
            
            # Verify all retry attempts were made
            assert mock_api.create_event_batch.call_count == DEFAULT_MAX_RETRIES + 1
            assert mock_sleep.call_count == DEFAULT_MAX_RETRIES
            
            # Verify events are cleared even after failure
            assert len(buffer.events) == 0
            
            # Verify error is logged
            mock_logger.error.assert_called()


if __name__ == "__main__":
    unittest.main()