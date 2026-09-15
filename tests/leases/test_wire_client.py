"""The adapter between the manager and the generated credits client."""

from __future__ import annotations

import datetime as dt
from typing import Any, Dict, List, Optional

from schematic.credits.types.acquire_credit_lease_response import AcquireCreditLeaseResponse
from schematic.credits.types.extend_credit_lease_response import ExtendCreditLeaseResponse
from schematic.leases import CreditsWireClient, LeaseWireClient
from schematic.types.credit_lease_response_data import CreditLeaseResponseData

EXPIRES_AT = dt.datetime(2026, 1, 1, 0, 5, tzinfo=dt.timezone.utc)


def _lease_data(lease_id: str = "lse_1", granted_amount: float = 1000) -> CreditLeaseResponseData:
    now = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)
    return CreditLeaseResponseData(
        id=lease_id,
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=granted_amount,
        tracked_amount=0,
        expires_at=EXPIRES_AT,
        created_at=now,
        updated_at=now,
    )


class StubCreditsClient:
    def __init__(self) -> None:
        self.acquire_calls: List[Dict[str, Any]] = []
        self.extend_calls: List[Dict[str, Any]] = []
        self.release_calls: List[str] = []

    async def acquire_credit_lease(self, **kwargs: Any) -> AcquireCreditLeaseResponse:
        self.acquire_calls.append(kwargs)
        return AcquireCreditLeaseResponse(data=_lease_data(), params={})

    async def extend_credit_lease(self, lease_id: str, **kwargs: Any) -> ExtendCreditLeaseResponse:
        self.extend_calls.append({"lease_id": lease_id, **kwargs})
        return ExtendCreditLeaseResponse(data=_lease_data(granted_amount=2000), params={})

    async def release_credit_lease(self, lease_id: str, **kwargs: Any) -> None:
        self.release_calls.append(lease_id)


async def test_acquire_maps_the_request_and_the_response() -> None:
    stub = StubCreditsClient()
    wire: LeaseWireClient = CreditsWireClient(stub)

    grant = await wire.acquire("co_1", "ct_1", 1000, EXPIRES_AT.timestamp())

    assert stub.acquire_calls[0]["company_id"] == "co_1"
    assert stub.acquire_calls[0]["credit_type_id"] == "ct_1"
    assert stub.acquire_calls[0]["requested_amount"] == 1000
    assert stub.acquire_calls[0]["expires_at"] == EXPIRES_AT
    assert grant.lease_id == "lse_1"
    assert grant.granted_amount == 1000
    assert grant.expires_at == EXPIRES_AT.timestamp()


async def test_extend_sends_the_additional_amount_and_reads_back_the_total() -> None:
    stub = StubCreditsClient()
    wire: LeaseWireClient = CreditsWireClient(stub)

    grant = await wire.extend("lse_1", 500, EXPIRES_AT.timestamp())

    assert stub.extend_calls[0]["lease_id"] == "lse_1"
    assert stub.extend_calls[0]["additional_amount"] == 500
    # The response carries the server-authoritative TOTAL, not the increment.
    assert grant.granted_amount == 2000


async def test_release_passes_the_lease_id() -> None:
    stub = StubCreditsClient()
    wire: LeaseWireClient = CreditsWireClient(stub)
    await wire.release("lse_1")
    assert stub.release_calls == ["lse_1"]


async def test_a_naive_expiry_is_read_as_utc() -> None:
    # A naive timestamp from the API is UTC; reading it as local time would
    # shift every expiry by the pod's offset.
    class NaiveClient(StubCreditsClient):
        async def acquire_credit_lease(self, **kwargs: Any) -> AcquireCreditLeaseResponse:
            data = _lease_data().model_copy(update={"expires_at": EXPIRES_AT.replace(tzinfo=None)})
            return AcquireCreditLeaseResponse(data=data, params={})

    wire: LeaseWireClient = CreditsWireClient(NaiveClient())
    grant = await wire.acquire("co_1", "ct_1", 1000, EXPIRES_AT.timestamp())
    assert grant.expires_at == EXPIRES_AT.timestamp()


async def test_request_options_are_threaded_through() -> None:
    stub = StubCreditsClient()
    options: Optional[Any] = {"timeout_in_seconds": 2}
    wire: LeaseWireClient = CreditsWireClient(stub, request_options=options)
    await wire.acquire("co_1", "ct_1", 1000, EXPIRES_AT.timestamp())
    assert stub.acquire_calls[0]["request_options"] == options
