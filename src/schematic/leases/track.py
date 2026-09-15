"""Settling a reservation: consume the hold, then build the billing event.

The event is built from the caller-held handle rather than the store, so the
usage is still billed when the hold has already been swept. The server is the
source of truth for real consumption; the local bookkeeping only keeps the
lease's view honest.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from ..types import EventBodyTrack
from .reservation_store import ReservationStore

if TYPE_CHECKING:
    from ..client import Reservation, TrackWithReservationOptions


@dataclass
class ReservationConsumeResult:
    """What a settle did locally, and what it owes the server."""

    track: EventBodyTrack
    # True when the hold was still open and this call debited the consumed
    # slice and refunded the rest. False when it had already been swept at its
    # TTL, already settled, or the store was unreachable: the lease balance was
    # not touched here, so it reads high until the lease rolls over, and the
    # track event is a recovery emit.
    settled_locally: bool


async def consume_reservation_and_build_event(
    reservations: ReservationStore,
    reservation: "Reservation",
    actual_quantity: float,
    options: Optional["TrackWithReservationOptions"] = None,
) -> ReservationConsumeResult:
    """Settle a hold against its lease and build the track event that bills it."""
    credits = actual_quantity * reservation.consumption_rate
    consumed = await reservations.consume(reservation.id, credits)
    return ReservationConsumeResult(
        track=build_reservation_track_event(reservation, settled_quantity(actual_quantity), options),
        settled_locally=consumed is not None,
    )


def build_reservation_track_event(
    reservation: "Reservation",
    actual_quantity: int,
    options: Optional["TrackWithReservationOptions"] = None,
) -> EventBodyTrack:
    """Build the track event that settles a reservation, from the handle alone.

    Kept free of store access so the client can still bill the usage when the
    local settle fails against an unreachable store.
    """
    return EventBodyTrack(
        company=reservation.company,
        event=reservation.event_subtype,
        # A client-mode hold routes the server-side consumption through the
        # lease's sub-ledger, instead of decrementing a grant the acquire
        # already pre-debited. In server mode the hold lives on the server and
        # settles by id; never send both, since the server prefers the lease id
        # and there is no lease behind it.
        lease_id=None if reservation.mode == "server" else reservation.lease_id,
        quantity=actual_quantity,
        reservation_id=reservation.id if reservation.mode == "server" else None,
        traits=options.traits if options is not None else None,
        user=reservation.user,
    )


def settled_quantity(actual_quantity: float) -> int:
    """Cast a settled usage onto the integer a track event records.

    The hold can be sized from a fractional usage but the event's quantity is
    an integer, so a partial unit settles as a whole one rather than as none.
    """
    return int(actual_quantity) if float(actual_quantity).is_integer() else math.ceil(actual_quantity)
