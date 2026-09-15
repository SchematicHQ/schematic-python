"""Redis-backed reservation table: one hash per hold, two secondary indexes.

Key layout, hash fields (camelCase), millisecond instants, the claim script,
and the TTL grace window match the Node SDK, so Node and Python pods sharing
one Redis read each other's holds.

Every mutation is a single-key operation (or single-key Lua), so the store is
correct on standalone and clustered Redis alike: the unspent-slice refund is
delegated to the lease store rather than reaching across to the lease hash
inside a multi-key script.
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional, Tuple

from .lease_store import LeaseStore
from .redis_lease_store import DEFAULT_KEY_PREFIX, LuaScript, decode_hash, format_amount, to_epoch_ms, to_str
from .reservation_store import ReservationStore, clamp_consumption
from .types import Clock, ReservationRecord

RES_KEY_NAMESPACE = "credit-reservation:"
# Sorted set scoring open reservations by expiry so the sweeper can pop expired
# entries in O(log n). Members encode the full (company, credit, id) tuple.
RES_INDEX_KEY = "credit-reservations:byExpiry"
# Per-(company, credit) index of open holds, one hash of id -> creditsReserved,
# so reserved_credits reads a tenant's holds with one HGETALL. The hash is also
# the source of truth for that sum: a field exists exactly while its
# reservation is open and unrefunded.
RES_BYCREDIT_NAMESPACE = "credit-reservations:byCredit:"
# Buffer past expiry before Redis evicts the row, so the sweeper has a window
# to refund.
RES_TTL_GRACE_MS = 30_000

# Page size for the sweeper's ZRANGEBYSCORE. Without a limit, a backlog of
# expired holds (after a Redis outage or a long pod pause) would come back as
# one giant reply on every pod's next tick; paging bounds the reply while the
# per-member ZREM keeps offset 0 advancing through the backlog.
SWEEP_BATCH_SIZE = 256
# Upper bound on pages per tick: keeps one sweep's work bounded and guards
# against an endless loop if ZREM persistently fails. Anything left over is
# picked up next tick.
MAX_SWEEP_BATCHES = 16

# Atomic claim: read the reservation hash and delete it in one step, returning
# its fields (or nil if it was already gone). Touches a single key. The atomic
# read-then-delete is what makes consume exactly-once: of two racing callers (a
# normal settle and a sweeper, say) only one gets the fields back and proceeds
# to refund. The refund to the lease hash is a separate single-key op; a crash
# in the gap leaves the unspent slice held on the lease until the lease itself
# expires, never double-refunded.
CLAIM_SCRIPT = """
local raw = redis.call('HGETALL', KEYS[1])
if #raw == 0 then return nil end
redis.call('DEL', KEYS[1])
return raw
"""


class RedisReservationStore(ReservationStore):
    """Reservation table in Redis, refunding through a lease store it is given.

    ``client`` is a connected ``redis.asyncio.Redis``.
    """

    def __init__(
        self,
        client: Any,
        lease_store: LeaseStore,
        *,
        key_prefix: str = DEFAULT_KEY_PREFIX,
        clock: Clock = time.time,
    ) -> None:
        self._client = client
        self._lease_store = lease_store
        self._key_prefix = key_prefix
        self._clock = clock
        self._claim = LuaScript(CLAIM_SCRIPT)

    def _hash_key(self, reservation_id: str) -> str:
        return f"{self._key_prefix}{RES_KEY_NAMESPACE}{reservation_id}"

    def _index_key(self) -> str:
        return f"{self._key_prefix}{RES_INDEX_KEY}"

    def _by_credit_key(self, company_id: str, credit_type_id: str) -> str:
        return f"{self._key_prefix}{RES_BYCREDIT_NAMESPACE}{company_id}:{credit_type_id}"

    async def add(self, reservation: ReservationRecord) -> None:
        expires_ms = int(to_epoch_ms(reservation.expires_at))
        hash_key = self._hash_key(reservation.id)
        # The hash goes out first so the reservation exists before anything
        # references it. These are independent single-key ops rather than one
        # multi-key script: a partial failure at worst leaves an un-indexed
        # reservation that the TTL reaps, never a double-spend.
        await self._client.hset(
            hash_key,
            mapping={
                "id": reservation.id,
                "leaseId": reservation.lease_id,
                "companyId": reservation.company_id,
                "creditTypeId": reservation.credit_type_id,
                "eventSubtype": reservation.event_subtype,
                "quantityReserved": format_amount(reservation.quantity_reserved),
                "creditsReserved": format_amount(reservation.credits_reserved),
                "consumptionRate": format_amount(reservation.consumption_rate),
                "expiresAt": str(expires_ms),
                "evalCtx": _encode_eval_ctx(reservation),
            },
        )
        await self._client.pexpireat(hash_key, expires_ms + RES_TTL_GRACE_MS)
        member = _encode_member(reservation.company_id, reservation.credit_type_id, reservation.id)
        await self._client.zadd(self._index_key(), {member: expires_ms})
        await self._client.hset(
            self._by_credit_key(reservation.company_id, reservation.credit_type_id),
            reservation.id,
            format_amount(reservation.credits_reserved),
        )

    async def get(self, reservation_id: str) -> Optional[ReservationRecord]:
        raw = decode_hash(await self._client.hgetall(self._hash_key(reservation_id)))
        if not raw.get("id"):
            return None
        return _decode_reservation(raw)

    async def consume(self, reservation_id: str, credits_consumed: float) -> Optional[float]:
        claimed = await self._claim.run(self._client, [self._hash_key(reservation_id)], [])
        raw = _decode_flat(claimed)
        if not raw or not raw.get("id"):
            return None

        company_id = raw["companyId"]
        credit_type_id = raw["creditTypeId"]
        reserved = float(raw.get("creditsReserved", "0"))

        # Index cleanup, single-key ops. The per-tenant hash loses the slice
        # BEFORE the refund below, so the lease (local remaining plus this
        # hash) never transiently double-counts it.
        member = _encode_member(company_id, credit_type_id, reservation_id)
        await _ignore_errors(self._client.zrem(self._index_key(), member))
        await _ignore_errors(self._client.hdel(self._by_credit_key(company_id, credit_type_id), reservation_id))

        consumed = clamp_consumption(credits_consumed, reserved)
        refund = reserved - consumed
        if refund > 0:
            # The lease store owns the lease hash, which keeps this cross-key
            # write out of a single Lua script. Pinned to the reservation's
            # lease so a hold carved out of an expired lease cannot inflate a
            # successor's balance.
            await self._lease_store.refund(company_id, credit_type_id, refund, raw.get("leaseId"))
        return consumed

    async def reserved_credits(self, company_id: str, credit_type_id: str) -> float:
        raw = await _ignore_errors(self._client.hgetall(self._by_credit_key(company_id, credit_type_id)))
        total = 0.0
        for value in decode_hash(raw).values():
            try:
                total += float(value)
            except ValueError:
                continue
        return total

    async def sweep_expired(self, now: Optional[float] = None) -> int:
        cutoff = int(to_epoch_ms(self._clock() if now is None else now))
        swept = 0
        # Page through expired members rather than fetching them all at once.
        # Each processed member is removed below, so re-reading at offset 0
        # advances through the backlog.
        for _ in range(MAX_SWEEP_BATCHES):
            expired = await self._client.zrangebyscore(
                self._index_key(), 0, cutoff, start=0, num=SWEEP_BATCH_SIZE
            )
            if not expired:
                break
            for member in expired:
                member_str = to_str(member)
                decoded = _decode_member(member_str)
                if decoded is None:
                    # Nothing but `add` writes members, so this is
                    # belt-and-braces: drop it rather than let it wedge the
                    # sweeper.
                    await _ignore_errors(self._client.zrem(self._index_key(), member_str))
                    continue
                company_id, credit_type_id, reservation_id = decoded
                refunded = await self.consume(reservation_id, 0)
                # Always drop the member just read. On the success path
                # `consume` already removed it, so this is idempotent; it also
                # covers the hash-evicted path below.
                await _ignore_errors(self._client.zrem(self._index_key(), member_str))
                if refunded is not None:
                    swept += 1
                    continue
                # No reservation hash: either a racing settle consumed it (and
                # reconciled the byCredit field, making this a no-op) or the
                # hash TTL-evicted before the sweeper reached it, orphaning the
                # field. Reconcile so reserved_credits stops summing an evicted
                # hold. Deliberately no refund: without the hash, exactly-once
                # cannot be arbitrated across racing sweepers, so the slice
                # waits for the lease to expire server-side.
                await _ignore_errors(
                    self._client.hdel(self._by_credit_key(company_id, credit_type_id), reservation_id)
                )
            if len(expired) < SWEEP_BATCH_SIZE:
                break
        return swept

    async def count(self) -> int:
        result = await _ignore_errors(self._client.zcard(self._index_key()))
        return int(result or 0)


def _encode_member(company_id: str, credit_type_id: str, reservation_id: str) -> str:
    """Expiry-index members carry the whole tuple.

    The sweeper needs company and credit to clean the per-tenant hash even
    after the reservation hash has TTL-evicted, at which point the claim
    returns nil and cannot report them; otherwise the orphaned field would
    inflate reserved_credits forever. The delimiter is absent from Schematic
    ids and from the reservation id.
    """
    return f"{company_id}|{credit_type_id}|{reservation_id}"


def _decode_member(member: str) -> Optional[Tuple[str, str, str]]:
    parts = member.split("|")
    if len(parts) != 3:
        return None
    return parts[0], parts[1], parts[2]


def _encode_eval_ctx(reservation: ReservationRecord) -> str:
    ctx: Dict[str, Any] = {}
    if reservation.company is not None:
        ctx["company"] = reservation.company
    if reservation.user is not None:
        ctx["user"] = reservation.user
    # Compact, like the Node SDK writes it, so a shared row reads identically.
    return json.dumps(ctx, separators=(",", ":"))


def _decode_flat(raw: Any) -> Dict[str, str]:
    """Decode the flat [field, value, ...] reply the claim script returns."""
    if not raw or not isinstance(raw, (list, tuple)):
        return {}
    items: List[str] = [to_str(item) for item in raw]
    return {items[i]: items[i + 1] for i in range(0, len(items) - 1, 2)}


def _decode_reservation(raw: Dict[str, str]) -> ReservationRecord:
    ctx: Dict[str, Any] = {}
    if raw.get("evalCtx"):
        try:
            ctx = json.loads(raw["evalCtx"])
        except ValueError:
            ctx = {}
    return ReservationRecord(
        id=raw["id"],
        lease_id=raw.get("leaseId", ""),
        company_id=raw.get("companyId", ""),
        credit_type_id=raw.get("creditTypeId", ""),
        event_subtype=raw.get("eventSubtype", ""),
        quantity_reserved=float(raw.get("quantityReserved", "0")),
        credits_reserved=float(raw.get("creditsReserved", "0")),
        consumption_rate=float(raw.get("consumptionRate", "0")),
        expires_at=float(raw.get("expiresAt", "0")) / 1000.0,
        company=ctx.get("company"),
        user=ctx.get("user"),
    )


async def _ignore_errors(awaitable: Any) -> Any:
    """Index bookkeeping is best-effort: a failed cleanup must not abort a settle."""
    try:
        return await awaitable
    except Exception:
        return None
