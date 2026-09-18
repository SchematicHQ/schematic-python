"""Redis reservation table semantics, ported from the Node SDK's tests."""

from __future__ import annotations

from typing import Any

import pytest
from lease_support import VirtualClock, make_reservation

from schematic.leases import RedisLeaseStore, RedisReservationStore
from schematic.leases.redis_reservation_store import RES_TTL_GRACE_MS, SWEEP_BATCH_SIZE


@pytest.fixture
def leases(redis_client: Any, frozen_clock: VirtualClock) -> RedisLeaseStore:
    return RedisLeaseStore(redis_client, clock=frozen_clock)


@pytest.fixture
def reservations(redis_client: Any, leases: RedisLeaseStore, frozen_clock: VirtualClock) -> RedisReservationStore:
    return RedisReservationStore(redis_client, leases, clock=frozen_clock)


@pytest.fixture(autouse=True)
async def seeded_lease(leases: RedisLeaseStore, frozen_clock: VirtualClock) -> None:
    await leases.replace(
        lease_id="lse_1",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=1000,
        expires_at=frozen_clock() + 600,
    )


async def _balance(leases: RedisLeaseStore) -> float:
    entry = await leases.get("co_1", "ct_1")
    assert entry is not None
    return entry.local_remaining_credits


async def test_add_round_trips_and_indexes(
    reservations: RedisReservationStore, frozen_clock: VirtualClock
) -> None:
    await reservations.add(make_reservation(expires_at=frozen_clock() + 60))
    fetched = await reservations.get("res_1")
    assert fetched is not None
    assert fetched.credits_reserved == 100
    assert fetched.lease_id == "lse_1"
    assert fetched.company == {"id": "co_1"}
    assert await reservations.count() == 1


async def test_add_writes_the_hash_and_its_ttl_in_one_transaction(
    redis_client: Any, reservations: RedisReservationStore, frozen_clock: VirtualClock
) -> None:
    transactions: list[list[str]] = []
    original = redis_client.pipeline

    def recording_pipeline(*args: Any, **kwargs: Any) -> Any:
        pipe = original(*args, **kwargs)
        execute = pipe.execute

        async def record(*call_args: Any, **call_kwargs: Any) -> Any:
            transactions.append([str(queued[0][0]) for queued in pipe.command_stack])
            return await execute(*call_args, **call_kwargs)

        pipe.execute = record
        return pipe

    redis_client.pipeline = recording_pipeline
    try:
        await reservations.add(make_reservation(expires_at=frozen_clock() + 60))
    finally:
        redis_client.pipeline = original

    # Written separately, a crash between the two leaves a row that never
    # expires and that nothing points at once the sweeper drops its index entry.
    assert transactions == [["HSET", "PEXPIREAT"]]
    fetched = await reservations.get("res_1")
    assert fetched is not None and fetched.credits_reserved == 100


async def test_consume_refunds_the_unspent_slice(
    leases: RedisLeaseStore, reservations: RedisReservationStore, frozen_clock: VirtualClock
) -> None:
    await leases.try_reserve("co_1", "ct_1", 100)
    await reservations.add(make_reservation(expires_at=frozen_clock() + 60))
    assert await _balance(leases) == 900

    assert await reservations.consume("res_1", 30) == 30
    assert await _balance(leases) == 970
    assert await reservations.get("res_1") is None


async def test_double_consume_returns_null(
    leases: RedisLeaseStore, reservations: RedisReservationStore, frozen_clock: VirtualClock
) -> None:
    await leases.try_reserve("co_1", "ct_1", 100)
    await reservations.add(make_reservation(expires_at=frozen_clock() + 60))
    await reservations.consume("res_1", 50)
    assert await reservations.consume("res_1", 10) is None


async def test_sweep_returns_expired_holds_to_the_lease(
    leases: RedisLeaseStore, reservations: RedisReservationStore, frozen_clock: VirtualClock
) -> None:
    await leases.try_reserve("co_1", "ct_1", 100)
    await reservations.add(make_reservation(expires_at=frozen_clock() - 0.001))
    assert await reservations.sweep_expired() == 1
    assert await _balance(leases) == 1000
    assert await reservations.get("res_1") is None


async def test_a_stale_lease_hold_never_inflates_its_successor(
    leases: RedisLeaseStore, reservations: RedisReservationStore, frozen_clock: VirtualClock
) -> None:
    await leases.try_reserve("co_1", "ct_1", 100)
    await reservations.add(make_reservation(expires_at=frozen_clock() - 0.001))

    await leases.drop("co_1", "ct_1")
    await leases.replace(
        lease_id="lse_2",
        company_id="co_1",
        credit_type_id="ct_1",
        granted_amount=1000,
        expires_at=frozen_clock() + 600,
    )
    await leases.try_reserve("co_1", "ct_1", 200)

    assert await reservations.sweep_expired() == 1
    assert await _balance(leases) == 800
    assert await reservations.get("res_1") is None


