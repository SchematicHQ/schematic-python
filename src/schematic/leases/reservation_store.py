"""Reservation table: the contract, plus the per-process in-memory backend.

A reservation is a hold carved out of a lease. ``add`` does not debit: the
debit already landed in ``LeaseStore.try_reserve``, and that ordering is what
bounds a crash to a leaked hold rather than a double-spend.
"""

from __future__ import annotations

import abc
import math
import time
from typing import Dict, List, Optional

from .lease_store import LeaseStore
from .types import Clock, ReservationRecord


class ReservationStore(abc.ABC):
    """Backing store for open reservations, shared by both backends."""

    @abc.abstractmethod
    async def add(self, reservation: ReservationRecord) -> None:
        """Register a reservation. Idempotent on id."""

    @abc.abstractmethod
    async def get(self, reservation_id: str) -> Optional[ReservationRecord]:
        """Look up a reservation, or ``None`` once it has been claimed or swept."""

    @abc.abstractmethod
    async def consume(self, reservation_id: str, credits_consumed: float) -> Optional[float]:
        """Claim a reservation exactly once and refund its unspent slice.

        The claim is atomic and comes first: a racing settle or sweep finds
        nothing to claim, gets ``None``, and refunds nothing. On a successful
        claim, ``credits_consumed`` is clamped to ``[0, credits_reserved]``, the
        remainder is refunded to the lease (pinned to the reservation's lease),
        and the clamped figure is returned. A crash between the claim and the
        refund loses the refund, never double-refunds.
        """

    @abc.abstractmethod
    async def reserved_credits(self, company_id: str, credit_type_id: str) -> float:
        """Sum of ``credits_reserved`` across the slot's open reservations.

        A hold counts exactly while it is in the table, so
        ``local_remaining_credits + reserved_credits`` stays exact between
        operations.
        """

    @abc.abstractmethod
    async def sweep_expired(self, now: Optional[float] = None) -> int:
        """Remove every reservation past its TTL, refunding each full hold.

        Refunds are pinned to the originating lease, so a hold carved from a
        lease that has since expired is dropped rather than credited to its
        successor. Returns the number swept.
        """

    @abc.abstractmethod
    async def count(self) -> int:
        """Open reservations across every slot."""


class InMemoryReservationStore(ReservationStore):
    """Per-process reservation table refunding into a per-process lease store."""

    def __init__(self, lease_store: LeaseStore, *, clock: Clock = time.time) -> None:
        self._lease_store = lease_store
        self._clock = clock
        self._reservations: Dict[str, ReservationRecord] = {}

    async def add(self, reservation: ReservationRecord) -> None:
        self._reservations[reservation.id] = reservation

    async def get(self, reservation_id: str) -> Optional[ReservationRecord]:
        return self._reservations.get(reservation_id)

    async def consume(self, reservation_id: str, credits_consumed: float) -> Optional[float]:
        # The claim: a dict pop with no await in it, so of two racing callers
        # exactly one comes away with the record.
        reservation = self._reservations.pop(reservation_id, None)
        if reservation is None:
            return None
        consumed = clamp_consumption(credits_consumed, reservation.credits_reserved)
        refund = reservation.credits_reserved - consumed
        if refund > 0:
            await self._lease_store.refund(
                reservation.company_id,
                reservation.credit_type_id,
                refund,
                reservation.lease_id,
            )
        return consumed

    async def reserved_credits(self, company_id: str, credit_type_id: str) -> float:
        return sum(
            reservation.credits_reserved
            for reservation in self._reservations.values()
            if reservation.company_id == company_id and reservation.credit_type_id == credit_type_id
        )

    async def sweep_expired(self, now: Optional[float] = None) -> int:
        cutoff = self._clock() if now is None else now
        expired: List[str] = [
            reservation_id
            for reservation_id, reservation in self._reservations.items()
            if reservation.expires_at <= cutoff
        ]
        swept = 0
        for reservation_id in expired:
            # Route through consume so the sweep claims exactly once too.
            if await self.consume(reservation_id, 0) is not None:
                swept += 1
        return swept

    async def count(self) -> int:
        return len(self._reservations)


def clamp_consumption(credits_consumed: float, credits_reserved: float) -> float:
    """Local bookkeeping never debits a lease past the hold it took."""
    if math.isnan(credits_consumed) or credits_consumed < 0:
        return 0.0
    return min(credits_consumed, credits_reserved)
