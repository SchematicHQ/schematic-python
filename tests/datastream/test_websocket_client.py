from __future__ import annotations

import asyncio
import json
import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator, List, Optional
from unittest.mock import patch

import pytest

from schematic.datastream.types import DataStreamBaseReq, DataStreamReq, DataStreamResp, EntityType
from schematic.datastream.websocket_client import (
    ClientOptions,
    DatastreamWSClient,
    convert_api_url_to_websocket_url,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Mock helpers
# ---------------------------------------------------------------------------


class MockWebSocket:
    """Fake WebSocket that yields a fixed list of messages then stops.

    Set ``block_on_empty=True`` to keep the connection open after all messages
    are consumed — useful for tests that need to inspect state while connected.
    Call ``.close()`` to unblock.
    """

    def __init__(self, messages: Optional[List[str]] = None, block_on_empty: bool = False) -> None:
        self._messages = messages or []
        self._index = 0
        self._block_on_empty = block_on_empty
        self._close_event: asyncio.Event = asyncio.Event()
        self.sent: List[str] = []
        self.closed = False

    async def send(self, message: str | bytes) -> None:
        self.sent.append(message.decode() if isinstance(message, bytes) else message)

    async def close(self) -> None:
        self.closed = True
        self._close_event.set()

    def __aiter__(self) -> AsyncIterator[str]:
        return self

    async def __anext__(self) -> str:
        if self._index < len(self._messages):
            msg = self._messages[self._index]
            self._index += 1
            return msg
        if self._block_on_empty:
            await self._close_event.wait()
        raise StopAsyncIteration


class _AlwaysFailConnect:
    """Mimics websockets.connect but always raises on __aenter__."""

    def __call__(self, *args, **kwargs) -> _AlwaysFailConnect:
        return self

    async def __aenter__(self) -> None:
        raise ConnectionError("connection refused")

    async def __aexit__(self, *args) -> None:
        pass


def make_connect(ws: MockWebSocket):
    """Return a mock for websockets.connect that yields the given MockWebSocket."""

    @asynccontextmanager
    async def _connect(*args, **kwargs):
        yield ws

    return _connect


def make_client(
    messages: Optional[List[str]] = None,
    ws: Optional[MockWebSocket] = None,
    **kwargs,
) -> tuple[DatastreamWSClient, MockWebSocket, List[DataStreamResp]]:
    """Build a DatastreamWSClient backed by a MockWebSocket.

    Extra kwargs are forwarded to ClientOptions, allowing callbacks and other
    options to be set per-test.
    """
    if ws is None:
        ws = MockWebSocket(messages or [])

    received: List[DataStreamResp] = []

    async def handler(msg: DataStreamResp) -> None:
        received.append(msg)

    client = DatastreamWSClient(
        ClientOptions(
            url="wss://test.example.com/datastream",
            api_key="test-key",
            message_handler=handler,
            logger=logger,
            min_reconnect_delay=0.0,
            max_reconnect_delay=0.0,
            **kwargs,
        )
    )
    return client, ws, received


async def wait_until(condition, timeout: float = 2.0, poll: float = 0.01) -> None:
    """Poll until condition() is True or timeout is reached."""

    async def _poll():
        while not condition():
            await asyncio.sleep(poll)

    await asyncio.wait_for(_poll(), timeout=timeout)


@asynccontextmanager
async def run_client(client: DatastreamWSClient):
    """Context manager that ensures client.close() is always called."""
    client.start()
    try:
        yield client
    finally:
        await client.close()


# ---------------------------------------------------------------------------
# convert_api_url_to_websocket_url
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "api_url,expected",
    [
        ("https://api.schematichq.com", "wss://datastream.schematichq.com/datastream"),
        ("https://api.staging.schematichq.com", "wss://datastream.staging.schematichq.com/datastream"),
        ("https://custom.example.com", "wss://custom.example.com/datastream"),
        ("http://localhost:8080", "ws://localhost:8080/datastream"),
        ("http://localhost", "ws://localhost/datastream"),
    ],
)
def test_convert_api_url(api_url: str, expected: str) -> None:
    assert convert_api_url_to_websocket_url(api_url) == expected


def test_convert_api_url_unsupported_scheme() -> None:
    with pytest.raises(ValueError, match="Unsupported scheme"):
        convert_api_url_to_websocket_url("ftp://example.com")


