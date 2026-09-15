"""Runs the language-agnostic conformance vectors against this SDK.

The vectors and the semantics they pin live in ``conformance/`` at the repo
root, copied verbatim from schematic-node (the reference implementation). This
runner is the only language-specific piece; every port reimplements it and must
pass the same vectors, on every store backend it ships.

Flow-level vectors (``check`` / ``track``) skip until the check/track port
lands: fill in ``_op_check`` and ``_op_track``, drop them from ``FLOW_OPS``,
and the same vectors start running.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
from unittest import mock

import pytest
from lease_support import CrashingRefundLeaseStore, ScriptedWireClient, VirtualClock, make_fake_redis

from schematic.leases import (
    InMemoryLeaseStore,
    InMemoryReservationStore,
    LeaseConfig,
    LeaseManager,
    LeaseState,
    LeaseStore,
    RedisLeaseStore,
    RedisReservationStore,
    ReservationRecord,
    ReservationStore,
)

VECTORS_DIR = Path(__file__).resolve().parents[2] / "conformance" / "vectors"
BACKENDS = ("in_memory", "redis")
# Ops belonging to the check/track orchestration, which this SDK has yet to
# port. A vector using one of them skips rather than half-runs.
FLOW_OPS = {"check", "track"}


def _load_cases() -> List[Any]:
    cases: List[Any] = []
    for path in sorted(VECTORS_DIR.glob("*.json")):
        document = json.loads(path.read_text())
        for vector in document["vectors"]:
            for backend in BACKENDS:
                allowed = vector.get("backends")
                if allowed and backend not in allowed:
                    continue
                cases.append(
                    pytest.param(
                        backend,
                        vector,
                        id=f"{backend}-{document['category']}-{vector['name']}",
                    )
                )
    return cases


class Harness:
    """One vector's stores, manager, clock, and reservation handles."""

    def __init__(self, backend: str, config: Dict[str, Any]) -> None:
        self.clock = VirtualClock()
        self.handles: Dict[str, ReservationRecord] = {}
        self.wire = ScriptedWireClient()
        self.leases: LeaseStore
        self.reservations: ReservationStore
        if backend == "in_memory":
            self.leases = InMemoryLeaseStore(clock=self.clock)
            self.crash = CrashingRefundLeaseStore(self.leases)
            self.reservations = InMemoryReservationStore(self.crash, clock=self.clock)
        else:
            client = make_fake_redis()
            self.leases = RedisLeaseStore(client, clock=self.clock)
            self.crash = CrashingRefundLeaseStore(self.leases)
            self.reservations = RedisReservationStore(client, self.crash, clock=self.clock)
        self.manager = LeaseManager(
            self.wire,
            self.leases,
            reservation_store=self.reservations,
            config=LeaseConfig(
                lease_duration=_seconds(config.get("lease_duration_ms")),
                reservation_ttl=_seconds(config.get("reservation_ttl_ms")),
                lease_size=config.get("lease_size"),
                low_water_mark=config.get("low_water_mark"),
            ),
            clock=self.clock,
        )

    def at_ms(self, offset_ms: float) -> float:
        return self.clock.at_ms(offset_ms)

    def reservation_id(self, op: Dict[str, Any]) -> str:
        if "handle" in op:
            reservation = self.handles.get(op["handle"])
            if reservation is None:
                raise AssertionError(f"unknown reservation handle: {op['handle']}")
            return reservation.id
        if "id" not in op:
            raise AssertionError(f"op {op['op']} needs an id or handle")
        return str(op["id"])

    async def drain(self) -> None:
        """Let the manager's fire-and-forget work (a redundant release) finish."""
        await self.manager._drain_background()


@pytest.mark.parametrize("backend,vector", _load_cases())
async def test_vector(backend: str, vector: Dict[str, Any]) -> None:
    if any(op["op"] in FLOW_OPS for op in vector["operations"]):
        pytest.skip("flow ops land with the check/track port")
    harness = Harness(backend, (vector.get("given") or {}).get("config") or {})
    # The Redis backend decides expiry against the store's own clock (TIME),
    # so the virtual clock has to be the process clock too, not just the one
    # the stores read.
    with mock.patch("time.time", harness.clock):
        for lease in (vector.get("given") or {}).get("leases") or []:
            written = await harness.leases.replace(
                lease_id=lease["lease_id"],
                company_id=lease["company_id"],
                credit_type_id=lease["credit_type_id"],
                granted_amount=lease["granted_amount"],
                expires_at=harness.at_ms(lease["expires_at_ms"]),
            )
            assert written is True
        for op in vector["operations"]:
            handler = _HANDLERS.get(op["op"])
            if handler is None:
                raise AssertionError(f"unknown conformance op: {op['op']}")
            await handler(harness, op, op.get("expect") or {})
    harness.manager.stop()


