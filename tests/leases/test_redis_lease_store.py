"""Redis lease slot semantics, ported from the Node SDK's Redis store tests.

The shared-backend cases here are the ones the vectors cannot express: two pods
on one Redis, and rows that are expired but not yet evicted.
"""

from __future__ import annotations

import asyncio
import math
from typing import Any

import pytest
from lease_support import VirtualClock

from schematic.leases import RedisLeaseStore
from schematic.leases.redis_lease_store import LEASE_TTL_GRACE_MS


@pytest.fixture
def store(redis_client: Any, frozen_clock: VirtualClock) -> RedisLeaseStore:
    return RedisLeaseStore(redis_client, clock=frozen_clock)


async def _seed(store: RedisLeaseStore, clock: VirtualClock, *, granted: float = 100, ttl: float = 60) -> bool:
    return await store.replace(
        lease_id="lse_1",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=granted,
        expires_at=clock() + ttl,
    )


async def test_replace_installs_a_fresh_lease(store: RedisLeaseStore, frozen_clock: VirtualClock) -> None:
    assert await _seed(store, frozen_clock) is True
    entry = await store.get("co_1", "ct_1")
    assert entry is not None
    assert entry.lease_id == "lse_1"
    assert entry.granted_amount == 100
    assert entry.local_remaining_credits == 100


async def test_replace_preserves_debits_when_the_same_live_lease_is_rewritten(
    store: RedisLeaseStore, frozen_clock: VirtualClock
) -> None:
    await _seed(store, frozen_clock, granted=1000)
    await store.try_reserve("co_1", "ct_1", 400)
    # A second pod acquires and is handed the same lease back.
    assert await _seed(store, frozen_clock, granted=1000) is False
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.local_remaining_credits == 600


async def test_replace_reconciles_an_expired_same_id_lease(
    store: RedisLeaseStore, frozen_clock: VirtualClock
) -> None:
    await _seed(store, frozen_clock, granted=1000)
    await store.try_reserve("co_1", "ct_1", 400)
    frozen_clock.advance_ms(61_000)
    later_expiry = frozen_clock() + 60
    wrote = await store.replace(
        lease_id="lse_1",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=1500,
        expires_at=later_expiry,
    )
    assert wrote is False
    entry = await store.get("co_1", "ct_1")
    assert entry is not None
    assert entry.granted_amount == 1500
    assert entry.local_remaining_credits == 1100
    assert entry.expires_at == later_expiry


async def test_replace_keeps_a_different_live_lease(store: RedisLeaseStore, frozen_clock: VirtualClock) -> None:
    # Two pods race the first acquire: the loser must not clobber the winner's
    # already-debited balance.
    await store.replace(
        lease_id="lse_winner",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=1000,
        expires_at=frozen_clock() + 60,
    )
    await store.try_reserve("co_1", "ct_1", 400)
    wrote = await store.replace(
        lease_id="lse_loser",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=1000,
        expires_at=frozen_clock() + 60,
    )
    assert wrote is False
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.lease_id == "lse_winner" and entry.local_remaining_credits == 600


async def test_try_reserve_gates_the_shared_balance(store: RedisLeaseStore, frozen_clock: VirtualClock) -> None:
    # Three concurrent 40-credit reserves against a 100-credit lease: the Lua
    # check-and-debit must not oversell it.
    await _seed(store, frozen_clock)
    results = await asyncio.gather(
        store.try_reserve("co_1", "ct_1", 40),
        store.try_reserve("co_1", "ct_1", 40),
        store.try_reserve("co_1", "ct_1", 40),
    )
    assert sorted(r for r in results if r is not None) == [20, 60]
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.local_remaining_credits == 20


async def test_try_reserve_refuses_an_expired_but_unevicted_row(
    store: RedisLeaseStore, frozen_clock: VirtualClock
) -> None:
    await _seed(store, frozen_clock, ttl=60)
    # Past the declared expiry but inside the TTL grace, so the row is still
    # readable; the script must still refuse it.
    frozen_clock.advance_ms(60_000 + LEASE_TTL_GRACE_MS / 2)
    assert await store.get("co_1", "ct_1") is not None
    assert await store.try_reserve("co_1", "ct_1", 10) is None
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.local_remaining_credits == 100


async def test_try_reserve_rejects_nan_before_it_reaches_the_script(
    store: RedisLeaseStore, frozen_clock: VirtualClock
) -> None:
    # The string form of NaN parses back to a Lua nan and would poison the
    # SHARED balance for every pod.
    await _seed(store, frozen_clock)
    assert await store.try_reserve("co_1", "ct_1", math.nan) is None
    assert await store.try_reserve("co_1", "ct_1", -10) is None
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.local_remaining_credits == 100
    assert await store.try_reserve("co_1", "ct_1", 30) == 70


async def test_fractional_credits_survive_the_round_trip(
    store: RedisLeaseStore, frozen_clock: VirtualClock
) -> None:
    await _seed(store, frozen_clock, granted=10)
    assert await store.try_reserve("co_1", "ct_1", 2.5) == 7.5
    await store.refund("co_1", "ct_1", 1.25)
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.local_remaining_credits == 8.75


async def test_refund_caps_at_the_granted_amount(store: RedisLeaseStore, frozen_clock: VirtualClock) -> None:
    await _seed(store, frozen_clock)
    await store.try_reserve("co_1", "ct_1", 30)
    await store.refund("co_1", "ct_1", 9999)
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.local_remaining_credits == 100


