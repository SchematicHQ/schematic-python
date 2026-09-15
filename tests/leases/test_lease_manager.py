"""Lease manager behavior, ported from the Node SDK's manager tests.

The cross-pod cases share one Redis between two managers, which is the shape
the store's convergence rules exist for.
"""

from __future__ import annotations

import asyncio
from typing import Any, List, Optional

import pytest
from lease_support import ScriptedWireClient, VirtualClock, make_fake_redis

from schematic.leases import (
    InMemoryLeaseStore,
    InMemoryReservationStore,
    LeaseConfig,
    LeaseGrant,
    LeaseManager,
    LeaseState,
    LeaseStore,
    RedisLeaseStore,
)

CONFIG = LeaseConfig(lease_duration=300, reservation_ttl=60, lease_size=1000, low_water_mark=0.25)


@pytest.fixture(autouse=True)
def _frozen(frozen_clock: VirtualClock) -> VirtualClock:
    """The shared-store cases run against fakeredis, which reads TIME from the
    process clock, so the virtual clock has to be that clock here."""
    return frozen_clock


def _lease(clock: VirtualClock, lease_id: str = "lse_1", granted: float = 1000, ttl: float = 300) -> dict:
    return {"lease": {"lease_id": lease_id, "granted_amount": granted, "expires_at": clock() + ttl}}


def _make_manager(clock: VirtualClock) -> tuple[LeaseManager, InMemoryLeaseStore, ScriptedWireClient]:
    store = InMemoryLeaseStore(clock=clock)
    wire = ScriptedWireClient()
    manager = LeaseManager(wire, store, config=CONFIG, clock=clock)
    return manager, store, wire


async def test_acquire_installs_the_lease(clock: VirtualClock) -> None:
    manager, store, wire = _make_manager(clock)
    wire.acquire_responses.append(_lease(clock))

    entry = await manager.acquire_if_needed("co_1", "ct_1")
    assert len(wire.acquire_calls) == 1
    assert wire.acquire_calls[0]["requested_amount"] == 1000
    assert entry is not None and entry.lease_id == "lse_1" and entry.local_remaining_credits == 1000


async def test_acquire_reuses_a_live_lease(clock: VirtualClock) -> None:
    manager, _store, wire = _make_manager(clock)
    wire.acquire_responses.append(_lease(clock))
    await manager.acquire_if_needed("co_1", "ct_1")
    await manager.acquire_if_needed("co_1", "ct_1")
    assert len(wire.acquire_calls) == 1


async def test_acquire_is_single_flight(clock: VirtualClock) -> None:
    manager, _store, wire = _make_manager(clock)
    gate: "asyncio.Future[None]" = asyncio.get_running_loop().create_future()
    original = wire.acquire

    async def slow_acquire(*args: Any, **kwargs: Any) -> LeaseGrant:
        await gate
        return await original(*args, **kwargs)

    wire.acquire = slow_acquire  # type: ignore[method-assign]
    wire.acquire_responses.append(_lease(clock))

    pending = [asyncio.ensure_future(manager.acquire_if_needed("co_1", "ct_1")) for _ in range(3)]
    await asyncio.sleep(0)
    gate.set_result(None)
    results = await asyncio.gather(*pending)

    assert len(wire.acquire_calls) == 1
    assert [r.lease_id for r in results if r] == ["lse_1"] * 3


async def test_acquire_replaces_an_expired_slot_without_releasing(clock: VirtualClock) -> None:
    manager, store, wire = _make_manager(clock)
    await store.replace(
        lease_id="lse_stale",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=1000,
        expires_at=clock() - 1,
    )
    wire.acquire_responses.append(_lease(clock, "lse_fresh"))

    entry = await manager.acquire_if_needed("co_1", "ct_1")
    await manager._drain_background()
    assert entry is not None and entry.lease_id == "lse_fresh" and entry.local_remaining_credits == 1000
    # `replace` wrote rather than keeping a live lease, so nothing is redundant.
    assert wire.release_calls == []


