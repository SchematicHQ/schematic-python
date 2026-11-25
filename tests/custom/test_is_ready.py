import asyncio
from typing import AsyncIterator, Callable, Iterator, List, Optional
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

import schematic.client as client_module
from schematic.client import (
    AsyncSchematic,
    AsyncSchematicConfig,
    DataStreamConfig,
    Schematic,
    SchematicConfig,
)
from schematic.datastream.datastream_client import DataStreamClient
from schematic.datastream.types import DataStreamResp

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


def _ws_client(connected: bool, ready: bool) -> MagicMock:
    ws = MagicMock()
    ws.is_connected.return_value = connected
    ws.is_ready.return_value = ready
    ws.close = AsyncMock()
    return ws


def _replicator_config() -> DataStreamConfig:
    return DataStreamConfig(
        replicator_mode=True,
        company_cache=MagicMock(),
        company_lookup_cache=MagicMock(),
        user_cache=MagicMock(),
        user_lookup_cache=MagicMock(),
        flag_cache=MagicMock(),
    )


async def _load_flags(ds: DataStreamClient) -> None:
    await ds._handle_flags_message(
        DataStreamResp(data=[], entity_type="rulesengine.Flags", message_type="full")
    )


@pytest.fixture
def make_sync() -> Iterator[Callable[..., Schematic]]:
    created: List[Schematic] = []
    http_clients: List[httpx.Client] = []

    def make(handler: Handler = _ok, requests: Optional[List[httpx.Request]] = None, **kwargs) -> Schematic:
        http = httpx.Client(transport=httpx.MockTransport(_recording(handler, requests if requests is not None else [])))
        http_clients.append(http)
        kwargs.setdefault("logger", MagicMock())
        client = Schematic("test_key", SchematicConfig(httpx_client=http, **kwargs))
        created.append(client)
        return client

    yield make
    for client in created:
        client.shutdown()
    for http in http_clients:
        http.close()


@pytest.fixture
async def make_async() -> AsyncIterator[Callable[..., AsyncSchematic]]:
    created: List[AsyncSchematic] = []
    http_clients: List[httpx.AsyncClient] = []

    def make(handler=_ok, requests: Optional[List[httpx.Request]] = None, **kwargs) -> AsyncSchematic:
        http = httpx.AsyncClient(transport=httpx.MockTransport(_recording(handler, requests if requests is not None else [])))
        http_clients.append(http)
        kwargs.setdefault("logger", MagicMock())
        client = AsyncSchematic("test_key", AsyncSchematicConfig(httpx_client=http, **kwargs))
        created.append(client)
        return client

    yield make
    for client in created:
        await client.shutdown()
    for http in http_clients:
        await http.aclose()


class TestSchematicIsReady:
    def test_offline(self, make_sync):
        requests: List[httpx.Request] = []
        client = make_sync(_ok, requests, offline=True)
        assert client.is_ready() is True
        assert requests == []

    def test_api_success(self, make_sync):
        requests: List[httpx.Request] = []
        client = make_sync(_ok, requests)
        assert client.is_ready() is True
        assert len(requests) == 1
        assert requests[0].method == "GET"
        assert requests[0].url.path == "/whoami"
        assert requests[0].headers["X-Schematic-Api-Key"] == "test_key"

    def test_api_failure_logs_warning(self, make_sync):
        requests: List[httpx.Request] = []
        logger = MagicMock()
        client = make_sync(_unauthorized, requests, logger=logger)
        assert client.is_ready() is False
        assert len(requests) == 1
        logger.warning.assert_called_once()

    def test_api_timeout(self, make_sync):
        requests: List[httpx.Request] = []
        client = make_sync(_timeout, requests)
        assert client.is_ready() is False
        assert len(requests) == 1

    def test_uses_five_second_timeout(self, make_sync):
        timeouts: List[dict] = []

        def handler(request: httpx.Request) -> httpx.Response:
            timeouts.append(request.extensions["timeout"])
            return _ok(request)

        client = make_sync(handler, timeout=60)
        assert client.is_ready() is True
        assert timeouts[0]["read"] == 5

    def test_server_error_is_not_retried(self, make_sync):
        requests: List[httpx.Request] = []
        client = make_sync(_server_error, requests)
        assert client.is_ready() is False
        assert len(requests) == 1


