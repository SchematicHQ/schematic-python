"""The client-mode check flow: probe the entitlement, lease, reserve, gate.

One ``check()`` with usage runs the rules engine twice. The first run is a
probe against the company's real balance that names the credit being metered;
the second gates the call against the lease's local balance, after the credits
have already been debited. The conformance vectors in ``conformance/vectors``
pin every step, and ``conformance/SPEC.md`` explains why each one is ordered
the way it is.
"""

from __future__ import annotations

import logging
import time
import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict, Optional, Protocol

from ..types import (
    EventBodyFlagCheck,
    RulesengineCheckFlagResult,
    RulesengineCompany,
    RulesengineFlag,
    RulesengineUser,
)
from .lease_manager import LeaseManager
from .lease_store import LeaseStore
from .reservation_store import ReservationStore
from .types import Clock, ReservationRecord, is_valid_quantity

if TYPE_CHECKING:
    from ..client import CheckFlagOptions, CheckOptions, CheckResult, Reservation

logger = logging.getLogger(__name__)

# The balance the fail-open evaluation substitutes for the metered credit:
# large enough that the credit gate always passes, and still exact as a JSON
# number, so the engine reads back what the SDK sent. This is Node's
# Number.MAX_SAFE_INTEGER, which the vectors name "max_safe_integer".
FAIL_OPEN_BALANCE = 2**53 - 1


class CheckDataStream(Protocol):
    """The slice of ``DataStreamClient`` a lease-bearing check touches.

    Narrow on purpose: it keeps this module off the DataStream client's wider
    surface, and lets the conformance runner script the flow without a socket.
    """

    async def get_flag(self, flag_key: str) -> Optional[RulesengineFlag]: ...

    async def get_company(self, keys: Dict[str, str]) -> RulesengineCompany: ...

    async def get_user(self, keys: Dict[str, str]) -> Any: ...

    def evaluate_flag(
        self, flag: Any, company: Any, user: Any, options: Any = None
    ) -> RulesengineCheckFlagResult: ...


@dataclass
class CreditCheckDeps:
    """Everything a lease-bearing check draws on, gathered by the client."""

    datastream: Optional[CheckDataStream]
    lease_store: LeaseStore
    reservations: ReservationStore
    manager: LeaseManager
    logger: logging.Logger
    # Report a flag_check event for a check this module resolved itself. The
    # plain check paths enqueue one per check, so without this a lease-gated
    # check would be invisible to flag-check analytics and company last-seen.
    # Fallback exits do not call it: the plain check they delegate to reports
    # its own.
    enqueue_flag_check: Callable[[EventBodyFlagCheck], Awaitable[None]]
    clock: Clock = time.time