async def test_refund_pinned_to_a_stale_lease_is_dropped(
    store: RedisLeaseStore, frozen_clock: VirtualClock
) -> None:
    await store.replace(
        lease_id="lse_b",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=100,
        expires_at=frozen_clock() + 60,
    )
    await store.try_reserve("co_1", "ct_1", 50)
    await store.refund("co_1", "ct_1", 30, "lse_a")
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.local_remaining_credits == 50
    await store.refund("co_1", "ct_1", 30, "lse_b")
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.local_remaining_credits == 80


async def test_extend_falls_back_to_the_configured_duration(
    redis_client: Any, frozen_clock: VirtualClock
) -> None:
    store = RedisLeaseStore(redis_client, default_lease_duration=0.25, clock=frozen_clock)
    # A short initial expiry so the fallback is a forward move.
    await store.replace(
        lease_id="lse_1",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=100,
        expires_at=frozen_clock() + 0.1,
    )
    await store.extend("co_1", "ct_1", 150)
    entry = await store.get("co_1", "ct_1")
    assert entry is not None
    assert entry.granted_amount == 150
    assert entry.expires_at == pytest.approx(frozen_clock() + 0.25)


async def test_extend_pinned_to_a_stale_lease_is_dropped(
    store: RedisLeaseStore, frozen_clock: VirtualClock
) -> None:
    await store.replace(
        lease_id="lse_b",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=100,
        expires_at=frozen_clock() + 60,
    )
    await store.extend("co_1", "ct_1", 150, frozen_clock() + 120, "lse_a")
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.granted_amount == 100 and entry.local_remaining_credits == 100
    await store.extend("co_1", "ct_1", 150, frozen_clock() + 120, "lse_b")
    entry = await store.get("co_1", "ct_1")
    assert entry is not None and entry.granted_amount == 150 and entry.local_remaining_credits == 150


async def test_concurrent_sibling_extends_converge_on_the_server_total(
    redis_client: Any, frozen_clock: VirtualClock
) -> None:
    # Two pods on one Redis. Per-process single-flight cannot serialize them,
    # so both wire calls go out against the same stale read (granted=100); the
    # server lands B's total (150) then A's (200). Each pod applies the TOTAL
    # it was handed, so the slot converges on 200, never 250.
    pod_a = RedisLeaseStore(redis_client, clock=frozen_clock)
    pod_b = RedisLeaseStore(redis_client, clock=frozen_clock)
    await pod_a.replace(
        lease_id="lse_1",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=100,
        expires_at=frozen_clock() + 60,
    )
    await pod_b.extend("co_1", "ct_1", 150, frozen_clock() + 90, "lse_1")
    await pod_a.extend("co_1", "ct_1", 200, frozen_clock() + 120, "lse_1")
    entry = await pod_a.get("co_1", "ct_1")
    assert entry is not None and entry.granted_amount == 200 and entry.local_remaining_credits == 200

    # Out-of-order arrival: the larger total lands first and the superseded one
    # is a no-op that never pulls the expiry back.
    await pod_a.replace(
        lease_id="lse_2",
        company_id="co_1",
        credit_type_id="ct_2",
        granted_amount=100,
        expires_at=frozen_clock() + 60,
    )
    far_expiry = frozen_clock() + 120
    await pod_a.extend("co_1", "ct_2", 200, far_expiry, "lse_2")
    await pod_b.extend("co_1", "ct_2", 150, frozen_clock() + 90, "lse_2")
    entry = await pod_a.get("co_1", "ct_2")
    assert entry is not None
    assert entry.granted_amount == 200
    assert entry.local_remaining_credits == 200
    assert entry.expires_at == far_expiry


async def test_drop_removes_the_hash(store: RedisLeaseStore, frozen_clock: VirtualClock) -> None:
    await _seed(store, frozen_clock)
    await store.drop("co_1", "ct_1")
    assert await store.get("co_1", "ct_1") is None


async def test_key_layout_and_hash_fields_match_the_node_sdk(
    store: RedisLeaseStore, redis_client: Any, frozen_clock: VirtualClock
) -> None:
    # Node and Python pods share one Redis, so the key, the camelCase field
    # names, and the millisecond instants have to match exactly.
    expires_at = frozen_clock() + 60
    await store.replace(
        lease_id="lse_1",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=1000,
        expires_at=expires_at,
    )
    key = store.hash_key("co_1", "ct_1")
    assert key == "schematic:credit-lease:co_1:ct_1"
    raw = await redis_client.hgetall(key)
    assert raw == {
        "leaseId": "lse_1",
        "companyId": "co_1",
        "creditTypeId": "ct_1",
        "grantedAmount": "1000",
        "localRemainingCredits": "1000",
        "expiresAt": str(int(round(expires_at * 1000))),
    }
    # The row outlives its expiry by the grace window so the sweeper can still
    # read it.
    ttl_ms = await redis_client.pttl(key)
    assert 60_000 < ttl_ms <= 60_000 + LEASE_TTL_GRACE_MS


async def test_a_flushed_script_cache_falls_back_to_eval(
    store: RedisLeaseStore, redis_client: Any, frozen_clock: VirtualClock
) -> None:
    # A Redis that restarts (or is flushed) loses the cached script and answers
    # NOSCRIPT; the store re-sends the body rather than failing the reserve.
    await _seed(store, frozen_clock)
    assert await store.try_reserve("co_1", "ct_1", 10) == 90
    await redis_client.script_flush()
    assert await store.try_reserve("co_1", "ct_1", 10) == 80
