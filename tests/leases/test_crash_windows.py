"""The two bounded-leak windows, on both backends.

A crash between the two steps of a transition must strand locally held credits
(which the server reclaims at lease expiry) rather than enable a double-spend.
The debit and the claim are durable first; the record and the refund are what
may be lost.
"""

from __future__ import annotations

from typing import Any, Awaitable, Tuple, cast

import pytest
from lease_support import CrashingRefundLeaseStore, VirtualClock, make_fake_redis, make_reservation

from schematic.leases import (
    InMemoryLeaseStore,
    InMemoryReservationStore,
    LeaseStore,
    RedisLeaseStore,
    RedisReservationStore,
    ReservationStore,
)

BACKENDS = ("in_memory", "redis")


@pytest.fixture(autouse=True)
def _frozen(frozen_clock: VirtualClock) -> VirtualClock:
    """fakeredis reads TIME from the process clock, so the virtual clock is it."""
    return frozen_clock


def _make_stores(
    backend: str, clock: VirtualClock
) -> Tuple[LeaseStore, ReservationStore, CrashingRefundLeaseStore]:
    leases: LeaseStore
    reservations: ReservationStore
    if backend == "in_memory":
        leases = InMemoryLeaseStore(clock=clock)
        crash = CrashingRefundLeaseStore(leases)
        reservations = InMemoryReservationStore(crash, clock=clock)
    else:
        client = make_fake_redis()
        leases = RedisLeaseStore(client, clock=clock)
        crash = CrashingRefundLeaseStore(leases)
        reservations = RedisReservationStore(client, crash, clock=clock)
    return leases, reservations, crash


async def _seed(leases: LeaseStore, clock: VirtualClock, ttl: float = 60) -> None:
    await leases.replace(
        lease_id="lse_1",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=1000,
        expires_at=clock() + ttl,
    )


async def _balance(leases: LeaseStore) -> float:
    entry = await leases.get("co_1", "ct_1")
    assert entry is not None
    return entry.local_remaining_credits


@pytest.mark.parametrize("backend", BACKENDS)
async def test_debit_without_record_leaks_only_the_hold(backend: str, frozen_clock: VirtualClock) -> None:
    leases, reservations, _crash = _make_stores(backend, frozen_clock)
    await _seed(leases, frozen_clock)

    # The crash: the atomic debit landed, the reservation record never did.
    assert await leases.try_reserve("co_1", "ct_1", 100) == 900

    # Exactly the reserved amount is stranded, and it is invisible to the
    # reservation table, so no sweep can ever refund it.
    assert await _balance(leases) == 900
    assert await reservations.reserved_credits("co_1", "ct_1") == 0
    assert await reservations.sweep_expired(frozen_clock() + 3600) == 0
    assert await _balance(leases) == 900


@pytest.mark.parametrize("backend", BACKENDS)
async def test_debit_leak_is_reclaimed_at_lease_expiry(backend: str, frozen_clock: VirtualClock) -> None:
    leases, _reservations, _crash = _make_stores(backend, frozen_clock)
    await _seed(leases, frozen_clock)
    assert await leases.try_reserve("co_1", "ct_1", 100) == 900

    frozen_clock.advance_ms(60_001)
    # The stale balance is never served again, and the successor installs at
    # the full grant: the leak does not outlive the lease.
    assert await leases.try_reserve("co_1", "ct_1", 1) is None
    assert await leases.replace(
        lease_id="lse_2",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=1000,
        expires_at=frozen_clock() + 120,
    )
    assert await _balance(leases) == 1000


@pytest.mark.parametrize("backend", BACKENDS)
async def test_a_retried_check_settles_independently(backend: str, frozen_clock: VirtualClock) -> None:
    leases, reservations, _crash = _make_stores(backend, frozen_clock)
    await _seed(leases, frozen_clock, ttl=3600)
    # The crashed attempt, then the retry with a fresh reservation.
    assert await leases.try_reserve("co_1", "ct_1", 100) == 900
    assert await leases.try_reserve("co_1", "ct_1", 100) == 800
    await reservations.add(make_reservation(id="res_retry", expires_at=frozen_clock() + 60))

    assert await reservations.consume("res_retry", 40) == 40
    # 1000 less the 100 leaked and the 40 consumed: the retry's unspent 60 came
    # back exactly once, the leaked 100 stayed leaked.
    assert await _balance(leases) == 860

    assert await reservations.consume("res_retry", 40) is None
    assert await reservations.sweep_expired(frozen_clock() + 3600) == 0
    assert await _balance(leases) == 860


