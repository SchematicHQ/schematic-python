"""In-memory lease slot semantics, ported from the Node SDK's store tests."""

from __future__ import annotations

import asyncio
import math

import pytest
from lease_support import VirtualClock

from schematic.leases import InMemoryLeaseStore, ReserveResult


async def _seed(store: InMemoryLeaseStore, clock: VirtualClock, *, granted: float = 100, ttl: float = 60) -> None:
    await store.replace(
        lease_id="lse_1",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=granted,
        expires_at=clock() + ttl,
    )


@pytest.fixture
def store(clock: VirtualClock) -> InMemoryLeaseStore:
    return InMemoryLeaseStore(clock=clock)


async def test_replace_installs_at_the_full_grant(store: InMemoryLeaseStore, clock: VirtualClock) -> None:
    await _seed(store, clock)
    entry = await store.get("co_1", "ct_1")
    assert entry is not None
    assert entry.granted_amount == 100
    assert entry.local_remaining_credits == 100


async def test_try_reserve_returns_the_post_debit_balance_and_charged_lease(
    store: InMemoryLeaseStore, clock: VirtualClock
) -> None:
    await _seed(store, clock)
    assert await store.try_reserve("co_1", "ct_1", 30) == ReserveResult(balance=70, lease_id="lse_1")
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.local_remaining_credits == 70


async def test_try_reserve_refuses_without_debiting(store: InMemoryLeaseStore, clock: VirtualClock) -> None:
    await _seed(store, clock)
    assert await store.try_reserve("co_1", "ct_1", 150) is None
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.local_remaining_credits == 100


async def test_try_reserve_refuses_an_expired_lease(store: InMemoryLeaseStore, clock: VirtualClock) -> None:
    await _seed(store, clock)
    clock.advance_ms(60_001)
    assert await store.try_reserve("co_1", "ct_1", 10) is None
    # The balance is stale, not spendable: the server released the lease and
    # refunded its remainder.
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.local_remaining_credits == 100


async def test_try_reserve_rejects_nan_and_infinity(store: InMemoryLeaseStore, clock: VirtualClock) -> None:
    await _seed(store, clock)
    # NaN slips through every comparison, so an unguarded debit would set the
    # balance to NaN and approve every later reserve.
    assert await store.try_reserve("co_1", "ct_1", math.nan) is None
    assert await store.try_reserve("co_1", "ct_1", -10) is None
    assert await store.try_reserve("co_1", "ct_1", math.inf) is None
    assert await store.try_reserve("co_1", "ct_1", 30) == ReserveResult(balance=70, lease_id="lse_1")
    assert await store.try_reserve("co_1", "ct_1", 80) is None


async def test_refund_caps_at_the_granted_amount(store: InMemoryLeaseStore, clock: VirtualClock) -> None:
    await _seed(store, clock)
    await store.try_reserve("co_1", "ct_1", 30)
    await store.refund("co_1", "ct_1", 20)
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.local_remaining_credits == 90
    await store.refund("co_1", "ct_1", 9999)
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.local_remaining_credits == 100


async def test_refund_pinned_to_a_stale_lease_is_dropped(store: InMemoryLeaseStore, clock: VirtualClock) -> None:
    await store.replace(
        lease_id="lse_b",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=100,
        expires_at=clock() + 60,
    )
    await store.try_reserve("co_1", "ct_1", 50)
    await store.refund("co_1", "ct_1", 30, "lse_a")
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.local_remaining_credits == 50
    await store.refund("co_1", "ct_1", 30, "lse_b")
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.local_remaining_credits == 80


async def test_concurrent_try_reserves_serialize_per_slot(store: InMemoryLeaseStore, clock: VirtualClock) -> None:
    # Per-slot atomicity: three concurrent 40-credit reserves against a
    # 100-credit lease must not oversell it.
    await _seed(store, clock)
    results = await asyncio.gather(
        store.try_reserve("co_1", "ct_1", 40),
        store.try_reserve("co_1", "ct_1", 40),
        store.try_reserve("co_1", "ct_1", 40),
    )
    successes = [r for r in results if r is not None]
    assert sorted(r.balance for r in successes) == [20, 60]
    assert [r.lease_id for r in successes] == ["lse_1", "lse_1"]
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.local_remaining_credits == 20


