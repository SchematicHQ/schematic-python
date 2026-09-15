"""Lease slot storage: the contract, plus the per-process in-memory backend.

At most one lease occupies a ``(company_id, credit_type_id)`` slot. Every
mutation is atomic per slot; ``RedisLeaseStore`` gets that from single-key Lua,
this one from a per-slot ``asyncio.Lock``.
"""

from __future__ import annotations

import abc
import asyncio
import math
import time
from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict, List, Optional, Tuple

from .types import Clock, LeaseState


def lease_key(company_id: str, credit_type_id: str) -> str:
    return f"{company_id}:{credit_type_id}"


class LeaseStore(abc.ABC):
    """Backing store for lease slots, shared by the in-memory and Redis backends."""

    @abc.abstractmethod
    async def get(self, company_id: str, credit_type_id: str) -> Optional[LeaseState]:
        """Snapshot of the slot, expired or not. Callers re-guard on expiry."""

    @abc.abstractmethod
    async def replace(
        self,
        *,
        lease_id: str,
        company_id: str,
        credit_type_id: str,
        granted_amount: float,
        expires_at: float,
    ) -> bool:
        """Install a fresh lease at its full grant, if the slot is free to take.

        A *live* lease holds the slot even when it carries a different id (a
        sibling pod won the acquire race): its already-debited balance wins and
        this reports ``False``. An *expired* row carrying the SAME id is not
        rewritten either, since that would reset the balance and erase debits
        whose reservations are still open; it is reconciled like an extend
        (granted to the incoming total, expiry forward only, balance untouched)
        and also reports ``False``. Returns ``True`` only when a fresh row was
        written, which is what tells the manager whether the lease it just
        acquired is redundant.
        """

    @abc.abstractmethod
    async def try_reserve(self, company_id: str, credit_type_id: str, credits: float) -> Optional[float]:
        """Atomically check and debit, returning the post-debit balance.

        ``None`` when there is no lease, it has expired, the balance is short,
        or ``credits`` is not a finite non-negative number. Returning the
        balance (rather than a bool) lets the caller derive the pre-debit
        figure as ``returned + credits`` without a racy follow-up read.
        """

    @abc.abstractmethod
    async def refund(
        self,
        company_id: str,
        credit_type_id: str,
        credits: float,
        pin_lease_id: Optional[str] = None,
    ) -> None:
        """Return credits to the slot's balance, clamped at the granted amount.

        With ``pin_lease_id``, the refund applies only while the slot still
        holds that lease: a hold carved out of an expired lease must never
        inflate its successor, whose grant the server already issued whole.
        """

    @abc.abstractmethod
    async def extend(
        self,
        company_id: str,
        credit_type_id: str,
        granted_total: float,
        new_expires_at: Optional[float] = None,
        pin_lease_id: Optional[str] = None,
    ) -> None:
        """Reconcile the slot to the server-authoritative total.

        The delta is computed inside the store against the currently stored
        total, never from a caller-held pre-wire-call read: two pods extending
        concurrently from the same stale read would each apply a delta and mint
        phantom credits. A total a sibling already applied is a no-op, so
        applies converge in any order. Expiry only ever moves forward.
        """

    @abc.abstractmethod
    async def drop(self, company_id: str, credit_type_id: str) -> None:
        """Remove the slot entry, after a remote release."""

    def list_leases(self) -> Optional[List[LeaseState]]:
        """Every lease this store holds, or ``None`` when it cannot enumerate.

        Only a per-process store answers: its leases are exclusively this
        process's, so releasing them on close is safe. A shared backend must
        never enumerate and release, since sibling pods still draw on those
        leases.
        """
        return None


class _SlotLocks:
    """Per-slot mutual exclusion, refcounted so idle slots do not accumulate."""

    def __init__(self) -> None:
        self._locks: Dict[str, Tuple[asyncio.Lock, int]] = {}

    @asynccontextmanager
    async def hold(self, key: str) -> AsyncIterator[None]:
        lock, waiters = self._locks.get(key, (asyncio.Lock(), 0))
        self._locks[key] = (lock, waiters + 1)
        try:
            async with lock:
                yield
        finally:
            held, count = self._locks[key]
            if count <= 1:
                del self._locks[key]
            else:
                self._locks[key] = (held, count - 1)


