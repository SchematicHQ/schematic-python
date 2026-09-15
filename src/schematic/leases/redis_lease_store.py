"""Redis-backed lease slots: one hash per slot, mutated by single-key Lua.

The key layout, hash field names (camelCase), millisecond instants, Lua
scripts, and TTL grace windows match the Node SDK exactly, so Node and Python
pods can share one Redis and agree on every slot.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from .lease_store import LeaseStore, is_finite_non_negative, lease_key
from .types import DEFAULT_LEASE_DURATION, Clock, LeaseState

DEFAULT_KEY_PREFIX = "schematic:"
LEASE_KEY_NAMESPACE = "credit-lease:"
# How long after the declared expiry the row survives before Redis evicts it.
# Gives the sweeper a window to refund expired reservations before the lease
# state underneath them disappears.
LEASE_TTL_GRACE_MS = 60_000

# Every Lua script below touches exactly ONE key (the lease hash), keeping
# them safe under Redis Cluster (multi-key scripts spanning slots raise
# CROSSSLOT). Only the lease hash needs atomic mutation; cross-key
# bookkeeping uses ordinary single-key commands.
#
# Expiry is decided against the *Redis server's* clock (`redis.call('TIME')`),
# not the calling pod's: with many pods sharing one lease, local clock skew
# would let pods disagree on whether the lease is live. The `LEASE_NOW_MS`
# snippet converts TIME to integer milliseconds (matching the stored
# `expiresAt`); `redis.replicate_commands()` first, so the non-deterministic
# TIME read is allowed alongside writes on Redis 5/6.
LEASE_NOW_MS = """
redis.replicate_commands()
local t = redis.call('TIME')
local now = (tonumber(t[1]) * 1000) + math.floor(tonumber(t[2]) / 1000)
"""

# Atomic `replace`. Writes the lease hash only when the slot is empty or the
# existing lease has expired. Returns 1 on write, 0 if a *live* lease already
# occupies the slot, even one with a different leaseId, e.g. installed by a
# sibling instance that raced this acquire. An expired row with the SAME
# leaseId is reconciled like an extend instead of rewritten, which would reset
# the balance and erase debits whose reservations are still open.
REPLACE_SCRIPT = (
    LEASE_NOW_MS
    + """
local existing_id = redis.call('HGET', KEYS[1], 'leaseId')
local existing_expiry = tonumber(redis.call('HGET', KEYS[1], 'expiresAt') or '0')
local new_id = ARGV[1]
local new_granted = ARGV[2]
local new_expiry = tonumber(ARGV[3])
local grace = tonumber(ARGV[4])

if existing_id and existing_expiry > now then
    return 0
end

if existing_id == new_id then
    local granted = tonumber(redis.call('HGET', KEYS[1], 'grantedAmount') or '0')
    local add = tonumber(new_granted) - granted
    if add > 0 then
        local remaining = tonumber(redis.call('HGET', KEYS[1], 'localRemainingCredits') or '0')
        redis.call('HSET', KEYS[1],
            'grantedAmount', new_granted,
            'localRemainingCredits', tostring(remaining + add))
    end
    if new_expiry > existing_expiry then
        redis.call('HSET', KEYS[1], 'expiresAt', ARGV[3])
        redis.call('PEXPIREAT', KEYS[1], new_expiry + grace)
    end
    return 0
end

redis.call('DEL', KEYS[1])
redis.call('HSET', KEYS[1],
    'leaseId', new_id,
    'companyId', ARGV[5],
    'creditTypeId', ARGV[6],
    'grantedAmount', new_granted,
    'localRemainingCredits', new_granted,
    'expiresAt', ARGV[3])
redis.call('PEXPIREAT', KEYS[1], new_expiry + grace)
return 1
"""
)

# Atomic check-and-decrement on `localRemainingCredits`. Returns the post-debit
# balance as a string (a Lua number reply truncates to integer, which would
# corrupt fractional credit costs); nil if there is no lease, the lease has
# expired, or there is insufficient remaining. The expiry guard compares
# against the Redis server clock, so a reserve against an expired-but-not-yet-
# evicted row during the TTL grace window is rejected.
TRY_RESERVE_SCRIPT = (
    LEASE_NOW_MS
    + """
