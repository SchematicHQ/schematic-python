"""Lease lifecycle against the server: acquire, extend, release, sweep.

Every path here resolves rather than raises. The manager's callers route a
missing lease through their fail-open/fail-closed handling, and several calls
are made fire-and-forget, where a raised exception would surface as an
unretrieved task exception instead.
"""

from __future__ import annotations

import asyncio
import datetime as dt
import logging
import time
from dataclasses import dataclass
from typing import Any, Awaitable, Dict, Optional, Protocol, Set

from .lease_store import LeaseStore, lease_key
from .reservation_store import ReservationStore
from .types import (
    DEFAULT_SWEEP_INTERVAL,
    Clock,
    LeaseConfig,
    LeaseState,
    ResolvedLeaseConfig,
    resolve_lease_config,
)

logger = logging.getLogger(__name__)


@dataclass
class LeaseGrant:
    """What the server says a lease is, after an acquire or an extend."""

    lease_id: str
    company_id: str
    credit_type_id: str
    # The server-authoritative TOTAL, not the increment an extend asked for.
    granted_amount: float
    expires_at: float


class LeaseWireClient(Protocol):
    """The three lease calls the manager makes.

    Narrow on purpose: it keeps the manager independent of the generated
    client's request and response models, and lets tests script the server.
    """

    async def acquire(
        self,
        company_id: str,
        credit_type_id: str,
        requested_amount: float,
        expires_at: float,
    ) -> LeaseGrant: ...

    async def extend(self, lease_id: str, additional_amount: float, expires_at: float) -> LeaseGrant: ...

    async def release(self, lease_id: str) -> None: ...


class CreditsWireClient:
    """Adapter over the generated async credits client (``AsyncCreditsClient``)."""

    def __init__(self, credits_client: Any, *, request_options: Optional[Any] = None) -> None:
        self._credits = credits_client
        self._request_options = request_options

    async def acquire(
        self,
        company_id: str,
        credit_type_id: str,
        requested_amount: float,
        expires_at: float,
    ) -> LeaseGrant:
        response = await self._credits.acquire_credit_lease(
            company_id=company_id,
            credit_type_id=credit_type_id,
            requested_amount=requested_amount,
            expires_at=_to_datetime(expires_at),
            request_options=self._request_options,
        )
        return _grant_from_response(response)

    async def extend(self, lease_id: str, additional_amount: float, expires_at: float) -> LeaseGrant:
        response = await self._credits.extend_credit_lease(
            lease_id,
            additional_amount=additional_amount,
            expires_at=_to_datetime(expires_at),
            request_options=self._request_options,
        )
        return _grant_from_response(response)

    async def release(self, lease_id: str) -> None:
        await self._credits.release_credit_lease(lease_id, request_options=self._request_options)