async def test_extend_fires_below_the_water_mark(clock: VirtualClock) -> None:
    manager, store, wire = _make_manager(clock)
    wire.acquire_responses.append(_lease(clock))
    await manager.acquire_if_needed("co_1", "ct_1")
    await store.try_reserve("co_1", "ct_1", 800)

    wire.extend_responses.append({"lease": {"granted_total": 2000, "expires_at": clock() + 600}})
    await manager.maybe_extend("co_1", "ct_1")
    assert len(wire.extend_calls) == 1
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.granted_amount == 2000 and entry.local_remaining_credits == 1200


async def test_extend_fires_for_required_credits_above_the_water_mark(clock: VirtualClock) -> None:
    manager, store, wire = _make_manager(clock)
    wire.acquire_responses.append(_lease(clock))
    await manager.acquire_if_needed("co_1", "ct_1")
    await store.try_reserve("co_1", "ct_1", 100)

    # Without the hint this is a no-op: 900/1000 is far above the water mark.
    await manager.maybe_extend("co_1", "ct_1")
    assert wire.extend_calls == []

    wire.extend_responses.append({"lease": {"granted_total": 2000, "expires_at": clock() + 600}})
    await manager.maybe_extend("co_1", "ct_1", 1500)
    assert len(wire.extend_calls) == 1
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.granted_amount == 2000


async def test_extend_is_sized_to_the_shortfall(clock: VirtualClock) -> None:
    manager, store, wire = _make_manager(clock)
    wire.acquire_responses.append(_lease(clock))
    await manager.acquire_if_needed("co_1", "ct_1")
    await store.try_reserve("co_1", "ct_1", 100)

    # A check needing 5000 credits has a 4100 shortfall, above the configured
    # 1000 tranche: a tranche-sized extend would leave its retry failing
    # forever however much balance the server has.
    wire.extend_responses.append({"lease": {"granted_total": 5100, "expires_at": clock() + 600}})
    await manager.maybe_extend("co_1", "ct_1", 5000)
    assert wire.extend_calls[-1]["additional_amount"] == 4100
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.local_remaining_credits == 5000


async def test_never_extends_an_expired_lease(clock: VirtualClock) -> None:
    manager, store, wire = _make_manager(clock)
    await store.replace(
        lease_id="lse_old",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=1000,
        expires_at=clock() - 1,
    )
    assert await manager.maybe_extend("co_1", "ct_1", 1500) is None
    assert wire.extend_calls == []


async def test_store_failures_resolve_to_no_lease(clock: VirtualClock) -> None:
    class BrokenStore(InMemoryLeaseStore):
        async def get(self, company_id: str, credit_type_id: str) -> Optional[LeaseState]:
            raise RuntimeError("redis down")

    wire = ScriptedWireClient()
    manager = LeaseManager(wire, BrokenStore(clock=clock), config=CONFIG, clock=clock)
    # Both are often called fire-and-forget, where a raised exception would
    # surface as an unretrieved task exception.
    assert await manager.acquire_if_needed("co_1", "ct_1") is None
    assert await manager.maybe_extend("co_1", "ct_1") is None
    assert wire.acquire_calls == []
    assert wire.extend_calls == []


async def test_wire_failures_resolve_to_no_lease(clock: VirtualClock) -> None:
    manager, store, wire = _make_manager(clock)
    wire.acquire_responses.append({"error": "wire down"})
    assert await manager.acquire_if_needed("co_1", "ct_1") is None
    assert await store.get("co_1", "ct_1") is None

    await store.replace(
        lease_id="lse_1",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=1000,
        expires_at=clock() + 300,
    )
    await store.try_reserve("co_1", "ct_1", 800)
    wire.extend_responses.append({"error": "wire down"})
    assert await manager.maybe_extend("co_1", "ct_1") is None
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.granted_amount == 1000 and entry.local_remaining_credits == 200


