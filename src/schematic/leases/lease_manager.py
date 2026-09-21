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
import uuid
from dataclasses import dataclass
from typing import Any, Awaitable, Dict, Optional, Protocol, Set

from .lease_store import LeaseStore, lease_key
from .reservation_store import ReservationStore
from .types import (
    DEFAULT_SWEEP_INTERVAL,
    SHUTDOWN_DRAIN_TIMEOUT,
    Clock,
    LeaseConfig,
    LeaseState,
    ResolvedLeaseConfig,
    resolve_lease_config,
)

logger = logging.getLogger(__name__)

# How many in-flight extends one caller will wait out before issuing its own.
# Two covers the case the single-flight was written for: the flight a caller
# joins, and the follow-up another caller registers while it was waiting.
MAX_EXTEND_JOINS = 2

# A wait on a shared extend that ran out the joiner's own timeout.
_JOIN_TIMED_OUT = object()


@dataclass
class LeaseGrant:
    """What the server says a lease is, after an acquire or an extend."""

    lease_id: str
    company_id: str
    credit_type_id: str
    # The server-authoritative TOTAL, not the increment an extend asked for.
    granted_amount: float
    expires_at: float


@dataclass
class _Flight:
    """An in-flight wire call under single-flight.

    ``requested_additional`` is the additional amount an extend's wire call
    asked for, the figure a joiner compares its own shortfall against. Acquire
    flights share the type and leave it unset.
    """

    task: "asyncio.Future[Optional[LeaseState]]"
    requested_additional: Optional[float] = None


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
        timeout: Optional[float] = None,
    ) -> LeaseGrant: ...

    async def extend(
        self,
        lease_id: str,
        additional_amount: float,
        expires_at: float,
        timeout: Optional[float] = None,
    ) -> LeaseGrant: ...

    async def release(self, lease_id: str) -> None: ...


