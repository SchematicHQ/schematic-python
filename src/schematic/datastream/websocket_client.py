from __future__ import annotations

# Note: This client is designed for server-side async environments only.

import asyncio
import json
import logging
import random
from dataclasses import dataclass
from typing import AsyncIterator, Awaitable, Callable, Dict, Optional, Protocol, Union
from urllib.parse import urlparse, urlunparse

import websockets

from .types import DataStreamBaseReq, DataStreamResp


class _WebSocketProtocol(Protocol):
    """Structural interface for the websocket connection object."""

    async def send(self, message: Union[str, bytes]) -> None: ...

    async def close(self) -> None: ...

    def __aiter__(self) -> AsyncIterator[Union[str, bytes]]: ...

# Connection timing constants (seconds)
WRITE_WAIT = 10.0
PONG_WAIT = 60.0
PING_PERIOD = (PONG_WAIT * 9) / 10  # 54 seconds
CONNECTION_TIMEOUT = 30.0

# Reconnection constants
MAX_RECONNECT_ATTEMPTS = 10
MIN_RECONNECT_DELAY = 1.0  # seconds
MAX_RECONNECT_DELAY = 30.0  # seconds

MessageHandlerFunc = Callable[[DataStreamResp], Awaitable[None]]
ConnectionReadyHandlerFunc = Callable[[], Awaitable[None]]


def convert_api_url_to_websocket_url(api_url: str) -> str:
    """Convert an HTTP API URL to a WebSocket datastream URL.

    Examples:
        https://api.schematichq.com   -> wss://datastream.schematichq.com/datastream
        https://api.staging.x.com     -> wss://datastream.staging.x.com/datastream
        https://custom.example.com    -> wss://custom.example.com/datastream
        http://localhost:8080          -> ws://localhost:8080/datastream
    """
    parsed = urlparse(api_url)

    if parsed.scheme == "https":
        scheme = "wss"
    elif parsed.scheme == "http":
        scheme = "ws"
    else:
        raise ValueError(f"Unsupported scheme: {parsed.scheme!r} (must be http or https)")

    # Replace 'api' subdomain with 'datastream' if present
    hostname = parsed.hostname or ""
    parts = hostname.split(".")
    if len(parts) > 1 and parts[0] == "api":
        parts[0] = "datastream"
        hostname = ".".join(parts)

    netloc = f"{hostname}:{parsed.port}" if parsed.port else hostname
    return urlunparse((scheme, netloc, "/datastream", "", "", ""))


@dataclass
class ClientOptions:
    """Configuration for DatastreamWSClient."""

    # Required
    url: str
    api_key: str
    message_handler: MessageHandlerFunc
    logger: logging.Logger

    # Optional
    connection_ready_handler: Optional[ConnectionReadyHandlerFunc] = None
    max_reconnect_attempts: int = MAX_RECONNECT_ATTEMPTS
    min_reconnect_delay: float = MIN_RECONNECT_DELAY
    max_reconnect_delay: float = MAX_RECONNECT_DELAY

    # Event callbacks — called on state transitions
    on_connected: Optional[Callable[[], None]] = None
    on_disconnected: Optional[Callable[[], None]] = None
    on_ready: Optional[Callable[[], None]] = None
    on_not_ready: Optional[Callable[[], None]] = None
    on_error: Optional[Callable[[Exception], None]] = None


