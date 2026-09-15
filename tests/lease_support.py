"""Harness shared by the lease unit tests and the conformance runner.

Everything here is test-only: the virtual clock, the fakeredis client the
verbatim Lua scripts can run against, the crash seam the bounded-leak tests
need, and a scriptable stand-in for the lease wire API.
"""

from __future__ import annotations

import datetime as dt
from typing import Any, Awaitable, Dict, List, Optional, cast

import fakeredis.aioredis

from schematic.leases import LeaseGrant, LeaseState, ReservationRecord
from schematic.leases.lease_store import LeaseStore

# The fixed virtual instant every vector and test starts from.
T0 = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc).timestamp()


class VirtualClock:
    """A clock only ``advance`` moves, so no test depends on wall time."""

    def __init__(self, now: float = T0) -> None:
        self._now = now

    def __call__(self) -> float:
        return self._now

    def advance_ms(self, milliseconds: float) -> None:
        self._now += milliseconds / 1000.0

    def at_ms(self, offset_ms: float) -> float:
        """An absolute position on the virtual timeline, as the vectors express it."""
        return T0 + offset_ms / 1000.0


class LuaCompatFakeRedis(fakeredis.aioredis.FakeRedis):
    """fakeredis with the one Lua builtin its runtime lacks papered over.

    ``redis.replicate_commands()`` is what lets a real Redis 5/6 read TIME in a
    writing script; fakeredis's Lua runtime does not define it. Stripping the
    call here (rather than dropping it from the scripts) keeps the shipped Lua
    byte-identical to the Node SDK's, which is what lets both fleets share one
    Redis. The scripts are sent through SCRIPT LOAD as well as EVAL, so both
    are rewritten and the server-assigned digest stays consistent.
    """

    @staticmethod
    def _strip(script: str) -> str:
        return script.replace("redis.replicate_commands()\n", "")

    async def script_load(self, script: str) -> Any:  # type: ignore[override]
        return await cast(Awaitable[Any], super().script_load(self._strip(script)))

    async def eval(self, script: str, numkeys: int, *keys_and_args: Any) -> Any:  # type: ignore[override]
        return await cast(Awaitable[Any], super().eval(self._strip(script), numkeys, *keys_and_args))


def make_fake_redis() -> LuaCompatFakeRedis:
    return LuaCompatFakeRedis(decode_responses=True)


class CrashingRefundLeaseStore(LeaseStore):
    """Lease store whose ``refund`` raises once while armed.

    The reservation store refunds through the store it is handed, so wrapping
    that one reproduces a process death between the claim and the refund while
    the test body keeps reading the real store.
    """

    def __init__(self, target: LeaseStore) -> None:
        self._target = target
        self._armed = False

    def arm(self) -> None:
        self._armed = True

    async def get(self, company_id: str, credit_type_id: str) -> Optional[LeaseState]:
        return await self._target.get(company_id, credit_type_id)

    async def replace(
        self,
        *,
        lease_id: str,
        company_id: str,
        credit_type_id: str,
        granted_amount: float,
        expires_at: float,
    ) -> bool:
        return await self._target.replace(
            lease_id=lease_id,
            company_id=company_id,
            credit_type_id=credit_type_id,
            granted_amount=granted_amount,
            expires_at=expires_at,
        )

    async def try_reserve(self, company_id: str, credit_type_id: str, credits: float) -> Optional[float]:
        return await self._target.try_reserve(company_id, credit_type_id, credits)

    async def refund(
        self,
        company_id: str,
        credit_type_id: str,
        credits: float,
        pin_lease_id: Optional[str] = None,
    ) -> None:
        if self._armed:
            self._armed = False
            raise RuntimeError("simulated crash before refund")
        await self._target.refund(company_id, credit_type_id, credits, pin_lease_id)

    async def extend(
        self,
        company_id: str,
        credit_type_id: str,
        granted_total: float,
        new_expires_at: Optional[float] = None,
        pin_lease_id: Optional[str] = None,
    ) -> None:
        await self._target.extend(company_id, credit_type_id, granted_total, new_expires_at, pin_lease_id)

    async def drop(self, company_id: str, credit_type_id: str) -> None:
        await self._target.drop(company_id, credit_type_id)

    def list_leases(self) -> Optional[List[LeaseState]]:
        return self._target.list_leases()


class ScriptedWireClient:
    """Stands in for the lease API: queued responses in, recorded calls out."""

    def __init__(self) -> None:
        self.acquire_responses: List[Dict[str, Any]] = []
        self.extend_responses: List[Dict[str, Any]] = []
        self.acquire_calls: List[Dict[str, Any]] = []
        self.extend_calls: List[Dict[str, Any]] = []
        self.release_calls: List[str] = []
        # Runs while an acquire is in flight, for emulating a sibling pod
        # winning the race.
        self.during_acquire: Optional[Any] = None

    async def acquire(
        self,
        company_id: str,
        credit_type_id: str,
        requested_amount: float,
        expires_at: float,
    ) -> LeaseGrant:
        self.acquire_calls.append(
            {
                "company_id": company_id,
                "credit_type_id": credit_type_id,
                "requested_amount": requested_amount,
                "expires_at": expires_at,
            }
        )
        during = self.during_acquire
        if during is not None:
            self.during_acquire = None
            await during()
        scripted = self.acquire_responses.pop(0) if self.acquire_responses else None
        lease = _scripted_lease(scripted, "unscripted acquire wire call")
        return LeaseGrant(
            lease_id=lease.get("lease_id", "lse_unnamed"),
            company_id=company_id,
            credit_type_id=credit_type_id,
            granted_amount=float(lease.get("granted_amount", 0)),
            expires_at=lease["expires_at"],
        )

    async def extend(self, lease_id: str, additional_amount: float, expires_at: float) -> LeaseGrant:
        self.extend_calls.append(
            {"lease_id": lease_id, "additional_amount": additional_amount, "expires_at": expires_at}
        )
        scripted = self.extend_responses.pop(0) if self.extend_responses else None
        lease = _scripted_lease(scripted, "unscripted extend wire call")
        return LeaseGrant(
            lease_id=lease_id,
            company_id=lease.get("company_id", "co_wire"),
            credit_type_id=lease.get("credit_type_id", "ct_wire"),
            granted_amount=float(lease.get("granted_total", lease.get("granted_amount", 0))),
            expires_at=lease["expires_at"],
        )

    async def release(self, lease_id: str) -> None:
        self.release_calls.append(lease_id)


def _scripted_lease(scripted: Optional[Dict[str, Any]], missing: str) -> Dict[str, Any]:
    if scripted is None:
        raise RuntimeError(missing)
    if scripted.get("error") is not None or not scripted.get("lease"):
        raise RuntimeError(str(scripted.get("error") or missing))
    lease: Dict[str, Any] = dict(scripted["lease"])
    return lease


def make_reservation(**overrides: Any) -> ReservationRecord:
    fields: Dict[str, Any] = {
        "id": "res_1",
        "lease_id": "lse_1",
        "company_id": "co_1",
        "credit_type_id": "ct_1",
        "event_subtype": "inference_tokens",
        "quantity_reserved": 10,
        "credits_reserved": 100,
        "consumption_rate": 10,
        "expires_at": T0 + 60,
        "company": {"id": "co_1"},
    }
    fields.update(overrides)
    return ReservationRecord(**fields)