async def test_release_all_releases_live_and_skips_expired(clock: VirtualClock) -> None:
    manager, store, wire = _make_manager(clock)
    await store.replace(
        lease_id="lse_live",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=1000,
        expires_at=clock() + 60,
    )
    await store.replace(
        lease_id="lse_expired",
        company_id="co_2",
        credit_type_id="ct_1",
        granted_amount=1000,
        expires_at=clock() - 1,
    )
    await manager.release_all_local_leases()
    assert wire.release_calls == ["lse_live"]
    # The released lease is dropped locally; the expired one is left to lazy
    # expiry.
    assert await store.get("co_1", "ct_1") is None
    assert await store.get("co_2", "ct_1") is not None


async def test_release_all_skips_a_shared_store(clock: VirtualClock) -> None:
    # A shared backend cannot enumerate: sibling pods still draw on its leases.
    client = make_fake_redis()
    store = RedisLeaseStore(client, clock=clock)
    wire = ScriptedWireClient()
    manager = LeaseManager(wire, store, config=CONFIG, clock=clock)
    await store.replace(
        lease_id="lse_shared",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=1000,
        expires_at=clock() + 60,
    )
    await manager.release_all_local_leases()
    assert wire.release_calls == []


async def test_acquire_and_extend_do_not_share_inflight_state(clock: VirtualClock) -> None:
    manager, store, wire = _make_manager(clock)
    gate: "asyncio.Future[None]" = asyncio.get_running_loop().create_future()
    original_extend = wire.extend

    async def slow_extend(*args: Any, **kwargs: Any) -> LeaseGrant:
        await gate
        return await original_extend(*args, **kwargs)

    wire.extend = slow_extend  # type: ignore[method-assign]
    wire.extend_responses.append({"lease": {"granted_total": 2000, "expires_at": clock() + 600}})
    wire.acquire_responses.append(_lease(clock, "lse_fresh"))

    await store.replace(
        lease_id="lse_live",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=1000,
        expires_at=clock() + 300,
    )
    await store.try_reserve("co_1", "ct_1", 800)
    extending = asyncio.ensure_future(manager.maybe_extend("co_1", "ct_1"))
    await asyncio.sleep(0)

    await store.drop("co_1", "ct_1")
    acquired = await manager.acquire_if_needed("co_1", "ct_1")
    assert acquired is not None and acquired.lease_id == "lse_fresh"
    assert len(wire.acquire_calls) == 1

    gate.set_result(None)
    await extending


async def test_lost_acquire_race_releases_the_redundant_lease(clock: VirtualClock) -> None:
    # Two managers on one Redis, as two pods would be. Both see an empty slot
    # and acquire; only one lease can hold the slot, and the loser must release
    # the one it minted rather than orphan it against the company balance.
    shared: LeaseStore = RedisLeaseStore(make_fake_redis(), clock=clock)
    pods = []
    for lease_id in ("lse_a", "lse_b"):
        wire = ScriptedWireClient()
        wire.acquire_responses.append(_lease(clock, lease_id))
        pods.append((LeaseManager(wire, shared, config=CONFIG, clock=clock), wire))

    entries = await asyncio.gather(*(manager.acquire_if_needed("co_1", "ct_1") for manager, _ in pods))
    for manager, _ in pods:
        await manager._drain_background()

    survivor = await shared.get("co_1", "ct_1")
    assert survivor is not None and survivor.lease_id in ("lse_a", "lse_b")
    assert [entry.lease_id for entry in entries if entry] == [survivor.lease_id] * 2

    released: List[str] = [lease_id for _, wire in pods for lease_id in wire.release_calls]
    loser = "lse_b" if survivor.lease_id == "lse_a" else "lse_a"
    assert released == [loser]