async def _op_advance_clock(h: Harness, op: Dict[str, Any], expect: Dict[str, Any]) -> None:
    h.clock.advance_ms(op.get("ms") or 0)


async def _op_replace_lease(h: Harness, op: Dict[str, Any], expect: Dict[str, Any]) -> None:
    written = await h.leases.replace(
        lease_id=op["lease_id"],
        company_id=op["company_id"],
        credit_type_id=op["credit_type_id"],
        granted_amount=op["granted_amount"],
        expires_at=h.at_ms(op["expires_at_ms"]),
    )
    if "written" in expect:
        assert written is expect["written"]


async def _op_drop_lease(h: Harness, op: Dict[str, Any], expect: Dict[str, Any]) -> None:
    await h.leases.drop(op["company_id"], op["credit_type_id"])


async def _op_try_reserve(h: Harness, op: Dict[str, Any], expect: Dict[str, Any]) -> None:
    balance = await h.leases.try_reserve(op["company_id"], op["credit_type_id"], op["credits"])
    if "balance" in expect:
        _assert_number(balance, expect["balance"])


async def _op_refund_lease(h: Harness, op: Dict[str, Any], expect: Dict[str, Any]) -> None:
    await h.leases.refund(op["company_id"], op["credit_type_id"], op["credits"], op.get("pin_lease_id"))


async def _op_extend_lease(h: Harness, op: Dict[str, Any], expect: Dict[str, Any]) -> None:
    expires_at = h.at_ms(op["expires_at_ms"]) if "expires_at_ms" in op else None
    await h.leases.extend(
        op["company_id"],
        op["credit_type_id"],
        op["granted_total"],
        expires_at,
        op.get("pin_lease_id"),
    )


async def _op_get_lease(h: Harness, op: Dict[str, Any], expect: Dict[str, Any]) -> None:
    entry = await h.leases.get(op["company_id"], op["credit_type_id"])
    if "exists" in expect:
        assert (entry is not None) is expect["exists"]
    if "lease_id" in expect:
        assert (entry.lease_id if entry else None) == expect["lease_id"]
    if "granted_amount" in expect:
        assert entry is not None and entry.granted_amount == expect["granted_amount"]
    if "local_remaining_credits" in expect:
        assert entry is not None and entry.local_remaining_credits == expect["local_remaining_credits"]


async def _op_add_reservation(h: Harness, op: Dict[str, Any], expect: Dict[str, Any]) -> None:
    await h.reservations.add(
        ReservationRecord(
            id=op["id"],
            lease_id=op["lease_id"],
            company_id=op["company_id"],
            credit_type_id=op["credit_type_id"],
            event_subtype=op["event_subtype"],
            quantity_reserved=op["quantity_reserved"],
            credits_reserved=op["credits_reserved"],
            consumption_rate=op["consumption_rate"],
            expires_at=h.at_ms(op["expires_at_ms"]),
            company={"id": op["company_id"]},
        )
    )


async def _op_consume_reservation(h: Harness, op: Dict[str, Any], expect: Dict[str, Any]) -> None:
    reservation_id = h.reservation_id(op)
    if op.get("crash_before_refund"):
        h.crash.arm()
        with pytest.raises(RuntimeError, match="simulated crash before refund"):
            await h.reservations.consume(reservation_id, op["credits"])
        assert expect.get("throws") is True
        return
    consumed = await h.reservations.consume(reservation_id, op["credits"])
    if "consumed" in expect:
        _assert_number(consumed, expect["consumed"])


async def _op_get_reservation(h: Harness, op: Dict[str, Any], expect: Dict[str, Any]) -> None:
    reservation = await h.reservations.get(h.reservation_id(op))
    if "exists" in expect:
        assert (reservation is not None) is expect["exists"]


async def _op_reserved_credits(h: Harness, op: Dict[str, Any], expect: Dict[str, Any]) -> None:
    total = await h.reservations.reserved_credits(op["company_id"], op["credit_type_id"])
    assert total == expect["total"]


async def _op_reservation_count(h: Harness, op: Dict[str, Any], expect: Dict[str, Any]) -> None:
    assert await h.reservations.count() == expect["count"]


async def _op_sweep_expired(h: Harness, op: Dict[str, Any], expect: Dict[str, Any]) -> None:
    swept = await h.reservations.sweep_expired()
    if "swept" in expect:
        assert swept == expect["swept"]