class TestAsyncSchematicIsReady:
    async def test_offline(self, make_async):
        requests: List[httpx.Request] = []
        client = make_async(_ok, requests, offline=True)
        assert await client.is_ready() is True
        assert requests == []

    async def test_websocket_connected_with_flags_loaded_makes_no_network_call(self, make_async):
        requests: List[httpx.Request] = []
        client = make_async(_ok, requests, use_datastream=True)
        ds = client._datastream_client
        assert isinstance(ds, DataStreamClient)
        ds._ws_client = _ws_client(connected=True, ready=True)
        await _load_flags(ds)

        with patch.object(ds._rules_engine, "is_initialized", return_value=True):
            assert await client.is_ready() is True
        assert requests == []

    async def test_cache_ready_but_socket_down_checks_api(self, make_async):
        requests: List[httpx.Request] = []
        client = make_async(_ok, requests, use_datastream=True)
        ds = client._datastream_client
        assert isinstance(ds, DataStreamClient)
        ds._ws_client = _ws_client(connected=False, ready=False)
        await _load_flags(ds)
        assert ds.is_cache_ready() is True

        with patch.object(ds._rules_engine, "is_initialized", return_value=True):
            assert await client.is_ready() is True
        assert [r.url.path for r in requests] == ["/whoami"]

    async def test_connected_but_flags_not_loaded_checks_api(self, make_async):
        requests: List[httpx.Request] = []
        client = make_async(_ok, requests, use_datastream=True)
        ds = client._datastream_client
        assert isinstance(ds, DataStreamClient)
        ds._ws_client = _ws_client(connected=True, ready=True)

        with patch.object(ds._rules_engine, "is_initialized", return_value=True):
            assert await client.is_ready() is True
        assert [r.url.path for r in requests] == ["/whoami"]

    async def test_websocket_never_started_checks_api(self, make_async):
        requests: List[httpx.Request] = []
        client = make_async(_ok, requests, use_datastream=True)
        ds = client._datastream_client
        assert isinstance(ds, DataStreamClient)
        assert ds.is_cache_ready() is True

        assert await client.is_ready() is True
        assert [r.url.path for r in requests] == ["/whoami"]

    async def test_rules_engine_not_loaded_checks_api(self, make_async):
        requests: List[httpx.Request] = []
        client = make_async(_ok, requests, use_datastream=True)
        ds = client._datastream_client
        assert isinstance(ds, DataStreamClient)
        ds._ws_client = _ws_client(connected=True, ready=True)
        await _load_flags(ds)
        assert ds._rules_engine.is_initialized() is False

        assert await client.is_ready() is True
        assert [r.url.path for r in requests] == ["/whoami"]

    async def test_replicator_ready_makes_no_network_call(self, make_async):
        requests: List[httpx.Request] = []
        client = make_async(
            _ok, requests, use_datastream=True, datastream=_replicator_config()
        )
        ds = client._datastream_client
        assert isinstance(ds, DataStreamClient)
        ds._replicator_ready = True

        with patch.object(ds._rules_engine, "is_initialized", return_value=True):
            assert await client.is_ready() is True
        assert requests == []

    async def test_replicator_not_ready_checks_api(self, make_async):
        requests: List[httpx.Request] = []
        client = make_async(
            _ok, requests, use_datastream=True, datastream=_replicator_config()
        )
        ds = client._datastream_client
        assert isinstance(ds, DataStreamClient)
        ds._replicator_ready = False

        with patch.object(ds._rules_engine, "is_initialized", return_value=True):
            assert await client.is_ready() is True
        assert [r.url.path for r in requests] == ["/whoami"]

    async def test_datastream_not_ready_api_failure(self, make_async):
        requests: List[httpx.Request] = []
        client = make_async(
            _unauthorized, requests, use_datastream=True, datastream=_replicator_config()
        )
        assert await client.is_ready() is False
        assert len(requests) == 1

    async def test_api_success(self, make_async):
        requests: List[httpx.Request] = []
        client = make_async(_ok, requests)
        assert await client.is_ready() is True
        assert len(requests) == 1
        assert requests[0].method == "GET"
        assert requests[0].url.path == "/whoami"
        assert requests[0].headers["X-Schematic-Api-Key"] == "test_key"

    async def test_api_failure_logs_warning(self, make_async):
        requests: List[httpx.Request] = []
        logger = MagicMock()
        client = make_async(_unauthorized, requests, logger=logger)
        assert await client.is_ready() is False
        assert len(requests) == 1
        logger.warning.assert_called_once()

    async def test_api_timeout(self, make_async):
        requests: List[httpx.Request] = []
        client = make_async(_timeout, requests)
        assert await client.is_ready() is False
        assert len(requests) == 1

    async def test_uses_five_second_timeout(self, make_async):
        timeouts: List[dict] = []

        def handler(request: httpx.Request) -> httpx.Response:
            timeouts.append(request.extensions["timeout"])
            return _ok(request)

        client = make_async(handler, timeout=60)
        assert await client.is_ready() is True
        assert timeouts[0]["read"] == 5

    async def test_whole_call_is_bounded(self, make_async, monkeypatch):
        monkeypatch.setattr(client_module, "_READINESS_TIMEOUT_SECONDS", 0.05)

        async def hang(request: httpx.Request) -> httpx.Response:
            await asyncio.sleep(10)
            return _ok(request)

        client = make_async(hang)
        assert await asyncio.wait_for(client.is_ready(), timeout=2) is False

    async def test_server_error_is_not_retried(self, make_async):
        requests: List[httpx.Request] = []
        client = make_async(_server_error, requests)
        assert await client.is_ready() is False
        assert len(requests) == 1

    async def test_cancellation_propagates(self, make_async):
        started = asyncio.Event()

        async def hang(request: httpx.Request) -> httpx.Response:
            started.set()
            await asyncio.sleep(10)
            return _ok(request)

        client = make_async(hang)
        task = asyncio.create_task(client.is_ready())
        await asyncio.wait_for(started.wait(), timeout=2)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