class CreditsWireClient:
    """Adapter over the generated async credits client (``AsyncCreditsClient``)."""

    def __init__(self, credits_client: Any, *, request_options: Optional[Any] = None) -> None:
        self._credits = credits_client
        self._request_options = request_options

    def _options(self, timeout: Optional[float]) -> Optional[Any]:
        """The caller's per-check timeout wins over the client-wide options,
        which is what a caller asking for one on this check means."""
        if timeout is None:
            return self._request_options
        return {"timeout": timeout}

    async def acquire(
        self,
        company_id: str,
        credit_type_id: str,
        requested_amount: float,
        expires_at: float,
        timeout: Optional[float] = None,
    ) -> LeaseGrant:
        response = await self._credits.acquire_credit_lease(
            company_id=company_id,
            credit_type_id=credit_type_id,
            requested_amount=requested_amount,
            expires_at=_to_datetime(expires_at),
            request_options=self._options(timeout),
        )
        return _grant_from_response(response)

    async def extend(
        self,
        lease_id: str,
        additional_amount: float,
        expires_at: float,
        timeout: Optional[float] = None,
    ) -> LeaseGrant:
        # One key per extend, minted before the call so that every attempt the
        # retry policy makes carries the same one: without it a 502 arriving
        # after the server committed the growth would grow the lease twice.
        response = await self._credits.extend_credit_lease(
            lease_id,
            additional_amount=additional_amount,
            expires_at=_to_datetime(expires_at),
            idempotency_key=str(uuid.uuid4()),
            request_options=self._options(timeout),
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
        self._inflight_acquire: Dict[str, _Flight] = {}
        self._inflight_extend: Dict[str, _Flight] = {}
        # Every task shutdown has to wait out, whatever it resolves to: the
        # fire-and-forget work from `_spawn` and the single-flight acquires and
        # extends, which resolve to a LeaseState.
        self._background: Set["asyncio.Task[Any]"] = set()
        self._sweep_task: Optional["asyncio.Task[None]"] = None
        self._stopped = False

    def resolve_config(self, credit_type_id: str) -> ResolvedLeaseConfig:
        return resolve_lease_config(self._config, None, credit_type_id)

    @property
    def sweep_interval(self) -> float:
        return self._config.sweep_interval or DEFAULT_SWEEP_INTERVAL

    async def acquire_if_needed(
        self, company_id: str, credit_type_id: str, timeout: Optional[float] = None
    ) -> Optional[LeaseState]:
        """The slot's live lease, acquiring one over the wire if none is live.

        ``timeout`` governs the wire call this caller starts. A caller that
        joins an in-flight acquire rides the first caller's timeout, since
        there is one shared call to time out.
        """
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
            return await asyncio.shield(inflight.task)
        return await self._single_flight(
            self._inflight_acquire, key, self._acquire(company_id, credit_type_id, timeout)
        )

    async def _acquire(
        self, company_id: str, credit_type_id: str, timeout: Optional[float] = None
    ) -> Optional[LeaseState]:
        resolved = self.resolve_config(credit_type_id)
        try:
            grant = await self._wire.acquire(
                company_id,
                credit_type_id,
                resolved.lease_size,
                self._clock() + resolved.lease_duration,
                timeout,
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
        timeout: Optional[float] = None,
    ) -> Optional[LeaseState]:
        """Extend the slot's lease when the local view warrants it.

        Triggered by either the low-water-mark ratio (steady-state refresh) or
        a ``required_credits`` hint above the local remaining (a check just
        failed a reserve of that size).

        A caller arriving while an extend is in flight joins it. If its own
        shortfall is larger than what that extend asked for, it waits the
        flight out and then issues exactly one follow-up extend for the
        remaining difference: otherwise it would inherit a tranche-sized ask
        and fail its post-extend retry with credits still sitting on the
        server. A flight it finds on the way back is only joined if that one
        covers the shortfall too; a smaller one is waited out, never inherited.
        """
        return await self._maybe_extend(company_id, credit_type_id, required_credits, timeout)

    async def _maybe_extend(
        self,
        company_id: str,
        credit_type_id: str,
        required_credits: Optional[float],
        timeout: Optional[float],
    ) -> Optional[LeaseState]:
        # A joiner waits on someone else's wire call, which runs on whatever
        # timeout ITS caller set (a background refresh uses the client
        # default). So the wait is capped at this caller's own timeout: a check
        # with 200ms to spend must not sit behind a 30s extend.
        join_deadline = None if timeout is None else time.monotonic() + timeout
        # Joins are budgeted, extends of our own are not: a caller may wait out
        # flights that ask for too little, but once the budget runs out it
        # issues its own single extend rather than joining again. Without the
        # budget a caller could wait behind an unbounded run of other callers'
        # follow-ups; without the own extend it would return a balance it
        # already knows is short and fail its retry with credits on the server.
        joins_left = MAX_EXTEND_JOINS
        while True:
            entry = await self._read_live_lease(company_id, credit_type_id)
            if entry is None:
                return None
            resolved = self.resolve_config(credit_type_id)
            if not self._needs_extend(entry, resolved, required_credits):
                return entry

            # Size the extend to cover the request that triggered it: a single
            # check needing more than remaining plus one tranche would
            # otherwise fail its post-extend retry forever, however much
            # balance the server has. The steady-state path keeps asking for
            # the configured tranche. Sized here, one level above the wire
            # call, so the flight registered below and the request body
            # provably carry the same number for a joiner to compare against.
            shortfall = (required_credits - entry.local_remaining_credits) if required_credits is not None else 0.0
            additional_amount = max(resolved.lease_size, shortfall)

            key = lease_key(company_id, credit_type_id)
            inflight = self._inflight_extend.get(key)
            if inflight is not None and joins_left > 0:
                joined = await self._join_within(inflight.task, join_deadline)
                if joined is _JOIN_TIMED_OUT:
                    # The flight runs on for everybody else; we just stop
                    # waiting on it. Reporting no entry sends the caller down
                    # its fail-open/fail-closed path, which is what its timeout
                    # asked for.
                    logger.debug(
                        "Extend in flight for %s/%s outlasted the caller's timeout; not waiting on it",
                        company_id,
                        credit_type_id,
                    )
                    return None
                # The flight asked for at least what we need: every
                # watermark-driven joiner, and any check the tranche covers.
                # One wire call serves all of them, which is the point of
                # single-flight.
                if additional_amount <= (inflight.requested_additional or 0.0):
                    return joined
                # It asked for less. Go round again to re-read the slot it just
                # moved, so what we ask for next is sized against the balance
                # it left rather than the one we started from.
                joins_left -= 1
                continue
            return await self._single_flight(
                self._inflight_extend,
                key,
                self._recheck_and_extend(
                    company_id, credit_type_id, resolved, required_credits, additional_amount, timeout
                ),
                additional_amount,
            )

    async def _join_within(
        self,
        task: "asyncio.Future[Optional[LeaseState]]",
        deadline: Optional[float],
    ) -> Any:
        """Await a flight somebody else is running, giving up at ``deadline``.

        Giving up abandons only our wait: the flight keeps running for the
        callers still on it, and whatever it installs is there for our next
        check to read.
        """
        if deadline is None:
            return await asyncio.shield(task)
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return _JOIN_TIMED_OUT
        try:
            return await asyncio.wait_for(asyncio.shield(task), remaining)
        except asyncio.TimeoutError:
            return _JOIN_TIMED_OUT

    async def _read_live_lease(self, company_id: str, credit_type_id: str) -> Optional[LeaseState]:
        """The slot's lease, or None when the read fails or the lease is absent
        or expired.

        Never extend an expired lease: the server treats it as released and has
        already refunded its remainder, so the only correct move is a fresh
        acquire on the next check.
        """
        try:
            entry = await self._lease_store.get(company_id, credit_type_id)
        except Exception as err:
            logger.warning("Failed to read lease store for %s/%s: %s", company_id, credit_type_id, err)
            return None
        if entry is None:
            return None
        if entry.expires_at <= self._clock():
            return None
        return entry

    def _needs_extend(
        self,
        entry: LeaseState,
        resolved: ResolvedLeaseConfig,
        required_credits: Optional[float],
    ) -> bool:
        """Whether the slot sits low enough to warrant an extend."""
        ratio = entry.local_remaining_credits / max(entry.granted_amount, 1)
        below_watermark = ratio <= resolved.low_water_mark
        below_required = required_credits is not None and entry.local_remaining_credits < required_credits
        return below_watermark or below_required

    async def _recheck_and_extend(
        self,
        company_id: str,
        credit_type_id: str,
        resolved: ResolvedLeaseConfig,
        required_credits: Optional[float],
        additional_amount: float,
        timeout: Optional[float],
    ) -> Optional[LeaseState]:
        """Re-read the slot now that this flight owns it, and extend only if the
        fresh row still warrants one.

        The row that decided this extend was read before the flight was
        registered, so an extend that landed in that gap, clearing its own
        flight on the way out, would otherwise be followed by a second extend,
        under a new idempotency key, for a lease it already topped up. The
        registered ``requested_additional`` stands: a joiner compares its
        shortfall against that figure, so the wire body has to carry it.
        """
        entry = await self._read_live_lease(company_id, credit_type_id)
        if entry is None:
            return None
        if not self._needs_extend(entry, resolved, required_credits):
            return entry
        return await self._extend(entry, resolved, additional_amount, timeout)

    async def _extend(
        self,
        entry: LeaseState,
        resolved: ResolvedLeaseConfig,
        additional_amount: float,
        timeout: Optional[float] = None,
    ) -> Optional[LeaseState]:
        try:
            grant = await self._wire.extend(
                entry.lease_id,
                additional_amount,
                self._clock() + resolved.lease_duration,
                timeout,
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

    def extend_in_background(self, company_id: str, credit_type_id: str) -> None:
        """Kick off a water-mark extend without waiting for it.

        A check that just drew the lease down should not pay for the top-up, so
        the extend runs as tracked background work and never raises into the
        caller.
        """

        async def run() -> None:
            await self.maybe_extend(company_id, credit_type_id)

        self._spawn(run())

    async def release_all_local_leases(self, timeout: Optional[float] = None) -> None:
        """Release every live lease this process exclusively holds.

        Only a per-process store answers ``list_leases``; a shared backend
        returns ``None`` and is skipped, since sibling pods still draw on those
        leases. Expired leases are skipped too: the server already swept them.
        Best-effort, with failures falling back to server-side expiry.

        Bounded by ``timeout``, so a store or wire call that never lands cannot
        hold a closing client open; whatever is abandoned expires server-side.
        """
        budget = SHUTDOWN_DRAIN_TIMEOUT if timeout is None else timeout
        try:
            entries = self._lease_store.list_leases()
        except Exception as err:
            logger.warning("Failed to enumerate leases on close: %s", err)
            return
        if not entries:
            return
        now = self._clock()
        live = [entry for entry in entries if entry.expires_at > now]
        if not live:
            return
        releases = asyncio.gather(*(self._release_local_lease(entry) for entry in live))
        try:
            await asyncio.wait_for(releases, budget)
        except asyncio.TimeoutError:
            logger.warning(
                "Timed out after %ss releasing credit leases on close; "
                "any still held will be released by server-side expiry",
                budget,
            )

    async def _release_local_lease(self, entry: LeaseState) -> None:
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
        registry: Dict[str, _Flight],
        key: str,
        coro: Awaitable[Optional[LeaseState]],
        requested_additional: Optional[float] = None,
    ) -> Optional[LeaseState]:
        task = asyncio.ensure_future(coro)
        flight = _Flight(task=task, requested_additional=requested_additional)
        registry[key] = flight
        # The registry dedupes concurrent callers and the drain set waits the
        # wire call out; they have different lifetimes. Cancelling a caller
        # cancels its `shield`, not the task, and drops the registry entry the
        # instant it lands, so without this the acquire would be tracked
        # nowhere and could install a lease after shutdown released the store.
        self._background.add(task)
        task.add_done_callback(self._background.discard)
        try:
            return await asyncio.shield(task)
        finally:
            # Identity-guarded rather than an unconditional delete: a joiner
            # whose shortfall outran this flight registers a follow-up under
            # the same key, and this cleanup must not evict it.
            if registry.get(key) is flight:
                del registry[key]

    async def _release(self, lease_id: str) -> None:
        try:
            await self._wire.release(lease_id)
        except Exception as err:
            logger.warning("Failed to release redundant credit lease %s: %s", lease_id, err)

    def _spawn(self, coro: Awaitable[None]) -> None:
        """Run a fire-and-forget step, holding a reference so it is not collected."""
        if self._stopped:
            # Past stop() the drain has run or is running; work started now
            # would install or extend a lease nothing is left to release.
            logger.debug("Lease manager is stopped; skipping background lease work")
            if asyncio.iscoroutine(coro):
                coro.close()
            return
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

    async def drain(self, timeout: Optional[float] = None) -> None:
        """Wait out in-flight lease work, so a close can release what it installed.

        Bounded: whatever has not landed by ``timeout`` is cancelled rather
        than stalling the caller's shutdown, and a grant the server issued for
        it falls back to server-side expiry.
        """
        budget = SHUTDOWN_DRAIN_TIMEOUT if timeout is None else timeout
        try:
            await asyncio.wait_for(self._drain_background(), budget)
        except asyncio.TimeoutError:
            logger.warning(
                "Timed out after %ss draining in-flight credit lease work; "
                "any credits it holds will be released by server-side expiry",
                budget,
            )


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