local raw = redis.call('HGET', KEYS[1], 'localRemainingCredits')
if not raw then return false end
local expiry = tonumber(redis.call('HGET', KEYS[1], 'expiresAt') or '0')
if expiry <= now then return false end
local remaining = tonumber(raw)
local requested = tonumber(ARGV[1])
if remaining < requested then return false end
local new_remaining = remaining - requested
redis.call('HSET', KEYS[1], 'localRemainingCredits', tostring(new_remaining))
return tostring(new_remaining)
"""
)

# Refund credits, clamped at `grantedAmount`. ARGV[2], when non-empty, pins the
# refund to a specific leaseId: if the slot now holds a different lease, the
# refund is dropped: the expired lease's unspent remainder was already
# returned to the company balance server-side, so crediting the successor would
# mint phantom credits.
REFUND_SCRIPT = """
local raw_remaining = redis.call('HGET', KEYS[1], 'localRemainingCredits')
if not raw_remaining then return 0 end
local required_lease = ARGV[2]
if required_lease and required_lease ~= '' then
    local current_lease = redis.call('HGET', KEYS[1], 'leaseId')
    if current_lease ~= required_lease then return 0 end
end
local remaining = tonumber(raw_remaining)
local granted = tonumber(redis.call('HGET', KEYS[1], 'grantedAmount') or '0')
local refund = tonumber(ARGV[1])
local new_balance = remaining + refund
if new_balance > granted then new_balance = granted end
redis.call('HSET', KEYS[1], 'localRemainingCredits', tostring(new_balance))
return 1
"""

# Reconcile the lease to the server-authoritative grantedAmount total
# (ARGV[1]), crediting the difference to localRemainingCredits. The delta is
# computed HERE, atomically against the hash's current total, never by the
# caller from a pre-wire-call read: two pods extending the same shared lease
# concurrently would each apply a delta against the same stale read and mint
# phantom credits. Reconciling to the absolute total converges regardless of
# arrival order. Expiry only ever moves forward. ARGV[4], when non-empty, pins
# the extend to a leaseId, mirroring REFUND_SCRIPT.
EXTEND_SCRIPT = """
local raw_granted = redis.call('HGET', KEYS[1], 'grantedAmount')
if not raw_granted then return 0 end
local required_lease = ARGV[4]
if required_lease and required_lease ~= '' then
    local current_lease = redis.call('HGET', KEYS[1], 'leaseId')
    if current_lease ~= required_lease then return 0 end
end
local granted = tonumber(raw_granted)
local target = tonumber(ARGV[1])
local add = target - granted
if add > 0 then
    local remaining = tonumber(redis.call('HGET', KEYS[1], 'localRemainingCredits') or '0')
    redis.call('HSET', KEYS[1],
        'grantedAmount', tostring(target),
        'localRemainingCredits', tostring(remaining + add))
end
local new_expiry = tonumber(ARGV[2])
local grace = tonumber(ARGV[3])
local current_expiry = tonumber(redis.call('HGET', KEYS[1], 'expiresAt') or '0')
if new_expiry > current_expiry then
    redis.call('HSET', KEYS[1], 'expiresAt', ARGV[2])
    redis.call('PEXPIREAT', KEYS[1], new_expiry + grace)