@pytest.mark.parametrize("backend", BACKENDS)
async def test_crash_before_refund_keeps_the_claim(backend: str, frozen_clock: VirtualClock) -> None:
    leases, reservations, crash = _make_stores(backend, frozen_clock)
    await _seed(leases, frozen_clock)
    assert await leases.try_reserve("co_1", "ct_1", 100) == 900
    await reservations.add(make_reservation(expires_at=frozen_clock() + 60))

    crash.arm()
    with pytest.raises(RuntimeError, match="simulated crash before refund"):
        await reservations.consume("res_1", 30)

    # The claim survived, so the reservation is gone everywhere and nothing can
    # double-spend; the 70-credit refund is lost, bounded by the hold.
    assert await reservations.get("res_1") is None
    assert await reservations.reserved_credits("co_1", "ct_1") == 0
    assert await _balance(leases) == 900

    # Neither a retried settle nor the sweeper can refund a claimed hold.
    assert await reservations.consume("res_1", 30) is None
    assert await reservations.sweep_expired(frozen_clock() + 3600) == 0
    assert await _balance(leases) == 900


@pytest.mark.parametrize("backend", BACKENDS)
async def test_crash_before_refund_never_leaks_into_a_successor(
    backend: str, frozen_clock: VirtualClock
) -> None:
    leases, reservations, crash = _make_stores(backend, frozen_clock)
    await _seed(leases, frozen_clock)
    assert await leases.try_reserve("co_1", "ct_1", 100) == 900
    await reservations.add(make_reservation(expires_at=frozen_clock() + 60))

    crash.arm()
    with pytest.raises(RuntimeError, match="simulated crash before refund"):
        await reservations.consume("res_1", 30)

    frozen_clock.advance_ms(60_001)
    assert await leases.try_reserve("co_1", "ct_1", 1) is None
    assert await leases.replace(
        lease_id="lse_2",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=1000,
        expires_at=frozen_clock() + 120,
    )
    # A very late retried settle must not push the lost refund into lse_2.
    assert await reservations.consume("res_1", 0) is None
    assert await _balance(leases) == 1000


async def test_crash_after_the_claim_is_reconciled_without_a_refund(frozen_clock: VirtualClock) -> None:
    # Redis only: a process death after the claim but before the index cleanup
    # leaves the per-tenant index over-counting. The sweeper reconciles it, and
    # deliberately does not refund: without the reservation hash, exactly-once
    # cannot be arbitrated across racing sweepers.
    client = make_fake_redis()
    leases = RedisLeaseStore(client, clock=frozen_clock)
    reservations = RedisReservationStore(client, leases, clock=frozen_clock)
    await _seed(leases, frozen_clock)
    assert await leases.try_reserve("co_1", "ct_1", 100) == 900
    await reservations.add(make_reservation(expires_at=frozen_clock() - 0.001))

    original_evalsha = client.evalsha
    armed = True

    async def crash_after_claim(sha: str, numkeys: int, *args: Any) -> Any:
        nonlocal armed
        result = await cast(Awaitable[Any], original_evalsha(sha, numkeys, *args))
        if armed and isinstance(result, list):
            armed = False
            raise RuntimeError("simulated crash after claim")
        return result

    client.evalsha = crash_after_claim  # type: ignore[method-assign]

    with pytest.raises(RuntimeError, match="simulated crash after claim"):
        await reservations.consume("res_1", 30)
    client.evalsha = original_evalsha  # type: ignore[method-assign]

    # The orphaned index field still counts the hold...
    assert await reservations.reserved_credits("co_1", "ct_1") == 100
    # ...until the sweeper reconciles it, without refunding.
    assert await reservations.sweep_expired() == 0
    assert await reservations.reserved_credits("co_1", "ct_1") == 0
    assert await reservations.count() == 0
    assert await _balance(leases) == 900