async def check_with_lease(
    deps: CreditCheckDeps,
    flag_key: str,
    company: Optional[Dict[str, str]],
    user: Optional[Dict[str, str]],
    options: "CheckOptions",
    fallback: Callable[[], Awaitable["CheckResult"]],
) -> "CheckResult":
    """Gate one check against a local lease, returning a hold when it allows.

    ``fallback`` is the plain flag check. Every step that cannot resolve a
    credit to meter defers to it, since the plain check has its own degradation
    story and issues no hold. A step that *can* resolve the credit but cannot
    gate on it goes through ``on_acquire_failure`` instead.
    """
    log = deps.logger
    mode = options.on_acquire_failure or "fail-closed"
    usage = options.usage

    # A malformed usage must never reach the stores, and the caller asked for a
    # contract for exactly this case, so resolve it through that rather than
    # letting it surface as an opaque reserve failure.
    if usage is None or not is_valid_quantity(usage):
        log.error(
            f"Lease check: invalid usage {usage!r} for flag {flag_key}; must be a finite, non-negative number"
        )
        return await _emit_flag_check(
            deps, company, user, _static_failure_result(mode, flag_key, "invalid_usage", None)
        )

    # Nothing to reserve. The plain check still carries the preflight, so every
    # rule evaluates normally; a 0-credit handle would only be a no-op.
    if usage == 0:
        log.debug(f"Lease check: usage is 0 for flag {flag_key}, nothing to reserve, using a plain check")
        return await fallback()

    datastream = deps.datastream
    if datastream is None:
        log.debug("Lease check: no DataStream, using a plain check")
        return await fallback()

    flag = await _load_flag(datastream, flag_key, log)
    if flag is None:
        log.debug(f"Lease check: no cached flag for {flag_key}, using a plain check")
        return await fallback()

    if not company:
        log.debug("Lease check: no company keys, using a plain check")
        return await fallback()

    # Resolve company and user the way a plain DataStream check does: cache
    # first, then a live fetch. Evaluating without an entity the caller named
    # would silently skip its targeted rules and overrides, so a miss defers to
    # the plain check instead.
    resolved_company = await _load_company(datastream, company, log)
    if resolved_company is None:
        return await fallback()

    resolved_user: Optional[RulesengineUser] = None
    if user:
        resolved_user = await _load_user(datastream, user, log)
        if resolved_user is None:
            return await fallback()

    # Entitlement-first resolution. The probe runs against the real balance
    # with no preflight: applying a credit cost to a lease-depleted server
    # balance could fail the credit condition, drop the engine to a
    # lower-priority rule, and hide the entitlement being looked for.
    try:
        probe = datastream.evaluate_flag(flag, resolved_company, resolved_user, None)
    except Exception as err:
        # A probe failure is a resolution miss, not the gate, and no hold
        # exists yet to cancel.
        log.warning(f"Lease check: entitlement probe failed for flag {flag_key} ({err}), using a plain check")
        return await fallback()

    entitlement = probe.entitlement
    if entitlement is None or entitlement.value_type != "credit":
        value_type = entitlement.value_type if entitlement is not None else "<none>"
        log.debug(
            f"Lease check: flag {flag_key} matched a non-credit entitlement (value_type={value_type}), "
            "using a plain check, no reservation"
        )
        return await fallback()

    credit_id = entitlement.credit_id
    consumption_rate = entitlement.consumption_rate or 0.0
    # The caller's subtype wins; otherwise the entitlement names the metered
    # event. A credit entitlement with neither a resolvable subtype nor a
    # positive rate can never be billed, so it is not gateable.
    event_subtype = options.event_subtype or entitlement.event_subtype
    if not credit_id or consumption_rate <= 0 or not event_subtype:
        log.debug(
            f"Lease check: flag {flag_key} has an incomplete credit entitlement "
            f"(credit_id={credit_id or '<none>'}, consumption_rate={consumption_rate}, "
            f"event_subtype={event_subtype or '<none>'}), using a plain check"
        )
        return await fallback()

    credit_cost = usage * consumption_rate

    async def failure(reason: str) -> "CheckResult":
        result = await _handle_lease_failure(
            datastream=datastream,
            log=log,
            mode=mode,
            flag_key=flag_key,
            reason=reason,
            flag=flag,
            company=resolved_company,
            user=resolved_user,
            credit_id=credit_id,
            options=options,
        )
        return await _emit_flag_check(
            deps,
            company,
            user,
            result,
            company_id=resolved_company.id,
            user_id=resolved_user.id if resolved_user is not None else None,
        )

    # The caller's per-check timeout governs the lease wire calls, the same way
    # it governs the plain check's.
    lease = await deps.manager.acquire_if_needed(resolved_company.id, credit_id, options.timeout)
    if lease is None:
        return await failure("lease_acquire_failed")

    # try_reserve is the atomic gate: check and debit in one step, returning
    # the post-debit balance so the pre-debit figure needs no second read.
    try:
        post_reserve_balance = await deps.lease_store.try_reserve(resolved_company.id, credit_id, credit_cost)
        if post_reserve_balance is None:
            # Pass the cost as required_credits so a single large request
            # extends even while the ratio sits above the water mark.
            await deps.manager.maybe_extend(resolved_company.id, credit_id, credit_cost, options.timeout)
            post_reserve_balance = await deps.lease_store.try_reserve(resolved_company.id, credit_id, credit_cost)
    except Exception as err:
        log.error(f"Lease check: reserve against {resolved_company.id}/{credit_id} failed: {err}")
        return await failure("lease_store_error")
    if post_reserve_balance is None:
        return await failure("insufficient_lease_balance")

    # Record the hold after the debit and before the gate. A crash between the
    # debit and this add leaks at most this one hold, reclaimed when the lease
    # expires server-side; recording first would instead leave a record with no
    # debit, which a later consume would refund into a double-spend.
    resolved_config = deps.manager.resolve_config(credit_id)
    record = ReservationRecord(
        id=str(uuid.uuid4()),
        lease_id=lease.lease_id,
        company_id=resolved_company.id,
        credit_type_id=credit_id,
        event_subtype=event_subtype,
        quantity_reserved=usage,
        credits_reserved=credit_cost,
        consumption_rate=consumption_rate,
        expires_at=deps.clock() + resolved_config.reservation_ttl,
        company=company,
        user=user,
    )
    try:
        await deps.reservations.add(record)
    except Exception as err:
        log.error(f"Lease check: failed to persist reservation {record.id}: {err}")
        # Undo the debit rather than strand it until lease expiry. consume
        # claims whatever slice of the add landed and refunds it; a None says
        # nothing landed, so refund the debit directly. Both are pinned to this
        # lease. If the undo itself fails, accept the bounded leak: the slice
        # comes back at lease expiry, which beats risking a double refund.
        try:
            if await deps.reservations.consume(record.id, 0) is None:
                await deps.lease_store.refund(resolved_company.id, credit_id, credit_cost, lease.lease_id)
        except Exception as undo_err:
            log.warning(
                f"Lease check: could not undo the local debit for {record.id} ({undo_err}); "
                "the slice is reclaimed at lease expiry"
            )
        return await failure("lease_store_error")

    # Gate against the lease's local view rather than the server's balance. The
    # substituted figure is the PRE-reservation balance (what try_reserve
    # returned plus what it debited, exact as of the debit), and credit_cost
    # tells the engine what this call costs, so it evaluates the same
    # arithmetic try_reserve just enforced, plus every non-credit rule.
    pre_reservation = post_reserve_balance + credit_cost
    substituted = _substitute_credit_balance(resolved_company, credit_id, pre_reservation)
    try:
        result = datastream.evaluate_flag(
            flag, substituted, resolved_user, _credit_cost_options(credit_id, credit_cost)
        )
    except Exception as err:
        log.error(f"Lease check: rules evaluation failed for flag {flag_key}: {err}")
        # The engine itself is down, so there is no fail-open re-evaluation to
        # run: resolve the mode statically.
        await _cancel_reservation(deps.reservations, record, log)
        return await _emit_flag_check(
            deps,
            company,
            user,
            _static_failure_result(mode, flag_key, f"wasm_error: {err}", flag),
            company_id=resolved_company.id,
            user_id=resolved_user.id if resolved_user is not None else None,
        )

    # Engine-evaluated exits report the engine's resolved ids, mirroring the
    # plain DataStream path's flag_check event.
    engine_company_id = result.company_id or resolved_company.id
    engine_user_id = result.user_id or (resolved_user.id if resolved_user is not None else None)

    if not result.value:
        await _cancel_reservation(deps.reservations, record, log)
        return await _emit_flag_check(
            deps,
            company,
            user,
            _check_result(
                allowed=False,
                value=False,
                reason=result.reason or "denied_by_engine",
                flag_key=result.flag_key or flag_key,
                entitlement=_entitlement(result),
                flag_id=result.flag_id,
            ),
            company_id=engine_company_id,
            user_id=engine_user_id,
            rule_id=result.rule_id,
        )

    # Allowed against the substituted balance, so the hold stands. Top the
    # lease up in the background now that it has been drawn down.
    deps.manager.extend_in_background(resolved_company.id, credit_id)
    return await _emit_flag_check(
        deps,
        company,
        user,
        _check_result(
            allowed=True,
            value=True,
            reason=result.reason or "lease_reserved",
            flag_key=result.flag_key or flag_key,
            reservation=_public_reservation(record),
            entitlement=_entitlement(result),
            flag_id=result.flag_id,
        ),
        company_id=engine_company_id,
        user_id=engine_user_id,
        rule_id=result.rule_id,
    )