class DatastreamWSClient:
    """WebSocket client for the Schematic datastream with automatic reconnection.

    Connects to the Schematic datastream, delivers incoming messages to the
    provided ``message_handler``, and transparently reconnects with exponential
    backoff whenever the connection drops.

    Usage::

        async def handle_message(msg: DataStreamResp) -> None:
            print(msg)

        client = DatastreamWSClient(ClientOptions(
            url="https://api.schematichq.com",
            api_key="your-api-key",
            message_handler=handle_message,
            logger=logging.getLogger(__name__),
        ))
        client.start()
        # ... later:
        await client.close()
    """

    def __init__(self, options: ClientOptions) -> None:
        if not options.url:
            raise ValueError("url is required")
        if not options.api_key:
            raise ValueError("api_key is required")
        if not options.message_handler:
            raise ValueError("message_handler is required")

        # Auto-convert HTTP(S) URLs to WebSocket URLs
        if options.url.startswith(("http://", "https://")):
            self._url = convert_api_url_to_websocket_url(options.url)
        else:
            self._url = options.url

        self._headers: Dict[str, str] = {"X-Schematic-Api-Key": options.api_key}
        self._logger = options.logger
        self._message_handler = options.message_handler
        self._connection_ready_handler = options.connection_ready_handler
        self._max_reconnect_attempts = options.max_reconnect_attempts
        self._min_reconnect_delay = options.min_reconnect_delay
        self._max_reconnect_delay = options.max_reconnect_delay

        # Event callbacks
        self._on_connected = options.on_connected
        self._on_disconnected = options.on_disconnected
        self._on_ready = options.on_ready
        self._on_not_ready = options.on_not_ready
        self._on_error = options.on_error

        # Connection state
        self._ws: Optional[_WebSocketProtocol] = None
        self._connected: bool = False
        self._ready: bool = False

        # Control state
        self._should_reconnect: bool = False
        self._reconnect_attempts: int = 0
        self._task: Optional[asyncio.Task[None]] = None

    def start(self) -> None:
        """Begin the WebSocket connection loop as a background asyncio task."""
        self._should_reconnect = True
        self._reconnect_attempts = 0
        self._task = asyncio.ensure_future(self._connect_and_read())

    def is_connected(self) -> bool:
        """Return whether the WebSocket is currently connected."""
        return self._connected

    def is_ready(self) -> bool:
        """Return whether the client is connected and fully initialised."""
        return self._ready and self._connected

    async def send_message(self, message: DataStreamBaseReq) -> None:
        """Send a message over the WebSocket connection.

        Raises ``RuntimeError`` if the connection is not available or the send
        times out after ``WRITE_WAIT`` seconds.
        """
        if not self.is_connected() or self._ws is None:
            raise RuntimeError("WebSocket connection is not available")

        payload = json.dumps(message.to_dict())
        try:
            await asyncio.wait_for(self._ws.send(payload), timeout=WRITE_WAIT)
        except asyncio.TimeoutError:
            raise RuntimeError("Write timeout")

    async def close(self) -> None:
        """Gracefully close the connection and stop the reconnection loop."""
        self._logger.info("Closing WebSocket connection")

        self._should_reconnect = False
        self._set_ready(False)
        self._set_connected(False)

        if self._ws is not None:
            try:
                await self._ws.close()
            except Exception:
                pass
            self._ws = None

        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except (asyncio.CancelledError, Exception):
                pass
            self._task = None

    # ------------------------------------------------------------------
    # Internal connection loop
    # ------------------------------------------------------------------

    async def _connect_and_read(self) -> None:
        while self._should_reconnect:
            try:
                async with websockets.connect(
                    self._url,
                    extra_headers=self._headers,
                    open_timeout=CONNECTION_TIMEOUT,
                    ping_interval=PING_PERIOD,
                    ping_timeout=PONG_WAIT,
                ) as ws:
                    self._ws = ws
                    self._reconnect_attempts = 0
                    self._set_connected(True)

                    # Run the ready handler before marking the client ready
                    if self._connection_ready_handler is not None:
                        try:
                            await self._connection_ready_handler()
                            self._logger.debug("Connection ready handler completed successfully")
                        except Exception as err:
                            self._logger.error(f"Connection ready handler failed: {err}")
                            continue

                    self._set_ready(True)
                    self._logger.debug("WebSocket client is ready")

                    async for raw_message in ws:
                        await self._handle_message(raw_message)

                    self._logger.info("WebSocket connection closed")

            except asyncio.CancelledError:
                break

            except Exception as err:
                self._reconnect_attempts += 1
                self._logger.warning(
                    f"WebSocket connection failed: {err}, "
                    f"attempt {self._reconnect_attempts}/{self._max_reconnect_attempts}"
                )

                if self._reconnect_attempts >= self._max_reconnect_attempts:
                    self._logger.error("Max reconnection attempts reached")
                    if self._on_error is not None:
                        self._on_error(Exception("Max reconnection attempts reached"))
                    break

            finally:
                self._set_connected(False)
                self._set_ready(False)
                self._ws = None

            if not self._should_reconnect:
                break

            delay = self._calculate_backoff_delay(self._reconnect_attempts)
            self._logger.debug(f"Waiting {delay:.1f}s before reconnecting...")
            try:
                await asyncio.sleep(delay)
            except asyncio.CancelledError:
                break

    # ------------------------------------------------------------------
    # Message handling
    # ------------------------------------------------------------------

    async def _handle_message(self, raw_message: Union[str, bytes]) -> None:
        try:
            if isinstance(raw_message, bytes):
                message_str = raw_message.decode("utf-8")
            else:
                message_str = str(raw_message)

            try:
                data = json.loads(message_str)
            except json.JSONDecodeError as err:
                if self._on_error is not None:
                    self._on_error(Exception(f"Failed to parse datastream message: {err}"))
                return

            message = DataStreamResp(
                data=data.get("data"),
                entity_type=data.get("entity_type", ""),
                message_type=data.get("message_type", ""),
            )

            try:
                await self._message_handler(message)
            except Exception as err:
                if self._on_error is not None:
                    self._on_error(Exception(f"Message handler error: {err}"))

        except Exception as err:
            if self._on_error is not None:
                self._on_error(err)

    # ------------------------------------------------------------------
    # State management
    # ------------------------------------------------------------------

    def _set_connected(self, connected: bool) -> None:
        was_connected = self._connected
        self._connected = connected

        if not connected:
            self._ready = False

        if was_connected != connected:
            self._logger.debug(f"Connection state changed: {connected}")
            if connected:
                if self._on_connected is not None:
                    self._on_connected()
            else:
                if self._on_disconnected is not None:
                    self._on_disconnected()

    def _set_ready(self, ready: bool) -> None:
        was_ready = self._ready
        self._ready = ready

        if was_ready != ready:
            self._logger.debug(f"Ready state changed: {ready}")
            if ready:
                if self._on_ready is not None:
                    self._on_ready()
            else:
                if self._on_not_ready is not None:
                    self._on_not_ready()

    def _calculate_backoff_delay(self, attempt: int) -> float:
        """Exponential backoff with jitter, capped at max_reconnect_delay."""
        jitter = random.uniform(0, self._min_reconnect_delay)
        delay = (2 ** (attempt - 1)) * self._min_reconnect_delay + jitter
        return min(delay, self._max_reconnect_delay + jitter)
