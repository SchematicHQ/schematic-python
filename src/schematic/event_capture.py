import datetime as dt
import typing

import httpx
import pydantic
from .core.pydantic_utilities import UniversalBaseModel
from .types import CreateEventRequestBody, EventBody, EventType

DEFAULT_EVENT_CAPTURE_BASE_URL = "https://c.schematichq.com"
DEFAULT_TIMEOUT = 10.0


class _CaptureEventPayload(UniversalBaseModel):
    """Wire format for a single event sent to the capture service.

    Mirrors the shape used by the Go/Ruby/C# SDKs: `type` (not `event_type`)
    and an `api_key` field embedded on each event.
    """

    api_key: str = pydantic.Field()
    body: typing.Optional[EventBody] = None
    type: EventType = pydantic.Field()
    sent_at: typing.Optional[dt.datetime] = None


class _CaptureBatchPayload(UniversalBaseModel):
    events: typing.List[_CaptureEventPayload]


def _to_payload(event: CreateEventRequestBody, api_key: str) -> _CaptureEventPayload:
    return _CaptureEventPayload(
        api_key=api_key,
        body=event.body,
        type=event.event_type,
        sent_at=event.sent_at,
    )


def _build_endpoint(base_url: str) -> str:
    return base_url.rstrip("/") + "/batch"


def _build_headers(
    api_key: str,
    get_headers: typing.Optional[typing.Callable[[], typing.Dict[str, str]]] = None,
) -> typing.Dict[str, str]:
    """Build the headers for capture-service requests.

    Reuses the API client's header builder when provided so we send the same
    X-Fern-* / User-Agent / X-Schematic-Api-Key headers as the REST client —
    keeps observability consistent across both endpoints.
    """
    headers: typing.Dict[str, str] = {}
    if get_headers is not None:
        headers.update(get_headers())
    else:
        headers["X-Schematic-Api-Key"] = api_key
    headers["Content-Type"] = "application/json"
    return headers


def _serialize_batch(
    events: typing.List[CreateEventRequestBody], api_key: str
) -> str:
    batch = _CaptureBatchPayload(
        events=[_to_payload(e, api_key) for e in events],
    )
    return batch.model_dump_json(by_alias=True, exclude_none=True)


class EventCaptureClient:
    """HTTP client for sending events to the Schematic event capture service."""

    def __init__(
        self,
        api_key: str,
        base_url: typing.Optional[str] = None,
        httpx_client: typing.Optional[httpx.Client] = None,
        get_headers: typing.Optional[typing.Callable[[], typing.Dict[str, str]]] = None,
    ):
        self._api_key = api_key
        self._base_url = base_url or DEFAULT_EVENT_CAPTURE_BASE_URL
        self._owns_client = httpx_client is None
        self._httpx_client = httpx_client or httpx.Client(timeout=DEFAULT_TIMEOUT)
        self._get_headers = get_headers

    def send_batch(self, events: typing.List[CreateEventRequestBody]) -> None:
        if not events:
            return

        body = _serialize_batch(events, self._api_key)
        response = self._httpx_client.post(
            _build_endpoint(self._base_url),
            content=body,
            headers=_build_headers(self._api_key, self._get_headers),
        )

        if response.status_code < 200 or response.status_code >= 300:
            raise RuntimeError(
                f"capture service returned HTTP {response.status_code}: {response.text}"
            )

    def close(self) -> None:
        if self._owns_client:
            self._httpx_client.close()


class AsyncEventCaptureClient:
    """Async HTTP client for sending events to the Schematic event capture service."""

    def __init__(
        self,
        api_key: str,
        base_url: typing.Optional[str] = None,
        httpx_client: typing.Optional[httpx.AsyncClient] = None,
        get_headers: typing.Optional[typing.Callable[[], typing.Dict[str, str]]] = None,
    ):
        self._api_key = api_key
        self._base_url = base_url or DEFAULT_EVENT_CAPTURE_BASE_URL
        self._owns_client = httpx_client is None
        self._httpx_client = httpx_client or httpx.AsyncClient(timeout=DEFAULT_TIMEOUT)
        self._get_headers = get_headers

    async def send_batch(self, events: typing.List[CreateEventRequestBody]) -> None:
        if not events:
            return

        body = _serialize_batch(events, self._api_key)
        response = await self._httpx_client.post(
            _build_endpoint(self._base_url),
            content=body,
            headers=_build_headers(self._api_key, self._get_headers),
        )

        if response.status_code < 200 or response.status_code >= 300:
            raise RuntimeError(
                f"capture service returned HTTP {response.status_code}: {response.text}"
            )

    async def close(self) -> None:
        if self._owns_client:
            await self._httpx_client.aclose()