async def _emit_flag_check(
    deps: CreditCheckDeps,
    req_company: Optional[Dict[str, str]],
    req_user: Optional[Dict[str, str]],
    result: "CheckResult",
    *,
    company_id: Optional[str] = None,
    user_id: Optional[str] = None,
    rule_id: Optional[str] = None,
) -> "CheckResult":
    """Report a lease-path resolution and pass the result straight through.

    Analytics must never change a verdict the caller is already acting on, so a
    failure here is logged and swallowed.
    """
    try:
        await deps.enqueue_flag_check(
            EventBodyFlagCheck(
                flag_key=result.flag_key,
                value=result.value,
                reason=result.reason,
                error=result.error,
                flag_id=result.flag_id,
                company_id=company_id,
                user_id=user_id,
                rule_id=rule_id,
                req_company=req_company,
                req_user=req_user,
            )
        )
    except Exception as err:
        deps.logger.debug(f"Lease check: failed to report the flag_check event: {err}")
    return result


async def _load_flag(datastream: CheckDataStream, flag_key: str, log: logging.Logger) -> Optional[RulesengineFlag]:
    try:
        return await datastream.get_flag(flag_key)
    except Exception as err:
        log.warning(f"Lease check: failed to load flag {flag_key}: {err}")
        return None


async def _load_company(
    datastream: CheckDataStream, keys: Dict[str, str], log: logging.Logger
) -> Optional[RulesengineCompany]:
    try:
        return await datastream.get_company(keys)
    except Exception as err:
        log.debug(f"Lease check: company fetch failed for keys {keys} ({err}), using a plain check")
        return None