# ---------------------------------------------------------------------------
# Constructor validation
# ---------------------------------------------------------------------------


def test_init_missing_url() -> None:
    async def handler(msg): pass

    with pytest.raises(ValueError, match="url is required"):
        DatastreamWSClient(ClientOptions(url="", api_key="key", message_handler=handler, logger=logger))


def test_init_missing_api_key() -> None:
    async def handler(msg): pass

    with pytest.raises(ValueError, match="api_key is required"):
        DatastreamWSClient(ClientOptions(url="wss://example.com", api_key="", message_handler=handler, logger=logger))


def test_init_missing_message_handler() -> None:
    with pytest.raises(ValueError, match="message_handler is required"):
        DatastreamWSClient(
            ClientOptions(url="wss://example.com", api_key="key", message_handler=None, logger=logger)  # type: ignore[arg-type]
        )


def test_init_converts_http_url() -> None:
    async def handler(msg): pass

    client = DatastreamWSClient(
        ClientOptions(url="https://api.schematichq.com", api_key="key", message_handler=handler, logger=logger)
    )
    assert client._url == "wss://datastream.schematichq.com/datastream"


# ---------------------------------------------------------------------------
# send_message
# ---------------------------------------------------------------------------


async def test_send_message_raises_when_not_connected() -> None:
    client, _, _ = make_client()
    req = DataStreamBaseReq(data=DataStreamReq(entity_type=EntityType.COMPANY))

    with pytest.raises(RuntimeError, match="not available"):
        await client.send_message(req)


async def test_send_message_sends_json_when_connected() -> None:
    ws = MockWebSocket(block_on_empty=True)
    connected = asyncio.Event()
    client, ws, _ = make_client(ws=ws, on_connected=lambda: connected.set())

    with patch("schematic.datastream.websocket_client.websockets.connect", make_connect(ws)):
        async with run_client(client):
            await asyncio.wait_for(connected.wait(), timeout=2.0)

            req = DataStreamBaseReq(data=DataStreamReq(entity_type=EntityType.COMPANY))
            await client.send_message(req)

            assert len(ws.sent) == 1
            assert json.loads(ws.sent[0]) == {"data": {"action": "start", "entity_type": "rulesengine.Company"}}


# ---------------------------------------------------------------------------
# Message handling
# ---------------------------------------------------------------------------


async def test_string_message_delivered_to_handler() -> None:
    msg = json.dumps({"entity_type": "rulesengine.Company", "message_type": "full", "data": {"id": "123"}})
    client, ws, received = make_client(messages=[msg])

    with patch("schematic.datastream.websocket_client.websockets.connect", make_connect(ws)):
        async with run_client(client):
            await wait_until(lambda: len(received) == 1)

    assert received[0].entity_type == "rulesengine.Company"
    assert received[0].message_type == "full"
    assert received[0].data == {"id": "123"}


async def test_bytes_message_delivered_to_handler() -> None:
    payload = json.dumps({"entity_type": "rulesengine.Flag", "message_type": "full", "data": None})
    ws = MockWebSocket(messages=[payload.encode()])  # type: ignore[list-item]
    client, ws, received = make_client(ws=ws)

    with patch("schematic.datastream.websocket_client.websockets.connect", make_connect(ws)):
        async with run_client(client):
            await wait_until(lambda: len(received) == 1)

    assert received[0].entity_type == "rulesengine.Flag"


async def test_invalid_json_calls_on_error() -> None:
    errors: List[Exception] = []
    client, ws, _ = make_client(messages=["not-valid-json"], on_error=errors.append)

    with patch("schematic.datastream.websocket_client.websockets.connect", make_connect(ws)):
        async with run_client(client):
            await wait_until(lambda: len(errors) > 0)

    assert "Failed to parse" in str(errors[0])


async def test_message_handler_exception_calls_on_error() -> None:
    errors: List[Exception] = []

    async def bad_handler(msg: DataStreamResp) -> None:
        raise ValueError("handler blew up")

    msg = json.dumps({"entity_type": "rulesengine.Company", "message_type": "full", "data": None})
    ws = MockWebSocket(messages=[msg])
    client = DatastreamWSClient(
        ClientOptions(
            url="wss://test.example.com/datastream",
            api_key="key",
            message_handler=bad_handler,
            logger=logger,
            min_reconnect_delay=0.0,
            max_reconnect_delay=0.0,
            on_error=errors.append,
        )
    )

    with patch("schematic.datastream.websocket_client.websockets.connect", make_connect(ws)):
        async with run_client(client):
            await wait_until(lambda: len(errors) > 0)

    assert "Message handler error" in str(errors[0])