async def test_reserved_credits_sums_open_holds(
    leases: RedisLeaseStore, reservations: RedisReservationStore, frozen_clock: VirtualClock
) -> None:
    await leases.try_reserve("co_1", "ct_1", 350)
    await reservations.add(make_reservation(id="res_1", credits_reserved=100, expires_at=frozen_clock() + 60))
    await reservations.add(make_reservation(id="res_2", credits_reserved=250, expires_at=frozen_clock() + 60))
    await reservations.add(
        make_reservation(id="res_3", credit_type_id="ct_2", credits_reserved=999, expires_at=frozen_clock() + 60)
    )

    assert await reservations.reserved_credits("co_1", "ct_1") == 350
    assert await reservations.reserved_credits("co_1", "ct_2") == 999

    await reservations.consume("res_1", 40)
    assert await reservations.reserved_credits("co_1", "ct_1") == 250


async def test_every_lua_call_touches_one_key(
    redis_client: Any, leases: RedisLeaseStore, reservations: RedisReservationStore, frozen_clock: VirtualClock
) -> None:
    # A multi-key script whose keys hash to different slots raises CROSSSLOT on
    # Redis Cluster, so every EVAL these stores send must touch exactly one.
    key_counts = []
    original_eval = redis_client.eval
    original_evalsha = redis_client.evalsha

    async def record_eval(script: str, numkeys: int, *args: Any) -> Any:
        key_counts.append(numkeys)
        return await original_eval(script, numkeys, *args)

    async def record_evalsha(sha: str, numkeys: int, *args: Any) -> Any:
        key_counts.append(numkeys)
        return await original_evalsha(sha, numkeys, *args)

    redis_client.eval = record_eval
    redis_client.evalsha = record_evalsha

    await leases.try_reserve("co_1", "ct_1", 200)
    await leases.refund("co_1", "ct_1", 50)
    await leases.extend("co_1", "ct_1", 1100, frozen_clock() + 120)
    await reservations.add(make_reservation(id="res_a", credits_reserved=100, expires_at=frozen_clock() + 60))
    await reservations.add(
        make_reservation(id="res_b", credits_reserved=80, expires_at=frozen_clock() - 0.001)
    )
    await reservations.consume("res_a", 40)
    await reservations.sweep_expired()

    assert key_counts
    assert set(key_counts) == {1}


async def test_sweep_reconciles_indexes_when_the_hash_has_evicted(
    leases: RedisLeaseStore, reservations: RedisReservationStore, frozen_clock: VirtualClock
) -> None:
    # A sweeper that goes silent long enough (deploy, restart, starvation) for
    # Redis to evict the reservation hash must still clean both indexes, or the
    # orphaned entry inflates reserved_credits forever.
    await leases.try_reserve("co_1", "ct_1", 100)
    await reservations.add(make_reservation(expires_at=frozen_clock() + 1))
    assert await reservations.count() == 1
    assert await reservations.reserved_credits("co_1", "ct_1") == 100

    frozen_clock.advance_ms(1000 + RES_TTL_GRACE_MS + 1)

    # Nothing is swept in the refund sense: without the hash, exactly-once
    # cannot be arbitrated across racing sweepers, so the slice waits for the
    # lease to expire server-side.
    assert await reservations.sweep_expired() == 0
    assert await reservations.count() == 0
    assert await reservations.reserved_credits("co_1", "ct_1") == 0
    assert await _balance(leases) == 900


async def test_sweep_drops_an_unparseable_index_member(
    redis_client: Any, reservations: RedisReservationStore, frozen_clock: VirtualClock
) -> None:
    # Only `add` writes members, so this cannot happen; a member that does not
    # decode must still be removed rather than re-read by every later sweep.
    await redis_client.zadd(
        "schematic:credit-reservations:byExpiry", {"garbage": int(frozen_clock() * 1000) - 1}
    )
    assert await reservations.sweep_expired() == 0
    assert await reservations.count() == 0


async def test_sweep_pages_through_a_backlog(
    leases: RedisLeaseStore, reservations: RedisReservationStore, frozen_clock: VirtualClock
) -> None:
    count = SWEEP_BATCH_SIZE + 44
    await leases.try_reserve("co_1", "ct_1", count)
    for index in range(count):
        await reservations.add(
            make_reservation(id=f"res_{index}", credits_reserved=1, expires_at=frozen_clock() - 0.001)
        )
    assert await reservations.sweep_expired() == count
    assert await _balance(leases) == 1000
    assert await reservations.count() == 0
    assert await reservations.reserved_credits("co_1", "ct_1") == 0


async def test_key_layout_and_hash_fields_match_the_node_sdk(
    redis_client: Any, reservations: RedisReservationStore, frozen_clock: VirtualClock
) -> None:
    expires_at = frozen_clock() + 60
    await reservations.add(make_reservation(expires_at=expires_at))
    raw = await redis_client.hgetall("schematic:credit-reservation:res_1")
    assert raw == {
        "id": "res_1",
        "leaseId": "lse_1",
        "companyId": "co_1",
        "creditTypeId": "ct_1",
        "eventSubtype": "inference_tokens",
        "quantityReserved": "10",
        "creditsReserved": "100",
        "consumptionRate": "10",
        "expiresAt": str(int(round(expires_at * 1000))),
        "evalCtx": '{"company":{"id":"co_1"}}',
    }
    assert await redis_client.zrange("schematic:credit-reservations:byExpiry", 0, -1) == ["co_1|ct_1|res_1"]
    assert await redis_client.hgetall("schematic:credit-reservations:byCredit:co_1:ct_1") == {"res_1": "100"}
    ttl_ms = await redis_client.pttl("schematic:credit-reservation:res_1")
    assert 60_000 < ttl_ms <= 60_000 + RES_TTL_GRACE_MS
