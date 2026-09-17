"""Acquire and extend across the SDK's own retry policy.

These drive the generated credits client over a mock transport rather than a
stand-in wire client, because what they pin is the retry loop itself: which
body each attempt carries, and what the manager does with the attempt that
finally succeeds.
"""

from __future__ import annotations

import datetime as dt
import json
from typing import Any, Dict, List

import httpx
import pytest
from lease_support import VirtualClock

from schematic.core import http_client
from schematic.core.client_wrapper import AsyncClientWrapper
from schematic.credits.client import AsyncCreditsClient
from schematic.leases import (
    CreditsWireClient,
    InMemoryLeaseStore,
    LeaseConfig,
    LeaseManager,
    LeaseWireClient,
)

CONFIG = LeaseConfig(lease_duration=300, reservation_ttl=60, lease_size=1000, low_water_mark=0.25)


@pytest.fixture(autouse=True)
def _fast_backoff(monkeypatch: pytest.MonkeyPatch) -> None:
    """The retry policy sleeps a second before its first retry, which no test
    needs to sit through."""
    monkeypatch.setattr(http_client, "INITIAL_RETRY_DELAY_SECONDS", 0.001)


class RecordingTransport(httpx.MockTransport):
    """Replays a queue of status codes in order, recording each request body."""

    def __init__(self, statuses: List[int], body: Dict[str, Any]) -> None:
        self.bodies: List[Dict[str, Any]] = []
        self._statuses = list(statuses)
        self._body = body
        super().__init__(self._handle)

    def _handle(self, request: httpx.Request) -> httpx.Response:
        self.bodies.append(json.loads(request.content) if request.content else {})
        status = self._statuses.pop(0) if self._statuses else 200
        if status >= 400:
            return httpx.Response(status, json={"error": "upstream is unhappy"})
        return httpx.Response(status, json=self._body)


def _lease_body(lease_id: str, granted_amount: float, expires_at: float) -> Dict[str, Any]:
    created = "2026-01-01T00:00:00Z"
    return {
        "data": {
            "id": lease_id,
            "company_id": "co_1",
            "credit_type_id": "ct_1",
            "granted_amount": granted_amount,
            "tracked_amount": 0,
            "expires_at": dt.datetime.fromtimestamp(expires_at, tz=dt.timezone.utc).isoformat(),
            "created_at": created,
            "updated_at": created,
        },
        "params": {},
    }


def _make_manager(clock: VirtualClock, transport: RecordingTransport) -> tuple[LeaseManager, InMemoryLeaseStore]:
    wrapper = AsyncClientWrapper(
        api_key="test",
        base_url="https://api.schematichq.test",
        httpx_client=httpx.AsyncClient(transport=transport),
    )
    wire: LeaseWireClient = CreditsWireClient(AsyncCreditsClient(client_wrapper=wrapper))
    store = InMemoryLeaseStore(clock=clock)
    return LeaseManager(wire, store, config=CONFIG, clock=clock), store


async def test_acquire_retried_after_a_502_installs_the_lease_from_the_200(clock: VirtualClock) -> None:
    transport = RecordingTransport([502, 200], _lease_body("lse_1", 1000, clock() + 300))
    manager, _store = _make_manager(clock, transport)

    entry = await manager.acquire_if_needed("co_1", "ct_1")

    assert len(transport.bodies) == 2
    assert entry is not None and entry.lease_id == "lse_1"
    assert entry.local_remaining_credits == 1000


async def test_extend_retried_after_a_502_repeats_its_key_and_lands_once(clock: VirtualClock) -> None:
    transport = RecordingTransport([502, 200], _lease_body("lse_1", 2000, clock() + 300))
    manager, store = _make_manager(clock, transport)
    await store.replace(
        lease_id="lse_1",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=1000,
        expires_at=clock() + 300,
    )
    await store.try_reserve("co_1", "ct_1", 900)

    entry = await manager.maybe_extend("co_1", "ct_1")

    assert len(transport.bodies) == 2
    keys = [body["idempotency_key"] for body in transport.bodies]
    assert keys[0] == keys[1]
    # The 2000 total the server reports, minus the 900 already drawn locally,
    # so the lease grew by one tranche rather than by two.
    assert entry is not None and entry.granted_amount == 2000
    assert entry.local_remaining_credits == 1100