async def test_lost_acquire_race_with_the_same_lease_releases_nothing(clock: VirtualClock) -> None:
    # The server is idempotent for an active slot, so a racing acquire is
    # handed back the SAME lease the sibling installed. Releasing it would pull
    # the shared lease out from under every pod.
    shared: LeaseStore = RedisLeaseStore(make_fake_redis(), clock=clock)
    pods = []
    for _ in range(2):
        wire = ScriptedWireClient()
        wire.acquire_responses.append(_lease(clock, "lse_shared"))
        pods.append((LeaseManager(wire, shared, config=CONFIG, clock=clock), wire))

    entries = await asyncio.gather(*(manager.acquire_if_needed("co_1", "ct_1") for manager, _ in pods))
    for manager, _ in pods:
        await manager._drain_background()

    assert [entry.lease_id for entry in entries if entry] == ["lse_shared", "lse_shared"]
    assert [lease_id for _, wire in pods for lease_id in wire.release_calls] == []


async def test_uncontended_acquire_releases_nothing(clock: VirtualClock) -> None:
    manager, _store, wire = _make_manager(clock)
    wire.acquire_responses.append(_lease(clock))
    await manager.acquire_if_needed("co_1", "ct_1")
    await manager._drain_background()
    assert wire.release_calls == []


async def test_sweep_loop_runs_and_stops(clock: VirtualClock) -> None:
    leases = InMemoryLeaseStore(clock=clock)
    reservations = InMemoryReservationStore(leases, clock=clock)
    manager = LeaseManager(
        ScriptedWireClient(),
        leases,
        reservation_store=reservations,
        # Short enough that the test does not idle, long enough that the loop
        # cannot run twice before it is stopped.
        config=LeaseConfig(sweep_interval=0.01),
        clock=clock,
    )
    swept: List[int] = []
    original = reservations.sweep_expired

    async def counting_sweep(now: Optional[float] = None) -> int:
        result = await original(now)
        swept.append(result)
        return result

    reservations.sweep_expired = counting_sweep  # type: ignore[method-assign]

    manager.start_sweep()
    manager.start_sweep()  # idempotent
    await asyncio.sleep(0.03)
    assert swept
    manager.stop()
    ticks = len(swept)
    await asyncio.sleep(0.03)
    assert len(swept) == ticks


async def test_sweep_loop_survives_a_failing_sweep(clock: VirtualClock) -> None:
    leases = InMemoryLeaseStore(clock=clock)
    reservations = InMemoryReservationStore(leases, clock=clock)
    manager = LeaseManager(
        ScriptedWireClient(),
        leases,
        reservation_store=reservations,
        config=LeaseConfig(sweep_interval=0.01),
        clock=clock,
    )
    attempts: List[int] = []

    async def failing_sweep(now: Optional[float] = None) -> int:
        attempts.append(1)
        raise RuntimeError("redis blip")

    reservations.sweep_expired = failing_sweep  # type: ignore[method-assign]
    manager.start_sweep()
    await asyncio.sleep(0.05)
    manager.stop()
    # A transient failure must not kill the loop: the next tick retries.
    assert len(attempts) > 1


async def test_resolve_config_applies_overrides(clock: VirtualClock) -> None:
    from schematic.leases import LeaseConfigOverride

    config = LeaseConfig(
        lease_size=500,
        overrides={"ct_special": LeaseConfigOverride(lease_size=25, low_water_mark=0.5)},
    )
    manager = LeaseManager(ScriptedWireClient(), InMemoryLeaseStore(clock=clock), config=config, clock=clock)

    plain = manager.resolve_config("ct_1")
    assert plain.lease_size == 500
    assert plain.low_water_mark == 0.25
    assert plain.lease_duration == 300

    special = manager.resolve_config("ct_special")
    assert special.lease_size == 25
    assert special.low_water_mark == 0.5


def test_resolve_lease_config_clamps_the_reservation_ttl() -> None:
    from schematic.leases import MAX_RESERVATION_TTL, resolve_lease_config

    resolved = resolve_lease_config(LeaseConfig(reservation_ttl=MAX_RESERVATION_TTL * 2), None, "ct_1")
    # The server refuses to hold credits longer than this, so a bigger TTL
    # would have the sweeper trail the server's own release.
    assert resolved.reservation_ttl == MAX_RESERVATION_TTL
