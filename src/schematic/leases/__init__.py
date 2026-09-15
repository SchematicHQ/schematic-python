"""Client-mode credit leases: local lease slots, reservations, and their manager.

Async only. Client-mode leases ride on DataStream, which this SDK offers on
``AsyncSchematic`` alone, so there is no synchronous variant.

The in-memory stores gate within one process; the Redis stores gate across
pods and share their key layout with the Node SDK, so mixed fleets agree on
every lease.
"""

from .lease_manager import CreditsWireClient, LeaseGrant, LeaseManager, LeaseWireClient
from .lease_store import InMemoryLeaseStore, LeaseStore, lease_key
from .redis_lease_store import RedisLeaseStore
from .redis_reservation_store import RedisReservationStore
from .reservation_store import InMemoryReservationStore, ReservationStore
from .types import (
    DEFAULT_LEASE_DURATION,
    DEFAULT_LEASE_SIZE,
    DEFAULT_LOW_WATER_MARK,
    DEFAULT_PREWARM_RESOLVE_TIMEOUT,
    DEFAULT_RESERVATION_TTL,
    DEFAULT_SWEEP_INTERVAL,
    MAX_RESERVATION_TTL,
    Clock,
    LeaseConfig,
    LeaseConfigOverride,
    LeaseState,
    ReservationRecord,
    ResolvedLeaseConfig,
    resolve_lease_config,
)

__all__ = [
    "Clock",
    "CreditsWireClient",
    "DEFAULT_LEASE_DURATION",
    "DEFAULT_LEASE_SIZE",
    "DEFAULT_LOW_WATER_MARK",
    "DEFAULT_PREWARM_RESOLVE_TIMEOUT",
    "DEFAULT_RESERVATION_TTL",
    "DEFAULT_SWEEP_INTERVAL",
    "InMemoryLeaseStore",
    "InMemoryReservationStore",
    "LeaseConfig",
    "LeaseConfigOverride",
    "LeaseGrant",
    "LeaseManager",
    "LeaseState",
    "LeaseStore",
    "LeaseWireClient",
    "MAX_RESERVATION_TTL",
    "RedisLeaseStore",
    "RedisReservationStore",
    "ReservationRecord",
    "ReservationStore",
    "ResolvedLeaseConfig",
    "lease_key",
    "resolve_lease_config",
]
