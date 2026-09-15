"""In-memory reservation table semantics, ported from the Node SDK's tests."""

from __future__ import annotations

import pytest
from lease_support import VirtualClock, make_reservation

from schematic.leases import InMemoryLeaseStore, InMemoryReservationStore


@pytest.fixture
def leases(clock: VirtualClock) -> InMemoryLeaseStore:
    return InMemoryLeaseStore(clock=clock)


@pytest.fixture
def reservations(leases: InMemoryLeaseStore, clock: VirtualClock) -> InMemoryReservationStore:
    return InMemoryReservationStore(leases, clock=clock)


@pytest.fixture(autouse=True)
async def seeded_lease(leases: InMemoryLeaseStore, clock: VirtualClock) -> None:
    await leases.replace(
        lease_id="lse_1",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=1000,
        expires_at=clock() + 60,
    )


async def _balance(leases: InMemoryLeaseStore) -> float:
    entry = await leases.get("co_1", "ct_1")
    assert entry is not None
    return entry.local_remaining_credits


async def test_consume_refunds_the_unspent_slice(
    leases: InMemoryLeaseStore, reservations: InMemoryReservationStore, clock: VirtualClock
) -> None:
    await leases.try_reserve("co_1", "ct_1", 100)
    await reservations.add(make_reservation(expires_at=clock() + 60))
    assert await _balance(leases) == 900

    assert await reservations.consume("res_1", 30) == 30
    assert await _balance(leases) == 970
    assert await reservations.get("res_1") is None


async def test_consume_clamps_to_the_hold(
    leases: InMemoryLeaseStore, reservations: InMemoryReservationStore, clock: VirtualClock
) -> None:
    await leases.try_reserve("co_1", "ct_1", 100)
    await reservations.add(make_reservation(expires_at=clock() + 60))
    assert await reservations.consume("res_1", 999) == 100
    assert await _balance(leases) == 900


async def test_consume_of_a_missing_reservation_is_null(reservations: InMemoryReservationStore) -> None:
    assert await reservations.consume("nope", 10) is None


async def test_consume_is_exactly_once(
    leases: InMemoryLeaseStore, reservations: InMemoryReservationStore, clock: VirtualClock
) -> None:
    await leases.try_reserve("co_1", "ct_1", 100)
    await reservations.add(make_reservation(expires_at=clock() + 60))
    assert await reservations.consume("res_1", 30) == 30
    assert await reservations.consume("res_1", 30) is None
    assert await _balance(leases) == 970


async def test_a_stale_lease_hold_never_inflates_its_successor(
    leases: InMemoryLeaseStore, reservations: InMemoryReservationStore, clock: VirtualClock
) -> None:
    await leases.try_reserve("co_1", "ct_1", 100)
    await reservations.add(make_reservation(expires_at=clock() - 0.001))

    # lse_1 expires and lse_2 takes the slot, partially debited.
    await leases.drop("co_1", "ct_1")
    await leases.replace(
        lease_id="lse_2",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=1000,
        expires_at=clock() + 60,
    )
    await leases.try_reserve("co_1", "ct_1", 200)

    # Sweeping lse_1's hold must not credit lse_2: that slice went back to the
    # company balance when lse_1 expired server-side.
    assert await reservations.sweep_expired() == 1
    assert await _balance(leases) == 800

    # An explicit consume of a stale-lease hold is dropped the same way.
    await reservations.add(make_reservation(id="res_2", expires_at=clock() + 60))
    await reservations.consume("res_2", 0)
    assert await _balance(leases) == 800


async def test_sweep_refunds_expired_holds_only(
    leases: InMemoryLeaseStore, reservations: InMemoryReservationStore, clock: VirtualClock
) -> None:
    await leases.try_reserve("co_1", "ct_1", 100)
    await reservations.add(make_reservation(expires_at=clock() + 10))
    assert await reservations.sweep_expired() == 0
    assert await reservations.count() == 1

    clock.advance_ms(10_001)
    assert await reservations.sweep_expired() == 1
    assert await reservations.get("res_1") is None
    assert await _balance(leases) == 1000


async def test_reserved_credits_sums_the_slot_only(reservations: InMemoryReservationStore) -> None:
    await reservations.add(make_reservation(id="res_1", credits_reserved=100))
    await reservations.add(make_reservation(id="res_2", credits_reserved=250))
    await reservations.add(make_reservation(id="res_3", credit_type_id="ct_2", credits_reserved=999))
    await reservations.add(make_reservation(id="res_4", company_id="co_2", credits_reserved=999))

    assert await reservations.reserved_credits("co_1", "ct_1") == 350
    assert await reservations.reserved_credits("co_1", "ct_2") == 999
    assert await reservations.reserved_credits("co_unknown", "ct_1") == 0


async def test_reserved_credits_drops_a_consumed_hold(
    leases: InMemoryLeaseStore, reservations: InMemoryReservationStore, clock: VirtualClock
) -> None:
    await leases.try_reserve("co_1", "ct_1", 100)
    await reservations.add(make_reservation(expires_at=clock() + 60))
    assert await reservations.reserved_credits("co_1", "ct_1") == 100
    await reservations.consume("res_1", 30)
    assert await reservations.reserved_credits("co_1", "ct_1") == 0