class LeaseManager:
    """Owns lease rows for one client: acquire on first use or after expiry,
    extend when the local view dips below the water mark, release on close.

    Acquire and extend each get their own best-effort single-flight map keyed
    by slot. Best-effort because callers racing ahead of the registration can
    still issue duplicate wire calls, which is safe: the server is idempotent
    for an active slot, ``replace`` keeps the first live lease, and ``extend``
    reconciles to a total.
    """

    def __init__(
        self,
        wire_client: LeaseWireClient,
        lease_store: LeaseStore,
        *,
        reservation_store: Optional[ReservationStore] = None,
        config: Optional[LeaseConfig] = None,
        clock: Clock = time.time,
    ) -> None:
        self._wire = wire_client
        self._lease_store = lease_store
        self._reservation_store = reservation_store
        self._config = config or LeaseConfig()
        self._clock = clock
        # Kept separate so an in-flight extend can never satisfy an acquire,
        # or the other way round.
        self._inflight_acquire: Dict[str, "asyncio.Future[Optional[LeaseState]]"] = {}
        self._inflight_extend: Dict[str, "asyncio.Future[Optional[LeaseState]]"] = {}
        self._background: Set["asyncio.Task[None]"] = set()
        self._sweep_task: Optional["asyncio.Task[None]"] = None
        self._stopped = False

    def resolve_config(self, credit_type_id: str) -> ResolvedLeaseConfig:
        return resolve_lease_config(self._config, None, credit_type_id)

    @property
    def sweep_interval(self) -> float:
        return self._config.sweep_interval or DEFAULT_SWEEP_INTERVAL

    async def acquire_if_needed(self, company_id: str, credit_type_id: str) -> Optional[LeaseState]:
        """The slot's live lease, acquiring one over the wire if none is live."""
        try:
            existing = await self._lease_store.get(company_id, credit_type_id)
        except Exception as err:
            logger.error("Failed to read lease store for %s/%s: %s", company_id, credit_type_id, err)
            return None
        if existing is not None and existing.expires_at > self._clock():
            return existing
        # An expired (or absent) slot is left for `replace` to overwrite: it
        # guards on expiry and writes atomically. Dropping the stale row first
        # would be a separate, non-atomic op that can interleave between a
        # sibling pod's read and its replace, clobbering a lease that pod just
        # installed. Reading a stale entry in the gap is harmless, since every
        # path that acts on a lease re-guards on expiry.

        key = lease_key(company_id, credit_type_id)
        inflight = self._inflight_acquire.get(key)
        if inflight is not None:
            return await asyncio.shield(inflight)
        return await self._single_flight(
            self._inflight_acquire, key, self._acquire(company_id, credit_type_id)
        )

    async def _acquire(self, company_id: str, credit_type_id: str) -> Optional[LeaseState]:
        resolved = self.resolve_config(credit_type_id)
        try:
            grant = await self._wire.acquire(
                company_id,
                credit_type_id,
                resolved.lease_size,
                self._clock() + resolved.lease_duration,
            )
            wrote = await self._lease_store.replace(
                lease_id=grant.lease_id,
                company_id=grant.company_id or company_id,
                credit_type_id=grant.credit_type_id or credit_type_id,
                granted_amount=grant.granted_amount,
                expires_at=grant.expires_at,
            )
            if wrote:
                return await self._lease_store.get(company_id, credit_type_id)

            # A sibling holds the slot with a live lease, or the slot's expired
            # row was reconciled in place. The server is idempotent for an
            # active slot, so a racing acquire is normally handed back the SAME
            # lease the sibling installed, and releasing it would pull the
            # shared lease out from under every pod. Only a *different* lease
            # is a redundant hold nobody will draw on, so only that one is
            # released. An empty slot (expired in the gap) releases nothing
            # either: this lease is likely what the next acquire is handed.
            current = await self._lease_store.get(company_id, credit_type_id)
            if current is not None and current.lease_id != grant.lease_id:
                logger.debug(
                    "Lost acquire race for %s/%s; releasing redundant lease %s",
                    company_id,
                    credit_type_id,
                    grant.lease_id,
                )
                self._spawn(self._release(grant.lease_id))
            return current
        except Exception as err:
            logger.error("Failed to acquire credit lease for %s/%s: %s", company_id, credit_type_id, err)
            return None

    async def maybe_extend(
        self,
        company_id: str,
        credit_type_id: str,
        required_credits: Optional[float] = None,
    ) -> Optional[LeaseState]:
        """Extend the slot's lease when the local view warrants it.

        Triggered by either the low-water-mark ratio (steady-state refresh) or
        a ``required_credits`` hint above the local remaining (a check just
        failed a reserve of that size).
        """
        try:
            entry = await self._lease_store.get(company_id, credit_type_id)
        except Exception as err:
            logger.warning("Failed to read lease store for %s/%s: %s", company_id, credit_type_id, err)
            return None
        if entry is None:
            return None
        # Never extend an expired lease: the server treats it as released and
        # has already refunded its remainder, so the only correct move is a
        # fresh acquire on the next check.
        if entry.expires_at <= self._clock():
            return None
        resolved = self.resolve_config(credit_type_id)
        ratio = entry.local_remaining_credits / max(entry.granted_amount, 1)
        below_watermark = ratio <= resolved.low_water_mark
        below_required = required_credits is not None and entry.local_remaining_credits < required_credits
        if not below_watermark and not below_required:
            return entry

        key = lease_key(company_id, credit_type_id)
        inflight = self._inflight_extend.get(key)
        if inflight is not None:
            return await asyncio.shield(inflight)
        return await self._single_flight(
            self._inflight_extend, key, self._extend(entry, resolved, required_credits)
        )

    async def _extend(
        self,
        entry: LeaseState,
        resolved: ResolvedLeaseConfig,
        required_credits: Optional[float],
    ) -> Optional[LeaseState]:
        # Size the extend to cover the request that triggered it: a single
        # check needing more than remaining plus one tranche would otherwise
        # fail its post-extend retry forever, however much balance the server
        # has. The steady-state path keeps asking for the configured tranche.
        shortfall = (required_credits - entry.local_remaining_credits) if required_credits is not None else 0.0
        try:
            grant = await self._wire.extend(
                entry.lease_id,
                max(resolved.lease_size, shortfall),
                self._clock() + resolved.lease_duration,
            )
            # Reconcile to the server's authoritative TOTAL, with the store
            # computing the delta against its own current total: per-process
            # single-flight does not cover sibling pods. Pinned to the lease
            # the server extended, so an expiry mid-call cannot mint the delta
            # onto a successor.
            await self._lease_store.extend(
                entry.company_id,
                entry.credit_type_id,
                grant.granted_amount,
                grant.expires_at,
                entry.lease_id,
            )
            return await self._lease_store.get(entry.company_id, entry.credit_type_id)
        except Exception as err:
            logger.warning("Failed to extend credit lease %s: %s", entry.lease_id, err)
            return None

    async def release_all_local_leases(self) -> None:
        """Release every live lease this process exclusively holds.

        Only a per-process store answers ``list_leases``; a shared backend
        returns ``None`` and is skipped, since sibling pods still draw on those
        leases. Expired leases are skipped too: the server already swept them.
        Best-effort, with failures falling back to server-side expiry.
        """
        try:
            entries = self._lease_store.list_leases()
        except Exception as err:
            logger.warning("Failed to enumerate leases on close: %s", err)
            return
        if not entries:
            return
        now = self._clock()
        for entry in entries:
            if entry.expires_at <= now:
                continue
            try:
                await self._wire.release(entry.lease_id)
                await self._lease_store.drop(entry.company_id, entry.credit_type_id)
                logger.debug("Released credit lease %s on close", entry.lease_id)
            except Exception as err:
                logger.warning(
                    "Failed to release credit lease %s on close (it will expire server-side): %s",
                    entry.lease_id,
                    err,
                )

    def start_sweep(self) -> None:
        """Run the expired-reservation sweep on an interval. Safe to call twice."""
        if self._reservation_store is None or self._sweep_task is not None or self._stopped:
            return
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            logger.debug("No running event loop; the reservation sweep stays off")
            return
        self._sweep_task = loop.create_task(self._sweep_loop())

    async def _sweep_loop(self) -> None:
        store = self._reservation_store
        assert store is not None
        while True:
            await asyncio.sleep(self.sweep_interval)
            try:
                await store.sweep_expired()
            except asyncio.CancelledError:
                raise
            except Exception as err:
                # Keep the loop alive: a sweep failure is transient (a Redis
                # blip), and the next tick retries.
                logger.debug("Reservation sweep failed: %s", err)

    def stop(self) -> None:
        """Cancel the sweep loop. Pending releases are left to finish."""
        self._stopped = True
        if self._sweep_task is not None:
            self._sweep_task.cancel()
            self._sweep_task = None

    async def _single_flight(
        self,
        registry: Dict[str, "asyncio.Future[Optional[LeaseState]]"],
        key: str,
        coro: Awaitable[Optional[LeaseState]],
    ) -> Optional[LeaseState]:
        task = asyncio.ensure_future(coro)
        registry[key] = task
        try:
            return await asyncio.shield(task)
        finally:
            if registry.get(key) is task:
                del registry[key]

    async def _release(self, lease_id: str) -> None:
        try:
            await self._wire.release(lease_id)
        except Exception as err:
            logger.warning("Failed to release redundant credit lease %s: %s", lease_id, err)

    def _spawn(self, coro: Awaitable[None]) -> None:
        """Run a fire-and-forget step, holding a reference so it is not collected."""
        try:
            task = asyncio.get_running_loop().create_task(_never_raises(coro))
        except RuntimeError:
            logger.debug("No running event loop; skipping background lease work")
            return
        self._background.add(task)
        task.add_done_callback(self._background.discard)

    async def _drain_background(self) -> None:
        """Wait out pending fire-and-forget work. For tests and close paths."""
        while self._background:
            await asyncio.gather(*list(self._background), return_exceptions=True)


async def _never_raises(coro: Awaitable[None]) -> None:
    try:
        await coro
    except asyncio.CancelledError:
        raise
    except Exception as err:
        logger.debug("Background lease work failed: %s", err)


def _to_datetime(epoch_seconds: float) -> dt.datetime:
    return dt.datetime.fromtimestamp(epoch_seconds, tz=dt.timezone.utc)


def _epoch_seconds(value: dt.datetime) -> float:
    # A naive timestamp from the API is UTC; reading it as local time would
    # shift every expiry by the pod's offset.
    if value.tzinfo is None:
        return value.replace(tzinfo=dt.timezone.utc).timestamp()
    return value.timestamp()


def _grant_from_response(response: Any) -> LeaseGrant:
    data = response.data
    return LeaseGrant(
        lease_id=data.id,
        company_id=data.company_id,
        credit_type_id=data.credit_type_id,
        granted_amount=float(data.granted_amount),
        expires_at=_epoch_seconds(data.expires_at),
    )
