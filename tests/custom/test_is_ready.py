from typing import Callable, List
from unittest.mock import MagicMock

import httpx

from schematic.client import AsyncSchematic, AsyncSchematicConfig, Schematic, SchematicConfig
from schematic.datastream.datastream_client import DataStreamClient

WHOAMI_BODY = {
    "data": {
        "account_id": "acc_1",
        "account_name": "Acme",
        "actor_type": "api_key",
        "environments": [],
        "onboarding_complete": True,
    },
    "params": {},
}

Handler = Callable[[httpx.Request], httpx.Response]


def _ok(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, json=WHOAMI_BODY)


def _unauthorized(request: httpx.Request) -> httpx.Response:
    return httpx.Response(401, json={"error": "invalid api key"})


def _server_error(request: httpx.Request) -> httpx.Response:
    return httpx.Response(503, json={"error": "unavailable"})


def _timeout(request: httpx.Request) -> httpx.Response:
    raise httpx.ReadTimeout("timed out", request=request)


def _recording(handler: Handler, requests: List[httpx.Request]) -> Handler:
    def record(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return handler(request)

    return record


def _sync_client(handler: Handler, requests: List[httpx.Request], **kwargs) -> Schematic:
    config = SchematicConfig(
        logger=MagicMock(),
        httpx_client=httpx.Client(transport=httpx.MockTransport(_recording(handler, requests))),
        **kwargs,
    )
    return Schematic("test_key", config)


def _async_client(handler: Handler, requests: List[httpx.Request], **kwargs) -> AsyncSchematic:
    config = AsyncSchematicConfig(
        logger=MagicMock(),
        httpx_client=httpx.AsyncClient(transport=httpx.MockTransport(_recording(handler, requests))),
        **kwargs,
    )
    return AsyncSchematic("test_key", config)


class TestSchematicIsReady:
    def test_offline(self):
        client = Schematic("test_key", SchematicConfig(offline=True, logger=MagicMock()))
        try:
            assert client.is_ready() is True
        finally:
            client.shutdown()

    def test_api_success(self):
        requests: List[httpx.Request] = []
        client = _sync_client(_ok, requests)
        try:
            assert client.is_ready() is True
            assert len(requests) == 1
            assert requests[0].method == "GET"
            assert requests[0].url.path == "/whoami"
            assert requests[0].headers["X-Schematic-Api-Key"] == "test_key"
        finally:
            client.shutdown()

    def test_api_failure(self):
        requests: List[httpx.Request] = []
        client = _sync_client(_unauthorized, requests)
        try:
            assert client.is_ready() is False
            assert len(requests) == 1
        finally:
            client.shutdown()

    def test_api_timeout(self):
        requests: List[httpx.Request] = []
        client = _sync_client(_timeout, requests)
        try:
            assert client.is_ready() is False
        finally:
            client.shutdown()

    def test_uses_five_second_timeout(self):
        timeouts: List[dict] = []

        def handler(request: httpx.Request) -> httpx.Response:
            timeouts.append(request.extensions["timeout"])
            return _ok(request)

        client = _sync_client(handler, [], timeout=60)
        try:
            assert client.is_ready() is True
            assert timeouts[0]["read"] == 5
        finally:
            client.shutdown()

    def test_server_error_is_not_retried(self):
        requests: List[httpx.Request] = []
        client = _sync_client(_server_error, requests)
        try:
            assert client.is_ready() is False
            assert len(requests) == 1
        finally:
            client.shutdown()


class TestAsyncSchematicIsReady:
    async def test_offline(self):
        client = AsyncSchematic("test_key", AsyncSchematicConfig(offline=True, logger=MagicMock()))
        try:
            assert await client.is_ready() is True
        finally:
            await client.event_buffer.stop()

    async def test_datastream_usable_makes_no_network_call(self):
        requests: List[httpx.Request] = []
        client = _async_client(_ok, requests, use_datastream=True)
        try:
            ds = MagicMock()
            ds.is_cache_ready.return_value = True
            ds.is_connected.return_value = True
            client._datastream_client = ds

            assert await client.is_ready() is True
            assert requests == []
        finally:
            await client.event_buffer.stop()

    async def test_websocket_not_connected_checks_api(self):
        requests: List[httpx.Request] = []
        client = _async_client(_ok, requests, use_datastream=True)
        try:
            assert isinstance(client._datastream_client, DataStreamClient)
            assert client._datastream_client.is_cache_ready() is True
            assert client._datastream_client.is_connected() is False

            assert await client.is_ready() is True
            assert [r.url.path for r in requests] == ["/whoami"]
        finally:
            await client.event_buffer.stop()

    async def test_datastream_not_ready_checks_api(self):
        requests: List[httpx.Request] = []
        client = _async_client(_ok, requests, use_datastream=True)
        try:
            ds = MagicMock()
            ds.is_cache_ready.return_value = False
            client._datastream_client = ds

            assert await client.is_ready() is True
            assert [r.url.path for r in requests] == ["/whoami"]
        finally:
            await client.event_buffer.stop()

    async def test_datastream_not_ready_api_failure(self):
        requests: List[httpx.Request] = []
        client = _async_client(_unauthorized, requests, use_datastream=True)
        try:
            ds = MagicMock()
            ds.is_cache_ready.return_value = False
            client._datastream_client = ds

            assert await client.is_ready() is False
        finally:
            await client.event_buffer.stop()

    async def test_api_success(self):
        requests: List[httpx.Request] = []
        client = _async_client(_ok, requests)
        try:
            assert await client.is_ready() is True
            assert len(requests) == 1
            assert requests[0].method == "GET"
            assert requests[0].url.path == "/whoami"
            assert requests[0].headers["X-Schematic-Api-Key"] == "test_key"
        finally:
            await client.event_buffer.stop()

    async def test_api_failure(self):
        requests: List[httpx.Request] = []
        client = _async_client(_unauthorized, requests)
        try:
            assert await client.is_ready() is False
            assert len(requests) == 1
        finally:
            await client.event_buffer.stop()

    async def test_api_timeout(self):
        requests: List[httpx.Request] = []
        client = _async_client(_timeout, requests)
        try:
            assert await client.is_ready() is False
        finally:
            await client.event_buffer.stop()

    async def test_uses_five_second_timeout(self):
        timeouts: List[dict] = []

        def handler(request: httpx.Request) -> httpx.Response:
            timeouts.append(request.extensions["timeout"])
            return _ok(request)

        client = _async_client(handler, [], timeout=60)
        try:
            assert await client.is_ready() is True
            assert timeouts[0]["read"] == 5
        finally:
            await client.event_buffer.stop()

    async def test_server_error_is_not_retried(self):
        requests: List[httpx.Request] = []
        client = _async_client(_server_error, requests)
        try:
            assert await client.is_ready() is False
            assert len(requests) == 1
        finally:
            await client.event_buffer.stop()