# ---------------------------------------------------------------------------
# State callbacks
# ---------------------------------------------------------------------------


async def test_on_connected_and_on_ready_fired() -> None:
    connected_calls: List[bool] = []
    ready_calls: List[bool] = []

    ws = MockWebSocket(block_on_empty=True)
    client, ws, _ = make_client(
        ws=ws,
        on_connected=lambda: connected_calls.append(True),
        on_ready=lambda: ready_calls.append(True),
    )

    with patch("schematic.datastream.websocket_client.websockets.connect", make_connect(ws)):
        async with run_client(client):
            await wait_until(client.is_ready)

            assert connected_calls == [True]
            assert ready_calls == [True]
            assert client.is_connected()
            assert client.is_ready()


async def test_on_disconnected_and_on_not_ready_fired_on_close() -> None:
    disconnected_calls: List[bool] = []
    not_ready_calls: List[bool] = []

    ws = MockWebSocket(block_on_empty=True)
    client, ws, _ = make_client(
        ws=ws,
        on_disconnected=lambda: disconnected_calls.append(True),
        on_not_ready=lambda: not_ready_calls.append(True),
    )

    with patch("schematic.datastream.websocket_client.websockets.connect", make_connect(ws)):
        async with run_client(client):
            await wait_until(client.is_connected)

    assert True in disconnected_calls
    assert True in not_ready_calls
    assert not client.is_connected()
    assert not client.is_ready()


# ---------------------------------------------------------------------------
# connection_ready_handler
# ---------------------------------------------------------------------------


async def test_connection_ready_handler_called_before_ready() -> None:
    order: List[str] = []

    async def ready_handler() -> None:
        order.append("ready_handler")

    ws = MockWebSocket(block_on_empty=True)
    client, ws, _ = make_client(
        ws=ws,
        connection_ready_handler=ready_handler,
        on_ready=lambda: order.append("on_ready"),
    )

    with patch("schematic.datastream.websocket_client.websockets.connect", make_connect(ws)):
        async with run_client(client):
            await wait_until(client.is_ready)

            assert order == ["ready_handler", "on_ready"]


async def test_connection_ready_handler_failure_prevents_ready() -> None:
    async def failing_handler() -> None:
        raise RuntimeError("setup failed")

    ws = MockWebSocket()
    client, ws, _ = make_client(
        ws=ws,
        connection_ready_handler=failing_handler,
        max_reconnect_attempts=1,
    )

    with patch("schematic.datastream.websocket_client.websockets.connect", make_connect(ws)):
        async with run_client(client):
            await asyncio.sleep(0.1)

    assert not client.is_ready()


# ---------------------------------------------------------------------------
# Reconnection
# ---------------------------------------------------------------------------


async def test_reconnects_after_connection_error() -> None:
    connect_calls: List[int] = []
    msg = json.dumps({"entity_type": "rulesengine.Company", "message_type": "full", "data": None})
    success_ws = MockWebSocket(messages=[msg])

    @asynccontextmanager
    async def mock_connect(*args, **kwargs):
        connect_calls.append(1)
        if len(connect_calls) == 1:
            raise ConnectionError("first attempt fails")
        yield success_ws

    received: List[DataStreamResp] = []

    async def handler(m: DataStreamResp) -> None:
        received.append(m)

    client = DatastreamWSClient(
        ClientOptions(
            url="wss://test.example.com/datastream",
            api_key="key",
            message_handler=handler,
            logger=logger,
            min_reconnect_delay=0.0,
            max_reconnect_delay=0.0,
            max_reconnect_attempts=5,
        )
    )

    with patch("schematic.datastream.websocket_client.websockets.connect", mock_connect):
        async with run_client(client):
            await wait_until(lambda: len(received) == 1)

    assert len(connect_calls) >= 2
    assert len(received) == 1


async def test_stops_at_max_reconnect_attempts() -> None:
    errors: List[Exception] = []

    client = DatastreamWSClient(
        ClientOptions(
            url="wss://test.example.com/datastream",
            api_key="key",
            message_handler=lambda _: None,  # type: ignore[arg-type,return-value]
            logger=logger,
            min_reconnect_delay=0.0,
            max_reconnect_delay=0.0,
            max_reconnect_attempts=3,
            on_error=errors.append,
        )
    )

    with patch("schematic.datastream.websocket_client.websockets.connect", _AlwaysFailConnect()):
        async with run_client(client):
            await wait_until(lambda: len(errors) > 0)

    assert "Max reconnection" in str(errors[0])