end
return 1
"""


class LuaScript:
    """One Lua script, run by EVALSHA with a lazy SCRIPT LOAD and an EVAL fallback.

    A Redis that has dropped its script cache (restart, SCRIPT FLUSH) answers
    NOSCRIPT; the fallback re-sends the body and re-loads it on the next call.
    """

    def __init__(self, body: str) -> None:
        self.body = body
        self._sha: Optional[str] = None

    async def run(self, client: Any, keys: List[str], args: List[str]) -> Any:
        if self._sha is None:
            self._sha = to_str(await client.script_load(self.body))
        try:
            return await client.evalsha(self._sha, len(keys), *keys, *args)
        except Exception as err:
            if not _is_noscript(err):
                raise
            self._sha = None
            return await client.eval(self.body, len(keys), *keys, *args)


class RedisLeaseStore(LeaseStore):
    """Lease slots in Redis: one hash per slot, atomic via single-key Lua.

    ``client`` is a connected ``redis.asyncio.Redis``. Balances are stored as
    strings so fractional credit amounts survive the round trip.
    """

    def __init__(
        self,
        client: Any,
        *,
        key_prefix: str = DEFAULT_KEY_PREFIX,
        default_lease_duration: float = DEFAULT_LEASE_DURATION,
        clock: Clock = time.time,
    ) -> None:
        self._client = client
        self._key_prefix = key_prefix
        # Only reached when a direct caller extends without an expiry; the
        # lease manager always passes one.
        self._default_lease_duration = default_lease_duration
        self._clock = clock
        self._replace = LuaScript(REPLACE_SCRIPT)
        self._try_reserve = LuaScript(TRY_RESERVE_SCRIPT)
        self._refund = LuaScript(REFUND_SCRIPT)
        self._extend = LuaScript(EXTEND_SCRIPT)

    def hash_key(self, company_id: str, credit_type_id: str) -> str:
        """Public so the reservation store can target the same lease hash."""
        return f"{self._key_prefix}{LEASE_KEY_NAMESPACE}{lease_key(company_id, credit_type_id)}"

    async def get(self, company_id: str, credit_type_id: str) -> Optional[LeaseState]:
        raw = decode_hash(await self._client.hgetall(self.hash_key(company_id, credit_type_id)))
        if not raw.get("leaseId"):
            return None
        return LeaseState(
            lease_id=raw["leaseId"],
            company_id=raw.get("companyId", company_id),
            credit_type_id=raw.get("creditTypeId", credit_type_id),
            granted_amount=float(raw.get("grantedAmount", "0")),
            local_remaining_credits=float(raw.get("localRemainingCredits", "0")),
            expires_at=float(raw.get("expiresAt", "0")) / 1000.0,
        )

    async def replace(
        self,
        *,
        lease_id: str,
        company_id: str,
        credit_type_id: str,
        granted_amount: float,
        expires_at: float,
    ) -> bool:
        result = await self._replace.run(
            self._client,
            [self.hash_key(company_id, credit_type_id)],
            # No client clock here: the script reads `now` from the Redis
            # server via TIME, so every pod agrees on expiry.
            [
                lease_id,
                format_amount(granted_amount),
                to_epoch_ms(expires_at),
                str(LEASE_TTL_GRACE_MS),
                company_id,
                credit_type_id,
            ],
        )
        return _to_number(result) == 1

    async def try_reserve(self, company_id: str, credit_type_id: str, credits: float) -> Optional[float]:
        # Reject non-finite/negative debits before they reach the script: the
        # string form of NaN parses back to a Lua nan, slips through the `<`
        # comparison, and would poison the SHARED balance for every pod.
        if not is_finite_non_negative(credits):
            return None
        result = await self._try_reserve.run(
            self._client,
            [self.hash_key(company_id, credit_type_id)],
            [format_amount(credits)],
        )
        if result is None or result is False:
            return None
        return float(to_str(result))

    async def refund(
        self,
        company_id: str,
        credit_type_id: str,
        credits: float,
        pin_lease_id: Optional[str] = None,
    ) -> None:
        if not is_finite_non_negative(credits) or credits <= 0:
            return
        await self._refund.run(
            self._client,
            [self.hash_key(company_id, credit_type_id)],
            # An empty string disables the lease pin (Lua has no nil ARGV).
            [format_amount(credits), pin_lease_id or ""],
        )

    async def extend(
        self,
        company_id: str,
        credit_type_id: str,
        granted_total: float,
        new_expires_at: Optional[float] = None,
        pin_lease_id: Optional[str] = None,
    ) -> None:
        expiry = new_expires_at if new_expires_at is not None else self._clock() + self._default_lease_duration
        await self._extend.run(
            self._client,
            [self.hash_key(company_id, credit_type_id)],
            # granted_total is the server-authoritative TOTAL; the script
            # computes the delta against the stored total.
            [format_amount(granted_total), to_epoch_ms(expiry), str(LEASE_TTL_GRACE_MS), pin_lease_id or ""],
        )

    async def drop(self, company_id: str, credit_type_id: str) -> None:
        # A plain single-key delete: no secondary index to keep in sync.
        await self._client.delete(self.hash_key(company_id, credit_type_id))


def _is_noscript(err: Exception) -> bool:
    """Did Redis answer that it no longer holds this script?

    Matched by exception name as well as message so the check does not depend
    on importing redis, nor on a client's exact wording.
    """
    return type(err).__name__ == "NoScriptError" or "NOSCRIPT" in str(err).upper()


def to_str(value: Any) -> str:
    return value.decode("utf-8") if isinstance(value, bytes) else str(value)


def decode_hash(raw: Any) -> Dict[str, str]:
    if not raw:
        return {}
    return {to_str(key): to_str(value) for key, value in raw.items()}


def _to_number(value: Any) -> float:
    if value is None or value is False:
        return 0.0
    if value is True:
        return 1.0
    return float(to_str(value))


def to_epoch_ms(epoch_seconds: float) -> str:
    """Instants cross the wire as integer milliseconds, as the Node SDK writes them."""
    return str(int(round(epoch_seconds * 1000)))


def format_amount(value: float) -> str:
    """Format a credit amount the way JavaScript would, so shared rows read alike."""
    if float(value).is_integer():
        return str(int(value))
    return repr(float(value))