async def test_extend_reconciles_to_the_server_total(store: InMemoryLeaseStore, clock: VirtualClock) -> None:
    await _seed(store, clock, ttl=10)
    await store.try_reserve("co_1", "ct_1", 30)
    new_expiry = clock() + 60
    await store.extend("co_1", "ct_1", 150, new_expiry)
    entry = await store.get("co_1", "ct_1")
    assert entry is not None
    assert entry.granted_amount == 150
    assert entry.local_remaining_credits == 120
    assert entry.expires_at == new_expiry


async def test_stale_extend_total_is_a_no_op(store: InMemoryLeaseStore, clock: VirtualClock) -> None:
    await _seed(store, clock, ttl=10)
    far_expiry = clock() + 120
    await store.extend("co_1", "ct_1", 200, far_expiry)
    await store.extend("co_1", "ct_1", 150, clock() + 60)
    entry = await store.get("co_1", "ct_1")
    assert entry is not None
    assert entry.granted_amount == 200
    assert entry.local_remaining_credits == 200
    assert entry.expires_at == far_expiry


async def test_extend_pinned_to_a_stale_lease_is_dropped(store: InMemoryLeaseStore, clock: VirtualClock) -> None:
    await store.replace(
        lease_id="lse_b",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=100,
        expires_at=clock() + 60,
    )
    await store.extend("co_1", "ct_1", 150, clock() + 120, "lse_a")
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.granted_amount == 100 and entry.local_remaining_credits == 100
    await store.extend("co_1", "ct_1", 150, clock() + 120, "lse_b")
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.granted_amount == 150 and entry.local_remaining_credits == 150


async def test_drop_removes_the_slot(store: InMemoryLeaseStore, clock: VirtualClock) -> None:
    await _seed(store, clock)
    await store.drop("co_1", "ct_1")
    assert await store.get("co_1", "ct_1") is None


async def test_replace_keeps_a_live_lease_with_a_different_id(
    store: InMemoryLeaseStore, clock: VirtualClock
) -> None:
    assert await store.replace(
        lease_id="lse_1",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=100,
        expires_at=clock() + 60,
    )
    await store.try_reserve("co_1", "ct_1", 40)
    wrote = await store.replace(
        lease_id="lse_2",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=100,
        expires_at=clock() + 60,
    )
    assert wrote is False
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.lease_id == "lse_1" and entry.local_remaining_credits == 60


async def test_replace_overwrites_an_expired_lease(store: InMemoryLeaseStore, clock: VirtualClock) -> None:
    await _seed(store, clock, ttl=60)
    clock.advance_ms(60_001)
    wrote = await store.replace(
        lease_id="lse_2",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=100,
        expires_at=clock() + 60,
    )
    assert wrote is True
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.lease_id == "lse_2" and entry.local_remaining_credits == 100


async def test_replace_reconciles_an_expired_same_id_lease(store: InMemoryLeaseStore, clock: VirtualClock) -> None:
    # A stale acquire response can hand back the lease already installed (the
    # server is idempotent for an active slot) after the local row expired.
    # Rewriting would reset the balance and erase debits whose reservations are
    # still open.
    await _seed(store, clock, ttl=60)
    await store.try_reserve("co_1", "ct_1", 40)
    clock.advance_ms(61_000)
    later_expiry = clock() + 60
    wrote = await store.replace(
        lease_id="lse_1",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=150,
        expires_at=later_expiry,
    )
    assert wrote is False
    entry = await store.get("co_1", "ct_1")
    assert entry is not None
    assert entry.granted_amount == 150
    assert entry.local_remaining_credits == 110
    assert entry.expires_at == later_expiry


async def test_get_returns_a_snapshot(store: InMemoryLeaseStore, clock: VirtualClock) -> None:
    # Mutating what `get` handed back must not reach the stored slot.
    await _seed(store, clock)
    entry = await store.get("co_1", "ct_1")
    assert entry is not None
    entry.local_remaining_credits = 0
    stored = await store.get("co_1", "ct_1")
    assert stored is not None and stored.local_remaining_credits == 100