# ---------------------------------------------------------------------------
# Backoff delay
# ---------------------------------------------------------------------------


async def test_on_disconnected_fires_when_connection_drops_mid_session() -> None:
    """Spec DataStream checklist item 10: Connection lost triggers disconnect event.

    Distinct from test_on_disconnected_and_on_not_ready_fired_on_close, which
    only covers graceful close(). Here the connection drops unexpectedly via a
    raised exception while the message-read loop is active.
    """

    class DroppingWebSocket(MockWebSocket):
        async def __anext__(self) -> str:
            raise ConnectionError("connection dropped mid-session")

    disconnected_calls: List[bool] = []
    connected_calls: List[bool] = []

    ws = DroppingWebSocket()
    client = DatastreamWSClient(
        ClientOptions(
            url="wss://test.example.com/datastream",
            api_key="key",
            message_handler=lambda _: None,  # type: ignore[arg-type,return-value]
            logger=logger,
            min_reconnect_delay=0.0,
            max_reconnect_delay=0.0,
            max_reconnect_attempts=1,  # Stop after first reconnect attempt
            on_connected=lambda: connected_calls.append(True),
            on_disconnected=lambda: disconnected_calls.append(True),
        )
    )

    with patch("schematic.datastream.websocket_client.websockets.connect", make_connect(ws)):
        async with run_client(client):
            await wait_until(lambda: len(disconnected_calls) > 0)

    assert connected_calls == [True]
    assert disconnected_calls == [True]


async def test_reconnects_after_mid_session_drop() -> None:
    """Spec DataStream checklist item 11: Reconnection after disconnect.

    First connection drops after delivering one message; second connection
    delivers another. Both should arrive at the message handler and the
    connect helper should be invoked at least twice.
    """
    msg1 = json.dumps({"entity_type": "rulesengine.Company", "message_type": "full", "data": {"id": "c1"}})
    msg2 = json.dumps({"entity_type": "rulesengine.Company", "message_type": "full", "data": {"id": "c2"}})

    class FirstDropsThenSucceeds:
        def __init__(self) -> None:
            self.first_ws = MockWebSocket(messages=[msg1])
            self.second_ws = MockWebSocket(messages=[msg2])
            self.connect_count = 0

        @asynccontextmanager
        async def connect(self, *args, **kwargs):
            self.connect_count += 1
            if self.connect_count == 1:
                yield self.first_ws
                # First WS exits (StopAsyncIteration on exhausted messages)
            else:
                yield self.second_ws

    fixture = FirstDropsThenSucceeds()
    received: List[DataStreamResp] = []

    async def handler(m: DataStreamResp) -> None:
        received.append(m)

    client = DatastreamWSClient(
        ClientOptions(
            url="wss://test.example.com/datastream",
            api_key="key",
            message_handler=handler,
            logger=logger,
            min_reconnect_delay=0.0,
            max_reconnect_delay=0.0,
            max_reconnect_attempts=5,
        )
    )

    with patch("schematic.datastream.websocket_client.websockets.connect", fixture.connect):
        async with run_client(client):
            await wait_until(lambda: len(received) >= 2)

    assert fixture.connect_count >= 2
    assert {r.data["id"] for r in received} == {"c1", "c2"}  # type: ignore[index]


def test_backoff_delay_within_bounds() -> None:
    client, _, _ = make_client()

    for attempt in range(1, 8):
        delay = client._calculate_backoff_delay(attempt)
        assert delay >= 0
        assert delay <= client._max_reconnect_delay + client._min_reconnect_delay


def test_backoff_delay_does_not_exceed_max() -> None:
    async def handler(msg): pass

    client = DatastreamWSClient(
        ClientOptions(
            url="wss://test.example.com/datastream",
            api_key="key",
            message_handler=handler,
            logger=logger,
            min_reconnect_delay=1.0,
            max_reconnect_delay=5.0,
        )
    )

    # At high attempt counts, delay should be capped at max + jitter ceiling
    delay = client._calculate_backoff_delay(20)
    assert delay <= 5.0 + 1.0