async def _load_user(
    datastream: CheckDataStream, keys: Dict[str, str], log: logging.Logger
) -> Optional[RulesengineUser]:
    try:
        return await datastream.get_user(keys)
    except Exception as err:
        log.debug(f"Lease check: user fetch failed for keys {keys} ({err}), using a plain check")
        return None


async def _handle_lease_failure(
    *,
    datastream: CheckDataStream,
    log: logging.Logger,
    mode: str,
    flag_key: str,
    reason: str,
    flag: RulesengineFlag,
    company: RulesengineCompany,
    user: Optional[RulesengineUser],
    credit_id: str,
    options: "CheckOptions",
) -> "CheckResult":
    """Resolve a check that could not gate: acquire failed, store unreachable,
    or the lease is exhausted.

    fail-closed denies. fail-open means assume the credits are there, not skip
    the evaluation: the rules still run with the balance substituted to an
    effectively unlimited value, so plan targeting, overrides, and every
    non-credit condition still apply, and a company that is not entitled stays
    denied with the lease backend down. Only an error in that evaluation drops
    to a blanket allow.
    """
    if mode == "fail-closed":
        return _static_failure_result(mode, flag_key, reason, flag)

    try:
        substituted = _substitute_credit_balance(company, credit_id, FAIL_OPEN_BALANCE)
        result = datastream.evaluate_flag(flag, substituted, user, _preflight_options(options))
    except Exception as err:
        log.warning(f"Lease check: the fail-open evaluation failed ({err}); allowing")
        return _static_failure_result(mode, flag_key, reason, flag)
    return _check_result(
        allowed=result.value,
        value=result.value,
        reason=f"{result.reason or 'evaluated'} ({reason}_fail_open)",
        flag_key=result.flag_key or flag_key,
        entitlement=_entitlement(result),
        flag_id=result.flag_id or flag.id,
        error=reason,
    )


def _static_failure_result(
    mode: str, flag_key: str, reason: str, flag: Optional[RulesengineFlag]
) -> "CheckResult":
    """Resolve a mode with no evaluation behind it: deny for fail-closed,
    blanket allow for fail-open.

    Used when the engine is the thing that failed, and when the fail-open
    evaluation itself errors.
    """
    allowed = mode != "fail-closed"
    return _check_result(
        allowed=allowed,
        value=allowed,
        reason=f"{reason}_fail_open" if allowed else reason,
        flag_key=flag_key,
        flag_id=flag.id if flag is not None else None,
        error=reason,
    )


async def _cancel_reservation(
    reservations: ReservationStore, record: ReservationRecord, log: logging.Logger
) -> None:
    """Claim the hold and refund all of it. Best effort: a failure leaves the
    hold for the sweeper or for lease expiry."""
    try:
        await reservations.consume(record.id, 0)
    except Exception as err:
        log.warning(
            f"Lease check: failed to cancel reservation {record.id} ({err}); "
            "its hold is reclaimed by the sweeper or at lease expiry"
        )


def _substitute_credit_balance(
    company: RulesengineCompany, credit_id: str, balance: float
) -> RulesengineCompany:
    balances = dict(company.credit_balances or {})
    balances[credit_id] = balance
    return company.model_copy(update={"credit_balances": balances})


def _credit_cost_options(credit_id: str, credit_cost: float) -> "CheckFlagOptions":
    from ..client import CheckFlagOptions

    return CheckFlagOptions(credit_cost={credit_id: credit_cost})


def _preflight_options(options: "CheckOptions") -> Optional["CheckFlagOptions"]:
    from ..client import _check_options_to_flag_options

    return _check_options_to_flag_options(options)


def _entitlement(result: RulesengineCheckFlagResult) -> Optional[Any]:
    if result.entitlement is None:
        return None
    from ..types import FeatureEntitlement

    return FeatureEntitlement.model_validate(result.entitlement.model_dump())


def _public_reservation(record: ReservationRecord) -> "Reservation":
    """The caller's handle on a hold carved out of a lease."""
    import datetime as dt

    from ..client import Reservation

    return Reservation(
        id=record.id,
        lease_id=record.lease_id,
        mode="client",
        company_id=record.company_id,
        credit_type_id=record.credit_type_id,
        event_subtype=record.event_subtype,
        quantity_reserved=record.quantity_reserved,
        credits_reserved=record.credits_reserved,
        consumption_rate=record.consumption_rate,
        expires_at=dt.datetime.fromtimestamp(record.expires_at, tz=dt.timezone.utc),
        company=record.company,
        user=record.user,
    )


def _check_result(**fields: Any) -> "CheckResult":
    """CheckResult is defined on the client, which imports this module, so the
    import waits until call time to keep the cycle from closing at import."""
    from ..client import CheckResult

    return CheckResult(**fields)
