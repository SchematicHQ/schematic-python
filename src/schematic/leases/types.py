"""Shared types, defaults, and config resolution for client-mode credit leases.

Durations are seconds (floats), like every other duration on this SDK, and
instants are epoch seconds (floats) rather than ``datetime`` objects: the
stores compare them against a clock the conformance runner can drive, and
Redis stores them as numbers anyway. The wire adapter converts at the
boundary.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, Mapping, Optional

# Reads the current time as epoch seconds. Injected into every store and the
# lease manager so tests and the conformance runner can drive a virtual clock.
Clock = Callable[[], float]

# Lease lifetime requested at acquire and extend (expires_at = now + duration).
DEFAULT_LEASE_DURATION = 300.0
# Reservation lifetime, and the sweep deadline. Size it above the longest
# expected gap between check() and track_with_reservation(): a settle arriving
# after the TTL still bills the server but no longer re-debits the lease.
DEFAULT_RESERVATION_TTL = 60.0
# Credits requested per acquire, and the minimum extend tranche.
DEFAULT_LEASE_SIZE = 10_000.0
# Remaining/granted ratio at or below which a background extend is kicked off.
DEFAULT_LOW_WATER_MARK = 0.25
# Expired-reservation sweep cadence.
DEFAULT_SWEEP_INTERVAL = 1.0
# How long a prewarm waits for a freshly identified company to surface in the
# datastream cache before giving up.
DEFAULT_PREWARM_RESOLVE_TIMEOUT = 5.0
# The server refuses to hold credits for longer than an hour, so a larger
# configured TTL would have the local sweeper trail the server's own release.
MAX_RESERVATION_TTL = 3600.0


@dataclass
class LeaseState:
    """The local view of the one lease a ``(company, credit type)`` slot holds."""

    lease_id: str
    company_id: str
    credit_type_id: str
    # Server-authoritative total granted to this lease. Grows on extend.
    granted_amount: float
    # Granted minus outstanding holds and consumption. Starts at the full
    # grant when the lease is installed.
    local_remaining_credits: float
    # Epoch seconds. Past it the lease is dead: the server has refunded the
    # remainder to the company balance, so the local balance is stale.
    expires_at: float


@dataclass
class ReservationRecord:
    """One credit hold carved out of a lease by a check."""

    id: str
    # The lease the hold was carved from. Pins refunds so a hold from an
    # expired lease can never inflate its successor.
    lease_id: str
    company_id: str
    credit_type_id: str
    # Event subtype the settling track event is billed as.
    event_subtype: str
    # Caller-declared usage, in event units.
    quantity_reserved: float
    # quantity_reserved * consumption_rate.
    credits_reserved: float
    consumption_rate: float
    # Epoch seconds. The sweeper refunds the full hold past this instant.
    expires_at: float
    # Evaluation context the hold was issued for, threaded onto the track
    # event so the server attributes usage to the same company and user.
    company: Optional[Dict[str, str]] = None
    user: Optional[Dict[str, str]] = None


@dataclass(frozen=True)
class ResolvedLeaseConfig:
    """Config for a single credit type, after overrides and defaults."""

    lease_duration: float = DEFAULT_LEASE_DURATION
    reservation_ttl: float = DEFAULT_RESERVATION_TTL
    lease_size: float = DEFAULT_LEASE_SIZE
    low_water_mark: float = DEFAULT_LOW_WATER_MARK


@dataclass
class LeaseConfigOverride:
    """Per-credit-type overrides of the four resolvable knobs."""

    lease_duration: Optional[float] = None
    reservation_ttl: Optional[float] = None
    lease_size: Optional[float] = None
    low_water_mark: Optional[float] = None


@dataclass
class LeaseConfig:
    """Client-wide lease knobs, in seconds, plus per-credit-type overrides.

    The user-facing configuration dataclass lives on the client; this is the
    plain-keyword form the lease machinery resolves against.
    """

    lease_duration: Optional[float] = None
    reservation_ttl: Optional[float] = None
    lease_size: Optional[float] = None
    low_water_mark: Optional[float] = None
    sweep_interval: Optional[float] = None
    overrides: Mapping[str, LeaseConfigOverride] = field(default_factory=dict)


def resolve_lease_config(
    config: Optional[LeaseConfig] = None,
    overrides: Optional[Mapping[str, LeaseConfigOverride]] = None,
    credit_type_id: Optional[str] = None,
) -> ResolvedLeaseConfig:
    """Resolve the knobs for one credit type: override, then client config, then default.

    ``overrides`` wins over ``config.overrides`` so a caller can resolve against
    a one-off override map without rebuilding the config.
    """
    override: Optional[LeaseConfigOverride] = None
    if credit_type_id is not None:
        table = overrides if overrides is not None else (config.overrides if config else None)
        if table:
            override = table.get(credit_type_id)

    def pick(name: str, default: float) -> float:
        if override is not None:
            value = getattr(override, name)
            if value is not None:
                return float(value)
        if config is not None:
            value = getattr(config, name)
            if value is not None:
                return float(value)
        return default

    return ResolvedLeaseConfig(
        lease_duration=pick("lease_duration", DEFAULT_LEASE_DURATION),
        # Clamped rather than rejected: a TTL past the server's cap would have
        # the sweeper refund a hold the server already released.
        reservation_ttl=min(pick("reservation_ttl", DEFAULT_RESERVATION_TTL), MAX_RESERVATION_TTL),
        lease_size=pick("lease_size", DEFAULT_LEASE_SIZE),
        low_water_mark=pick("low_water_mark", DEFAULT_LOW_WATER_MARK),
    )
