import asyncio
import logging
import random
import threading
import time
from typing import List, Optional

from .events.client import AsyncEventsClient, EventsClient
from .types import CreateEventRequestBody

DEFAULT_MAX_EVENTS = 100  # Default maximum number of events
DEFAULT_EVENT_BUFFER_PERIOD = 5  # 5 seconds
DEFAULT_MAX_RETRIES = 3  # Default maximum number of retry attempts
DEFAULT_INITIAL_RETRY_DELAY = 1  # Initial retry delay in seconds


class EventBuffer:
    def __init__(
        self,
        events_api: EventsClient,
        logger: logging.Logger,
        period: Optional[int] = None,
        max_events: int = DEFAULT_MAX_EVENTS,
        max_retries: int = DEFAULT_MAX_RETRIES,
        initial_retry_delay: float = DEFAULT_INITIAL_RETRY_DELAY,
    ):
        self.events: List[CreateEventRequestBody] = []
        self.events_api = events_api
        self.interval = period or DEFAULT_EVENT_BUFFER_PERIOD
        self.logger = logger
        self.max_events = max_events
        self.max_retries = max_retries
        self.initial_retry_delay = initial_retry_delay
        self.flush_lock = threading.Lock()
        self.push_lock = threading.Lock()
        self.shutdown = threading.Event()
        self.stopped = False

        # Start periodic flushing thread
        self.flush_thread = threading.Thread(target=self._periodic_flush)
        self.flush_thread.daemon = True
        self.flush_thread.start()

    def _flush(self):
        with self.flush_lock:
            if not self.events:
                return

            events = [event for event in self.events if event is not None]

            # Initialize retry counter and success flag
            retry_count = 0
            success = False
            last_exception = None

            # Try with retries and exponential backoff
            while retry_count <= self.max_retries and not success:
                try:
                    if retry_count > 0:
                        # Log retry attempt
                        self.logger.info(f"Retrying event batch submission (attempt {retry_count} of {self.max_retries})")

                    # Attempt to send events
                    self.events_api.create_event_batch(events=events)
                    success = True

                except Exception as e:
                    last_exception = e
                    retry_count += 1

                    if retry_count <= self.max_retries:
                        # Calculate backoff with jitter
                        delay = self.initial_retry_delay * (2 ** (retry_count - 1))
                        jitter = random.uniform(0, 0.1 * delay)  # 10% jitter
                        wait_time = delay + jitter

                        self.logger.warning(
                            f"Event batch submission failed: {e}. "
                            f"Retrying in {wait_time:.2f} seconds..."
                        )

                        # Wait before retry
                        time.sleep(wait_time)

            # After all retries, if still not successful, log the error
            if not success:
                self.logger.error(
                    f"Event batch submission failed after {self.max_retries} retries: {last_exception}"
                )
            elif retry_count > 0:
                self.logger.info(f"Event batch submission succeeded after {retry_count} retries")

            self.events.clear()

    def _periodic_flush(self):
        while not self.shutdown.is_set():
            self._flush()
            self.shutdown.wait(timeout=self.interval)

    def push(self, event: CreateEventRequestBody):
        if self.stopped:
            self.logger.error("Event buffer is stopped, not accepting new events")
            return

        with self.push_lock:
            if len(self.events) >= self.max_events:
                self._flush()

            self.events.append(event)

    def stop(self):
        try:
            self.stopped = True
            self.shutdown.set()
            self.flush_thread.join(timeout=5)
        except Exception as e:
            self.logger.error(f"Panic occurred while closing client: {e}")


class AsyncEventBuffer:
    def __init__(
        self,
        events_api: AsyncEventsClient,
        logger: logging.Logger,
        period: Optional[int] = None,
        max_events: int = DEFAULT_MAX_EVENTS,
        max_retries: int = DEFAULT_MAX_RETRIES,
        initial_retry_delay: float = DEFAULT_INITIAL_RETRY_DELAY,
    ):
        self.events: List[CreateEventRequestBody] = []
        self.events_api = events_api
        self.interval = period or DEFAULT_EVENT_BUFFER_PERIOD
        self.logger = logger
        self.max_events = max_events
        self.max_retries = max_retries
        self.initial_retry_delay = initial_retry_delay
        self.shutdown_event = asyncio.Event()
        self.stopped = False
        self.flush_lock = asyncio.Lock()
        self.push_lock = asyncio.Lock()

        # Start periodic flushing task
        self.flush_task = asyncio.create_task(self._periodic_flush())

    async def _flush(self):
        async with self.flush_lock:
            if not self.events:
                return

            events = [event for event in self.events if event is not None]

            # Initialize retry counter and success flag
            retry_count = 0
            success = False
            last_exception = None

            # Try with retries and exponential backoff
            while retry_count <= self.max_retries and not success:
                try:
                    if retry_count > 0:
                        # Log retry attempt
                        self.logger.info(f"Retrying event batch submission (attempt {retry_count} of {self.max_retries})")

                    # Attempt to send events
                    await self.events_api.create_event_batch(events=events)
                    success = True

                except Exception as e:
                    last_exception = e
                    retry_count += 1

                    if retry_count <= self.max_retries:
                        # Calculate backoff with jitter
                        delay = self.initial_retry_delay * (2 ** (retry_count - 1))
                        jitter = random.uniform(0, 0.1 * delay)  # 10% jitter
                        wait_time = delay + jitter

                        self.logger.warning(
                            f"Event batch submission failed: {e}. "
                            f"Retrying in {wait_time:.2f} seconds..."
                        )

                        # Wait before retry (asyncio sleep)
                        await asyncio.sleep(wait_time)

            # After all retries, if still not successful, log the error
            if not success:
                self.logger.error(
                    f"Event batch submission failed after {self.max_retries} retries: {last_exception}"
                )
            elif retry_count > 0:
                self.logger.info(f"Event batch submission succeeded after {retry_count} retries")

            self.events.clear()

    async def _periodic_flush(self):
        while not self.shutdown_event.is_set():
            await self._flush()
            try:
                await asyncio.wait_for(
                    self.shutdown_event.wait(), timeout=self.interval
                )
            except asyncio.TimeoutError:
                pass

    async def push(self, event: CreateEventRequestBody):
        if self.stopped:
            self.logger.error("Event buffer is stopped, not accepting new events")
            return

        async with self.push_lock:
            if len(self.events) >= self.max_events:
                await self._flush()

            self.events.append(event)

    async def stop(self):
        try:
            self.stopped = True
            self.shutdown_event.set()
            await self.flush_task
        except Exception as e:
            self.logger.error(f"Panic occurred while closing client: {e}")