class InMemoryLeaseStore(LeaseStore):
    """Per-process lease slots. Single-pod gating only.

    Swap in ``RedisLeaseStore`` to gate across pods; both implement the same
    contract.
    """

    def __init__(self, *, clock: Clock = time.time) -> None:
        self._clock = clock
        self._leases: Dict[str, LeaseState] = {}
        self._locks = _SlotLocks()

    async def get(self, company_id: str, credit_type_id: str) -> Optional[LeaseState]:
        entry = self._leases.get(lease_key(company_id, credit_type_id))
        return _copy(entry) if entry else None

    async def replace(
        self,
        *,
        lease_id: str,
        company_id: str,
        credit_type_id: str,
        granted_amount: float,
        expires_at: float,
    ) -> bool:
        key = lease_key(company_id, credit_type_id)
        async with self._locks.hold(key):
            existing = self._leases.get(key)
            if existing is not None and existing.expires_at > self._clock():
                return False
            if existing is not None and existing.lease_id == lease_id:
                # The same lease coming back over its own expired row: a stale
                # acquire response for a lease the idempotent server also
                # handed a racing sibling, which may since have extended it.
                add = granted_amount - existing.granted_amount
                if add > 0:
                    existing.granted_amount = granted_amount
                    existing.local_remaining_credits += add
                if expires_at > existing.expires_at:
                    existing.expires_at = expires_at
                return False
            self._leases[key] = LeaseState(
                lease_id=lease_id,
                company_id=company_id,
                credit_type_id=credit_type_id,
                granted_amount=granted_amount,
                local_remaining_credits=granted_amount,
                expires_at=expires_at,
            )
            return True

    async def try_reserve(self, company_id: str, credit_type_id: str, credits: float) -> Optional[float]:
        # NaN passes every comparison below, and a NaN balance would approve
        # every later reserve, so it never reaches the arithmetic.
        if not is_finite_non_negative(credits):
            return None
        key = lease_key(company_id, credit_type_id)
        async with self._locks.hold(key):
            entry = self._leases.get(key)
            if entry is None:
                return None
            if entry.expires_at <= self._clock():
                return None
            if entry.local_remaining_credits < credits:
                return None
            entry.local_remaining_credits -= credits
            return entry.local_remaining_credits

    async def refund(
        self,
        company_id: str,
        credit_type_id: str,
        credits: float,
        pin_lease_id: Optional[str] = None,
    ) -> None:
        if not is_finite_non_negative(credits) or credits <= 0:
            return
        key = lease_key(company_id, credit_type_id)
        async with self._locks.hold(key):
            entry = self._leases.get(key)
            if entry is None:
                return
            if pin_lease_id is not None and entry.lease_id != pin_lease_id:
                return
            entry.local_remaining_credits = min(
                entry.local_remaining_credits + credits,
                entry.granted_amount,
            )

    async def extend(
        self,
        company_id: str,
        credit_type_id: str,
        granted_total: float,
        new_expires_at: Optional[float] = None,
        pin_lease_id: Optional[str] = None,
    ) -> None:
        key = lease_key(company_id, credit_type_id)
        async with self._locks.hold(key):
            entry = self._leases.get(key)
            if entry is None:
                return
            if pin_lease_id is not None and entry.lease_id != pin_lease_id:
                return
            add = granted_total - entry.granted_amount
            if add > 0:
                entry.granted_amount = granted_total
                entry.local_remaining_credits += add
            if new_expires_at is not None and new_expires_at > entry.expires_at:
                entry.expires_at = new_expires_at

    async def drop(self, company_id: str, credit_type_id: str) -> None:
        key = lease_key(company_id, credit_type_id)
        async with self._locks.hold(key):
            self._leases.pop(key, None)

    def list_leases(self) -> Optional[List[LeaseState]]:
        return [_copy(entry) for entry in self._leases.values()]


def _copy(entry: LeaseState) -> LeaseState:
    return LeaseState(
        lease_id=entry.lease_id,
        company_id=entry.company_id,
        credit_type_id=entry.credit_type_id,
        granted_amount=entry.granted_amount,
        local_remaining_credits=entry.local_remaining_credits,
        expires_at=entry.expires_at,
    )


def is_finite_non_negative(value: float) -> bool:
    """A credit amount fit for arithmetic: finite, and not negative."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(number) and number >= 0