async def _op_acquire_if_needed(h: Harness, op: Dict[str, Any], expect: Dict[str, Any]) -> None:
    if op.get("server"):
        h.wire.acquire_responses.append(_server_script(h, op["server"]))
    install = op.get("install_during_wire")
    if install:

        async def install_lease() -> None:
            await h.leases.replace(
                lease_id=install["lease_id"],
                company_id=install["company_id"],
                credit_type_id=install["credit_type_id"],
                granted_amount=install["granted_amount"],
                expires_at=h.at_ms(install["expires_at_ms"]),
            )

        h.wire.during_acquire = install_lease
    entry = await h.manager.acquire_if_needed(op["company_id"], op["credit_type_id"])
    await h.drain()
    if "lease_id" in expect:
        assert (entry.lease_id if entry else None) == expect["lease_id"]
    if "wire_acquires" in expect:
        assert len(h.wire.acquire_calls) == expect["wire_acquires"]
    if "last_acquire_requested_amount" in expect:
        assert h.wire.acquire_calls[-1]["requested_amount"] == expect["last_acquire_requested_amount"]
    if "released_lease_ids" in expect:
        assert h.wire.release_calls == expect["released_lease_ids"]


async def _op_maybe_extend(h: Harness, op: Dict[str, Any], expect: Dict[str, Any]) -> None:
    if op.get("server"):
        h.wire.extend_responses.append(_server_script(h, op["server"]))
    await h.manager.maybe_extend(op["company_id"], op["credit_type_id"], op.get("required_credits"))
    await h.drain()
    if "wire_extends" in expect:
        assert len(h.wire.extend_calls) == expect["wire_extends"]
    if "last_extend_additional_amount" in expect:
        assert h.wire.extend_calls[-1]["additional_amount"] == expect["last_extend_additional_amount"]
    if "last_extend_lease_id" in expect:
        assert h.wire.extend_calls[-1]["lease_id"] == expect["last_extend_lease_id"]


async def _op_release_all_local_leases(h: Harness, op: Dict[str, Any], expect: Dict[str, Any]) -> None:
    await h.manager.release_all_local_leases()
    if "released_lease_ids" in expect:
        assert h.wire.release_calls == expect["released_lease_ids"]
    if "remaining_slots" in expect:
        remaining: Optional[List[LeaseState]] = h.leases.list_leases()
        assert len(remaining or []) == expect["remaining_slots"]


async def _op_check(h: Harness, op: Dict[str, Any], expect: Dict[str, Any]) -> None:
    # Part 2 (the check/track port) fills this in and drops "check" from
    # FLOW_OPS; the vectors then run unchanged.
    raise NotImplementedError("check flow not ported yet")


async def _op_track(h: Harness, op: Dict[str, Any], expect: Dict[str, Any]) -> None:
    # See _op_check.
    raise NotImplementedError("track flow not ported yet")


_Handler = Callable[[Harness, Dict[str, Any], Dict[str, Any]], Any]

_HANDLERS: Dict[str, _Handler] = {
    "advance_clock": _op_advance_clock,
    "replace_lease": _op_replace_lease,
    "drop_lease": _op_drop_lease,
    "try_reserve": _op_try_reserve,
    "refund_lease": _op_refund_lease,
    "extend_lease": _op_extend_lease,
    "get_lease": _op_get_lease,
    "add_reservation": _op_add_reservation,
    "consume_reservation": _op_consume_reservation,
    "get_reservation": _op_get_reservation,
    "reserved_credits": _op_reserved_credits,
    "reservation_count": _op_reservation_count,
    "sweep_expired": _op_sweep_expired,
    "acquire_if_needed": _op_acquire_if_needed,
    "maybe_extend": _op_maybe_extend,
    "release_all_local_leases": _op_release_all_local_leases,
    "check": _op_check,
    "track": _op_track,
}


def _server_script(h: Harness, server: Dict[str, Any]) -> Dict[str, Any]:
    """Turn a vector's server script into one the wire stand-in can serve."""
    if server.get("error") is not None:
        return {"error": server["error"]}
    lease: Dict[str, Any] = dict(server["lease"])
    lease["expires_at"] = h.at_ms(lease["expires_at_ms"])
    return {"lease": lease}


def _assert_number(actual: Optional[float], expected: Optional[float]) -> None:
    """``None`` is the refused result, so it never compares equal to a figure."""
    if expected is None:
        assert actual is None
        return
    assert actual is not None and actual == expected


def _seconds(milliseconds: Optional[float]) -> Optional[float]:
    return None if milliseconds is None else milliseconds / 1000.0
