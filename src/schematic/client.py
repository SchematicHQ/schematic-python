import asyncio
import atexit
import datetime as dt
import logging
import math
import time
import uuid
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Union

import httpx
from .base_client import AsyncBaseSchematic, BaseSchematic
from .cache import (
    DEFAULT_CACHE_SIZE,
    DEFAULT_CACHE_TTL,
    AsyncCacheProvider,
    CacheProvider,
    LocalCache,
    RedisCache,
)
from .core.api_error import ApiError
from .core.request_options import RequestOptions
from .datastream import DataStreamClient, DataStreamClientOptions
from .errors import PaymentRequiredError
from .event_buffer import AsyncEventBuffer, EventBuffer
from .event_capture import AsyncEventCaptureClient, EventCaptureClient
from .http_client import AsyncOfflineHTTPClient, OfflineHTTPClient
from .leases import (
    DEFAULT_LEASE_DURATION,
    DEFAULT_PREWARM_RESOLVE_TIMEOUT,
    SHUTDOWN_DRAIN_TIMEOUT,
    CreditCheckDeps,
    CreditsWireClient,
    InMemoryLeaseStore,
    InMemoryReservationStore,
    LeaseConfig,
    LeaseConfigOverride,
    LeaseManager,
    LeaseStore,
    RedisLeaseStore,
    RedisReservationStore,
    ReservationStore,
    check_with_lease,
    consume_reservation_and_build_event,
)
from .leases import build_reservation_track_event as _build_reservation_track_event
from .leases import is_valid_quantity as _is_valid_quantity
from .leases import settled_quantity as _settled_quantity
from .leases.redis_lease_store import DEFAULT_KEY_PREFIX as DEFAULT_LEASE_KEY_PREFIX
from .logging import DEFAULT_LOG_LEVEL, LogLevel, get_default_logger
from .types import (
    CheckAndReserveFlagResponseData,
    CheckFlagRequestBody,
    CheckFlagResponseData,
    CreateEventRequestBody,
    EventBody,
    EventBodyFlagCheck,
    EventBodyIdentify,
    EventBodyIdentifyCompany,
    EventBodyTrack,
    FeatureEntitlement,
    FlagCheckReservationResponseData,
    PreflightEventUsageRequestBody,
    PreflightRequestBody,
    RulesengineCheckFlagResult,
)

# Reason strings used when returning a fallback / default flag value.
# Kept descriptive (rather than "flag default") so callers reading the reason
# field can distinguish *why* a default was returned.
REASON_OFFLINE = "Offline mode - using default value"
REASON_FLAG_NOT_FOUND = "Flag not found - using default value"
REASON_ERROR = "Error occurred - using default value"

# Prefix of the deterministic idempotency key carried by the track event that
# settles a reservation, so a duplicate or retried settle is dropped
# server-side instead of billing the usage twice.
RESERVATION_TRACK_IDEMPOTENCY_PREFIX = "lease-reservation:"

# How long a server-side hold lives when the caller configures no TTL. In
# seconds, like every other duration on this client.
DEFAULT_RESERVATION_TTL = 60.0

# How often prewarm re-asks DataStream for a company it is waiting on.
PREWARM_POLL_INTERVAL = 0.1

# The longest hold the server will take. A longer configured TTL is clamped to
# it, rather than sent and rejected on every check.
MAX_RESERVATION_TTL = 3600.0
# Room for the two clocks to disagree. expires_at is computed here and measured
# against the server's own clock, so a TTL sitting exactly on the cap is
# rejected whenever this process runs even slightly ahead.
RESERVATION_TTL_SKEW_ALLOWANCE = 60.0

# What the API calls a denial for want of credits. The 402 branch and the
# plain 200-with-value-false branch both report it, so callers have one string
# to match on.
INSUFFICIENT_CREDITS_REASON = "Insufficient credits"

# Where a credit hold lives for a check() that passes usage.
# - "server": one check-and-reserve API call per check; the server evaluates
#   the flag and takes the hold in the same round trip.
# - "client": a lease drawn from the server per company and credit type, with
#   each check's hold carved out of it locally. Needs DataStream, so only
#   AsyncSchematic can run it.
# - "auto" (default): "client" when DataStream is running, "server" otherwise.
CreditLeaseMode = Literal["client", "server", "auto"]

# What a check does when it cannot gate: deny ("fail-closed"), or fall back to
# the caller's default value ("fail-open").
OnAcquireFailure = Literal["fail-closed", "fail-open"]


@dataclass
class EventUsage:
    """Usage of one event subtype, for preflighting a flag check."""

    event_subtype: str
    # Any finite non-negative number. Both the REST body and the local engine
    # take an integer, so a fraction rounds up at each of those boundaries.
    quantity: float


@dataclass
class CheckFlagOptions:
    """Options for flag check methods."""

    default_value: Optional[Union[bool, Callable[[], bool]]] = None
    timeout: Optional[float] = None
    # Preflight fields: hypothetical usage the flag is evaluated against, so a
    # caller can ask "would this action be allowed?" before performing it.
    # They mirror the API's PreflightRequestBody.
    #
    # Quantity applied to any numeric condition met while evaluating the flag.
    # Both the REST body and the local engine take an integer, so a fraction
    # rounds up rather than letting the check pass on less usage than the
    # action is about to record.
    usage: Optional[float] = None
    # Usage of one specific event subtype. Preferred over `usage` when the
    # subtype is known, since it only moves conditions measuring that subtype.
    event_usage: Optional[EventUsage] = None
    # Cost in credits, keyed by credit ID, for callers that already computed
    # it. Takes precedence over usage and event_usage for the same credit.
    credit_cost: Optional[Dict[str, float]] = None


@dataclass
class CreditLeaseConfig:
    """Opt in to credit-gated checks (``check`` / ``track_with_reservation``).

    Leave it unset and ``check`` is a plain flag check that holds nothing.
    Every duration is in seconds. The knobs below the first two steer client
    mode only, and server mode warns at construction when one is set.
    """

    # Where the hold lives. "server" takes it over the check-and-reserve API;
    # "client" carves it out of a local lease over DataStream; "auto" picks
    # client when DataStream is running and server otherwise.
    mode: CreditLeaseMode = "auto"
    # How long a hold survives unsettled. Size it above the longest expected
    # gap between check() and track_with_reservation(). Anything above the
    # server's one hour cap is clamped, in server mode. Client mode keeps it:
    # the TTL only drives the local sweeper there.
    default_reservation_ttl: float = DEFAULT_RESERVATION_TTL
    # Lease lifetime requested at acquire and extend. Default 5 minutes.
    default_lease_duration: Optional[float] = None
    # Credits requested per acquire, and the minimum extend tranche. Default 10000.
    default_lease_size: Optional[float] = None
    # Remaining/granted ratio at or below which a background extend fires. Default 0.25.
    low_water_mark: Optional[float] = None
    # How often expired reservations are swept back to their leases. Default 1 second.
    sweep_interval: Optional[float] = None
    # How long prewarm() waits for a freshly identified company to surface
    # over DataStream. Default 5 seconds; 0 skips the wait.
    prewarm_resolve_timeout: Optional[float] = None
    # A connected redis.asyncio client for lease and reservation state. Without
    # one the SDK reuses the DataStream company cache's Redis, and failing that
    # keeps lease state per-process, which gates within one process only.
    redis_client: Optional[Any] = None
    # Key prefix for lease and reservation keys. Defaults to the DataStream
    # cache's prefix when its Redis is reused, else "schematic:", which is what
    # the Node SDK uses, so mixed fleets share the same leases.
    redis_key_prefix: Optional[str] = None
    # Per-credit-type overrides of the four resolvable knobs, keyed by credit
    # type ID. Client mode only.
    overrides: Optional[Dict[str, LeaseConfigOverride]] = None


@dataclass
class CheckOptions:
    """Options accepted by ``check``."""

    # Units of the feature this operation will consume, as any finite
    # non-negative number. The check holds usage * consumption_rate credits.
    # A check takes at most one hold.
    usage: Optional[float] = None
    # Event subtype the usage applies to, e.g. "inference_tokens". Needed only
    # when the flag meters more than one event.
    event_subtype: Optional[str] = None
    # What to do when the check cannot gate (API error, unreachable server).
    on_acquire_failure: OnAcquireFailure = "fail-closed"
    default_value: Optional[Union[bool, Callable[[], bool]]] = None
    # Per-check timeout for the API calls this check makes, in seconds.
    timeout: Optional[float] = None


@dataclass
class Reservation:
    """Handle returned by ``check`` when a credit hold was taken.

    Pass it to ``track_with_reservation`` when the work completes.
    """

    id: str
    # The lease the hold draws from. Server mode has no lease, so this mirrors
    # `id` and the field stays populated for code that reads it.
    lease_id: str
    mode: Literal["client", "server"]
    company_id: str
    credit_type_id: str
    # Event subtype the settling track event is recorded under.
    event_subtype: str
    quantity_reserved: float
    credits_reserved: float
    consumption_rate: float
    # When the unspent hold is refunded if nothing settles it.
    expires_at: dt.datetime
    # Evaluation context the hold was issued for, so the settling track event
    # attributes the usage to the same company and user.
    company: Optional[Dict[str, str]] = None
    user: Optional[Dict[str, str]] = None


@dataclass
class CheckResult:
    """Result of ``check``."""

    # Whether the caller may proceed.
    allowed: bool
    # The flag's boolean value; `allowed` mirrors it outside the credit paths.
    value: bool
    reason: str
    flag_key: str
    reservation: Optional[Reservation] = None
    entitlement: Optional[FeatureEntitlement] = None
    flag_id: Optional[str] = None
    error: Optional[str] = None


@dataclass
class TrackWithReservationOptions:
    """Extras accepted by ``track_with_reservation``."""

    traits: Optional[Dict[str, Any]] = None


# Prefix Schematic's secure company ids carry, whatever key name they are
# passed under.
COMPANY_ID_PREFIX = "comp_"


def _schematic_id(keys: Dict[str, str], prefix: str) -> Optional[str]:
    """The Schematic id hiding among a set of entity keys, recognized by its
    secure-id prefix.

    The server reads keys this way once a key lookup has come up empty, so
    ``{"account_id": "comp_1"}`` resolves and ``{"id": "acme"}`` does not: the
    prefix decides, not the key's name.
    """
    for value in keys.values():
        if isinstance(value, str) and value.startswith(prefix):
            return value
    return None


def _build_preflight(options: Optional[CheckFlagOptions]) -> Optional[PreflightRequestBody]:
    """Build the preflight body for a flag check, or None when the caller set
    no preflight field."""
    if options is None:
        return None
    if options.usage is None and options.event_usage is None and options.credit_cost is None:
        return None
    # The wire quantities are integers, so a fraction rounds up here the way it
    # does at the engine boundary.
    return PreflightRequestBody(
        credit_cost=options.credit_cost,
        event_usage=(
            PreflightEventUsageRequestBody(
                event_subtype=options.event_usage.event_subtype,
                quantity=_preflight_quantity(options.event_usage.quantity),
            )
            if options.event_usage is not None
            else None
        ),
        usage=None if options.usage is None else _preflight_quantity(options.usage),
    )


def _preflight_quantity(usage: float) -> int:
    """Cast a usage onto the integer the preflight body carries.

    A hold can be sized from a fractional usage, but the API's preflight usage
    is an integer. A preflight asks an upper-bound question ("would this action
    be allowed?"), so a fraction rounds up: the check must not pass on less
    usage than the operation is about to record.
    """
    return int(usage) if float(usage).is_integer() else math.ceil(usage)


def _check_options_to_flag_options(options: Optional[CheckOptions]) -> Optional[CheckFlagOptions]:
    """Map credit-aware check options onto plain flag check options.

    With an event subtype the usage goes out as the event_usage pair so the
    engine matches it to that subtype's condition; without one it goes out as
    the generic usage knob. A usage no hold could be sized from is dropped
    instead of threaded, since it would only make the preflight unserializable.
    """
    if options is None:
        return None
    flag_options = CheckFlagOptions(default_value=options.default_value, timeout=options.timeout)
    if options.usage is not None and _is_valid_quantity(options.usage):
        quantity = _preflight_quantity(options.usage)
        if options.event_subtype is not None:
            flag_options.event_usage = EventUsage(event_subtype=options.event_subtype, quantity=quantity)
        else:
            flag_options.usage = quantity
    return flag_options


# Options that only steer the client-mode lease plumbing, so server mode would
# quietly ignore them.
_CLIENT_ONLY_LEASE_OPTIONS = (
    "default_lease_duration",
    "default_lease_size",
    "low_water_mark",
    "sweep_interval",
    "prewarm_resolve_timeout",
    "redis_client",
    "redis_key_prefix",
    "overrides",
)


def _mode_uses_leases(mode: CreditLeaseMode, datastream_enabled: bool) -> bool:
    """Whether a configured mode wants the local lease plumbing built."""
    if mode == "server":
        return False
    if mode == "client":
        return True
    return datastream_enabled


def _warn_credit_lease_config(
    logger: logging.Logger,
    credit_leases: CreditLeaseConfig,
    offline: bool,
    *,
    supports_client_mode: bool,
    datastream_enabled: bool = False,
) -> None:
    """Say once, at construction, when the configured credit leases will not
    gate the way the caller asked."""
    if offline:
        logger.warning(
            "credit_leases is configured but the client is offline; check() returns flag defaults "
            "and holds no credits."
        )
        return
    # The client-only knobs are ignored wherever the mode lands on server, not
    # only where the caller named it: 'auto' without DataStream lands there
    # too, and on the sync client it always does.
    if not _mode_uses_leases(credit_leases.mode, supports_client_mode and datastream_enabled):
        ignored = [name for name in _CLIENT_ONLY_LEASE_OPTIONS if getattr(credit_leases, name) is not None]
        if ignored:
            logger.warning(
                f"credit_leases resolves to server mode, so {', '.join(ignored)} will be ignored; those "
                "options only apply to client mode, where leases are carved up locally over DataStream."
            )
    if credit_leases.mode == "server":
        return
    if not supports_client_mode:
        if credit_leases.mode == "client":
            logger.warning(
                "credit_leases.mode is 'client', which needs DataStream, and DataStream is only available on "
                "AsyncSchematic; check() falls back to a plain, ungated flag check. Use 'server' (or the 'auto' "
                "default) to gate on credits from this client."
            )
        return
    if datastream_enabled:
        return
    if credit_leases.mode == "client":
        logger.warning(
            "credit_leases.mode is 'client' but DataStream is not enabled; check() falls back to plain flag "
            "checks with no credit gating. Set use_datastream=True to gate on local leases."
        )
    else:
        # Not a misconfiguration: auto without DataStream is the server-mode
        # default, which gates over the API instead.
        logger.info(
            "credit_leases is configured and DataStream is not enabled, so credit holds are taken in server "
            "mode, one check-and-reserve call per check. Set use_datastream=True for client-side leases."
        )


def _resolve_reservation_ttl(logger: logging.Logger, credit_leases: Optional[CreditLeaseConfig]) -> float:
    """How long this client asks the server to hold credits for, clamped to
    what the server will grant.

    Client mode is exempt: its TTL never reaches the server, it only tells the
    local sweeper when to refund an unsettled hold, and the caller may well
    want one that outlives an hour.
    """
    if credit_leases is None:
        return DEFAULT_RESERVATION_TTL
    ttl = credit_leases.default_reservation_ttl
    if credit_leases.mode == "client":
        return ttl
    effective = MAX_RESERVATION_TTL - RESERVATION_TTL_SKEW_ALLOWANCE
    if ttl > effective:
        logger.warning(
            f"credit_leases.default_reservation_ttl of {ttl}s is above the server's one hour cap; "
            f"server-mode holds will be clamped to {effective}s"
        )
        return effective
    return ttl


def _reservation_request_kwargs(options: CheckOptions) -> Dict[str, Any]:
    """Preflight body, idempotency key and request options for a
    check-and-reserve call, with the preflight omitted when the caller set
    nothing.

    One key per check, minted before the call so that every attempt the retry
    policy makes carries the same one: the server answers the repeat with the
    hold the first attempt took, so a 502 arriving after it committed no
    longer costs a second hold.
    """
    kwargs: Dict[str, Any] = {"idempotency_key": str(uuid.uuid4())}
    preflight = _build_preflight(_check_options_to_flag_options(options))
    if preflight is not None:
        kwargs["preflight"] = preflight
    request_options: RequestOptions = {}
    if options.timeout is not None:
        request_options["timeout"] = options.timeout
    kwargs["request_options"] = request_options
    return kwargs


def _is_payment_required(error: Exception) -> bool:
    """Whether an error is the server saying the credits are not there.

    The generated features client has no 402 branch, unlike the credits one, so
    a real 402 from check-and-reserve arrives as the base ApiError carrying the
    status code rather than as PaymentRequiredError.
    """
    if isinstance(error, PaymentRequiredError):
        return True
    return isinstance(error, ApiError) and error.status_code == 402


def _payment_required_message(error: Exception) -> str:
    """The server's own explanation for a 402, when the body carries one."""
    body = getattr(error, "body", None)
    message = body.get("error") if isinstance(body, dict) else getattr(body, "error", None)
    if isinstance(message, str) and message:
        return message
    return str(error)


def _payment_required_result(flag_key: str, error: Exception) -> CheckResult:
    """A 402 is the server's answer, not a failure to answer: it knows the
    credits are not there. Deny whatever on_acquire_failure says."""
    return CheckResult(
        allowed=False,
        value=False,
        reason=INSUFFICIENT_CREDITS_REASON,
        flag_key=flag_key,
        error=_payment_required_message(error),
    )


def _reservation_check_result(flag_key: str, data: CheckAndReserveFlagResponseData) -> CheckResult:
    """The flag verdict a check-and-reserve response carries, before any hold
    is attached to it."""
    return CheckResult(
        allowed=data.value,
        value=data.value,
        reason=data.reason,
        flag_key=data.flag or flag_key,
        entitlement=data.entitlement,
        flag_id=data.flag_id,
        error=data.error,
    )


def _server_reservation(
    held: FlagCheckReservationResponseData,
    event_subtype: str,
    company: Optional[Dict[str, str]],
    user: Optional[Dict[str, str]],
) -> Reservation:
    """The caller's handle on a hold the server took."""
    return Reservation(
        id=held.id,
        lease_id=held.id,
        mode="server",
        company_id=held.company_id,
        credit_type_id=held.credit_type_id,
        event_subtype=event_subtype,
        quantity_reserved=held.quantity_reserved,
        credits_reserved=held.credits_reserved,
        consumption_rate=held.consumption_rate,
        expires_at=held.expires_at,
        company=company,
        user=user,
    )


def _server_failure_result(
    flag_key: str, options: CheckOptions, reason: str, default_value: bool,
) -> CheckResult:
    """Resolve a check that could not gate. ``fail-closed`` denies;
    ``fail-open`` returns the caller's resolved default, since server mode has
    no local engine to re-run with the balance assumed sufficient."""
    if options.on_acquire_failure == "fail-closed":
        return CheckResult(allowed=False, value=False, reason=reason, flag_key=flag_key, error=reason)
    return CheckResult(
        allowed=default_value,
        value=default_value,
        reason=f"{reason}_fail_open",
        flag_key=flag_key,
        error=reason,
    )


def _missing_event_subtype_result(options: CheckOptions, result: CheckResult) -> CheckResult:
    """Resolve a check whose hold was released because nothing names the event
    the settling track event would carry.

    Fail-open means assume the credits are there, and the server has already
    evaluated the flag and said yes; only the settle is impossible, so its
    verdict stands. Fail-closed denies, as it does for any check it cannot gate.
    """
    reason = "missing_event_subtype"
    if options.on_acquire_failure == "fail-closed":
        return CheckResult(allowed=False, value=False, reason=reason, flag_key=result.flag_key, error=reason)
    result.reservation = None
    result.error = reason
    return result


@dataclass
class TrackOptions:
    """Optional metadata for a track event.

    Fields map directly to the corresponding ``CreateEventRequestBody``
    properties. Omit any field you don't need; the SDK only sends fields
    that are explicitly set.
    """

    # Client-supplied dedupe key. Duplicate events with the same key
    # (scoped to the environment) are dropped server-side for 24 hours.
    idempotency_key: Optional[str] = None
    # Timestamp the event was sent. Required when trusted_client_clock=True.
    sent_at: Optional[dt.datetime] = None
    # When True, use sent_at as the effective event timestamp instead of
    # server receipt time. Requires a secret API key and sent_at.
    trusted_client_clock: Optional[bool] = None
    # Import historical data without affecting billing. Requires a secret
    # API key and trusted_client_clock.
    backfill: Optional[bool] = None


@dataclass
class IdentifyOptions:
    """Optional metadata for an identify event.

    Fields map directly to the corresponding ``CreateEventRequestBody``
    properties. Omit any field you don't need; the SDK only sends fields
    that are explicitly set.
    """

    # Client-supplied dedupe key. Duplicate events with the same key
    # (scoped to the environment) are dropped server-side for 24 hours.
    idempotency_key: Optional[str] = None
    # Credit type IDs to warm leases for once the identify is enqueued, so the
    # session's first check() does not pay the acquire round trip. Honored by
    # AsyncSchematic in client mode; ignored everywhere else.
    prewarm: Optional[List[str]] = None


def _event_options_to_kwargs(
    options: Optional[Union[TrackOptions, IdentifyOptions]],
) -> Dict[str, Any]:
    """Flatten an options dataclass into kwargs for CreateEventRequestBody.

    Only fields that were explicitly set on the dataclass are returned, so
    unset fields don't override CreateEventRequestBody's own defaults and
    don't appear on the wire as explicit nulls.
    """
    if options is None:
        return {}
    kwargs: Dict[str, Any] = {}
    for field in ("idempotency_key", "sent_at", "trusted_client_clock", "backfill"):
        value = getattr(options, field, None)
        if value is not None:
            kwargs[field] = value
    return kwargs


@dataclass
class DataStreamConfig:
    """Configuration for DataStream real-time flag evaluation."""

    cache_ttl: Optional[int] = None
    company_cache: Optional[AsyncCacheProvider[Any]] = None
    company_lookup_cache: Optional[AsyncCacheProvider[str]] = None
    user_cache: Optional[AsyncCacheProvider[Any]] = None
    user_lookup_cache: Optional[AsyncCacheProvider[str]] = None
    flag_cache: Optional[AsyncCacheProvider[Any]] = None
    replicator_mode: bool = False
    replicator_health_url: Optional[str] = None
    replicator_health_check: Optional[int] = None
    # Largest WebSocket message in bytes we accept; leave unset for the default.
    max_message_size: Optional[int] = None


@dataclass
class SchematicConfig:
    base_url: Optional[str] = None
    event_buffer_period: Optional[int] = None
    event_capture_url: Optional[str] = None
    flag_defaults: Optional[Dict[str, bool]] = None
    follow_redirects: Optional[bool] = True
    httpx_client: Optional[httpx.Client] = None
    logger: Optional[logging.Logger] = None
    # Level for the default logger; ignored when `logger` is provided so the
    # consumer's own logger configuration is the source of truth.
    log_level: LogLevel = DEFAULT_LOG_LEVEL
    offline: bool = False
    timeout: Optional[float] = None
    cache_providers: Optional[List[CacheProvider[CheckFlagResponseData]]] = None
    credit_leases: Optional[CreditLeaseConfig] = None


class Schematic(BaseSchematic):
    def __init__(self, api_key: str, config: Optional[SchematicConfig] = None):
        config = config or SchematicConfig()
        httpx_client = OfflineHTTPClient() if config.offline else config.httpx_client

        super().__init__(
            api_key=api_key,
            base_url=config.base_url,
            follow_redirects=config.follow_redirects,
            httpx_client=httpx_client,
            timeout=config.timeout,
        )
        self.event_buffer_period = config.event_buffer_period
        self.logger = config.logger or get_default_logger(level=config.log_level)
        self.flag_defaults = config.flag_defaults or {}
        self.event_capture_client = EventCaptureClient(
            api_key=api_key,
            base_url=config.event_capture_url,
            httpx_client=httpx_client,
            get_headers=self._client_wrapper.get_headers,
        )
        self.event_buffer = EventBuffer(
            event_sender=self.event_capture_client,
            logger=self.logger,
            period=self.event_buffer_period,
        )
        self.flag_check_cache_providers: List[CacheProvider[CheckFlagResponseData]] = (
            config.cache_providers if config.cache_providers is not None
            else [LocalCache[CheckFlagResponseData](DEFAULT_CACHE_SIZE, DEFAULT_CACHE_TTL)]
        )
        self.offline = config.offline
        self._credit_leases = config.credit_leases
        self._reservation_ttl = _resolve_reservation_ttl(self.logger, config.credit_leases)
        if config.credit_leases is not None:
            _warn_credit_lease_config(
                self.logger, config.credit_leases, self.offline, supports_client_mode=False,
            )

        atexit.register(self.shutdown)

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        self.event_buffer.stop()
        self.event_capture_client.close()

    def check_flag(
        self,
        flag_key: str,
        company: Optional[Dict[str, str]] = None,
        user: Optional[Dict[str, str]] = None,
        options: Optional[CheckFlagOptions] = None,
    ) -> bool:
        resp = self.check_flag_with_entitlement(flag_key, company=company, user=user, options=options)
        return resp.value

    def check_flag_with_entitlement(
        self,
        flag_key: str,
        company: Optional[Dict[str, str]] = None,
        user: Optional[Dict[str, str]] = None,
        options: Optional[CheckFlagOptions] = None,
    ) -> CheckFlagResponseData:
        if self.offline:
            return self._default_response(flag_key, options, REASON_OFFLINE)

        return self._check_flag_via_api(flag_key, company, user, options)

    def check_flags(
        self,
        flag_keys: Optional[List[str]] = None,
        company: Optional[Dict[str, str]] = None,
        user: Optional[Dict[str, str]] = None,
        options: Optional[CheckFlagOptions] = None,
    ) -> List[CheckFlagResponseData]:
        if self.offline:
            keys = flag_keys if flag_keys else list(self.flag_defaults.keys())
            return [self._default_response(k, options, REASON_OFFLINE) for k in keys]

        return self._check_flags_via_api(flag_keys, company, user, options)

    def _check_flags_via_api(
        self,
        flag_keys: Optional[List[str]],
        company: Optional[Dict[str, str]],
        user: Optional[Dict[str, str]],
        options: Optional[CheckFlagOptions],
    ) -> List[CheckFlagResponseData]:
        try:
            # Build the evaluation context, omitting empty/None entries so we
            # don't send `null` fields on the wire.
            eval_body: Dict[str, Any] = {}
            if company:
                eval_body["company"] = company
            if user:
                eval_body["user"] = user

            # No specific keys requested — return every flag the API knows
            # about for this company/user context.
            if not flag_keys:
                resp = self.features.check_flags(**eval_body)
                if resp is None or resp.data is None or resp.data.flags is None:
                    return []
                flags = list(resp.data.flags)
                for f in flags:
                    if f.flag:
                        self._safe_cache_set(_build_cache_key(f.flag, company, user), f)
                return flags

            # Cache lookup pass
            cached_results: Dict[str, CheckFlagResponseData] = {}
            for flag_key in flag_keys:
                cached = self._safe_cache_get(_build_cache_key(flag_key, company, user))
                if cached is not None:
                    cached_results[flag_key] = cached

            if len(cached_results) == len(flag_keys):
                return [cached_results[k] for k in flag_keys]

            # Cache miss for at least one key — fetch all flags for this
            # company/user context in a single bulk API call and refresh cache.
            resp = self.features.check_flags(**eval_body)
            api_by_key: Dict[str, CheckFlagResponseData] = {}
            if resp is not None and resp.data is not None and resp.data.flags is not None:
                for f in resp.data.flags:
                    if f.flag:
                        api_by_key[f.flag] = f
                        self._safe_cache_set(_build_cache_key(f.flag, company, user), f)

            # Once we've called the API, it's the source of truth: any key
            # that's no longer in the response is treated as deleted, even if
            # we still have a stale cached value for it.
            return [
                api_by_key[k] if k in api_by_key
                else self._default_response(k, options, REASON_FLAG_NOT_FOUND)
                for k in flag_keys
            ]
        except Exception as e:
            self.logger.error(e)
            reason = f"{REASON_ERROR}: {e}"
            return [self._default_response(k, options, reason) for k in (flag_keys or [])]

    def _default_response(
        self, flag_key: str, options: Optional[CheckFlagOptions], reason: str,
    ) -> CheckFlagResponseData:
        return CheckFlagResponseData(
            flag=flag_key,
            reason=reason,
            value=self._resolve_default(flag_key, options),
        )

    def _safe_cache_get(self, cache_key: str) -> Optional[CheckFlagResponseData]:
        """Try each cache provider in order; treat any provider error as a miss.

        Cache provider failures (e.g. Redis connection refused) must not poison
        the flag check — we log a warning and fall through to the next provider
        (or to the API).
        """
        for provider in self.flag_check_cache_providers:
            try:
                cached = provider.get(cache_key)
            except Exception as e:
                self.logger.warning(f"Cache provider get failed for {cache_key}: {e}")
                continue
            if cached is not None:
                return cached
        return None

    def _safe_cache_set(self, cache_key: str, value: CheckFlagResponseData) -> None:
        """Write to every cache provider; log but never propagate failures."""
        for provider in self.flag_check_cache_providers:
            try:
                provider.set(cache_key, value)
            except Exception as e:
                self.logger.warning(f"Cache provider set failed for {cache_key}: {e}")

    def _check_flag_via_api(
        self,
        flag_key: str,
        company: Optional[Dict[str, str]],
        user: Optional[Dict[str, str]],
        options: Optional[CheckFlagOptions] = None,
    ) -> CheckFlagResponseData:
        try:
            preflight = _build_preflight(options)
            cache_key = _build_cache_key(flag_key, company, user)

            # The cache is keyed by flag, company and user, and a preflighted
            # check asks a different question ("would this action be allowed?")
            # than the plain one, so it can neither be answered from the cache
            # nor written to it.
            if preflight is None:
                cached_value = self._safe_cache_get(cache_key)
                if cached_value is not None:
                    return cached_value

            preflight_kwargs: Dict[str, Any] = {} if preflight is None else {"preflight": preflight}
            resp = self.features.check_flag(flag_key, company=company, user=user, **preflight_kwargs)
            if resp is None or resp.data is None or resp.data.value is None:
                return self._default_response(flag_key, options, REASON_FLAG_NOT_FOUND)

            if preflight is None:
                self._safe_cache_set(cache_key, resp.data)

            return resp.data
        except Exception as e:
            self.logger.error(e)
            return self._default_response(flag_key, options, f"{REASON_ERROR}: {e}")

    def _effective_lease_mode(self) -> Optional[Literal["client", "server"]]:
        """Which mode a check with usage resolves to on this client.

        None means no credit gating at all. Client mode rides on DataStream,
        which this SDK offers on AsyncSchematic alone, so it resolves to
        nothing here and the check stays plain.
        """
        if self._credit_leases is None or self.offline:
            return None
        if self._credit_leases.mode == "client":
            return None
        return "server"

    def check(
        self,
        flag_key: str,
        company: Optional[Dict[str, str]] = None,
        user: Optional[Dict[str, str]] = None,
        options: Optional[CheckOptions] = None,
    ) -> CheckResult:
        """Credit-aware feature check.

        When ``credit_leases`` is configured and the caller passes ``usage``,
        this gates the check on the company's credit balance and returns a
        reservation handle on success; pass that handle to
        ``track_with_reservation`` when the work completes.

        Without either it falls through to a plain flag check and returns
        ``allowed = value`` with no reservation. The caller's preflight
        (``usage`` / ``event_subtype``) is still threaded through that plain
        check, so the verdict accounts for the usage about to be recorded, just
        without holding anything.
        """
        mode = self._effective_lease_mode()
        if options is None or options.usage is None or mode is None:
            return self._check_fallback(flag_key, company, user, options)
        if mode == "server":
            return self._check_with_server_reservation(flag_key, company, user, options)
        return self._check_fallback(flag_key, company, user, options)

    def _check_fallback(
        self,
        flag_key: str,
        company: Optional[Dict[str, str]],
        user: Optional[Dict[str, str]],
        options: Optional[CheckOptions],
    ) -> CheckResult:
        resp = self.check_flag_with_entitlement(
            flag_key, company=company, user=user, options=_check_options_to_flag_options(options),
        )
        return CheckResult(
            allowed=resp.value,
            value=resp.value,
            reason=resp.reason,
            flag_key=resp.flag or flag_key,
            entitlement=resp.entitlement,
            flag_id=resp.flag_id,
            error=resp.error,
        )

    def _check_with_server_reservation(
        self,
        flag_key: str,
        company: Optional[Dict[str, str]],
        user: Optional[Dict[str, str]],
        options: CheckOptions,
    ) -> CheckResult:
        """Gate one check on the server: a single check-and-reserve call
        evaluates the flag against the company's real balance and takes the
        hold in the same round trip.

        ``fail-open`` here returns the caller's default rather than re-running
        the rules with an assumed-sufficient balance, since the call that would
        have answered is the one that failed and there is no local engine to
        fall back on. No flag_check event is enqueued: the server logs the
        check, the same way the plain REST path does.
        """
        def failure(reason: str) -> CheckResult:
            return _server_failure_result(
                flag_key, options, reason, self._resolve_default(flag_key, _check_options_to_flag_options(options)),
            )

        if not _is_valid_quantity(options.usage):
            self.logger.error(
                f"Server reservation: invalid usage {options.usage!r} for flag {flag_key}; "
                "must be a finite, non-negative number"
            )
            return failure("invalid_usage")

        if options.usage == 0:
            self.logger.debug(
                f"Server reservation: usage is 0 for flag {flag_key}, nothing to hold, using a plain check"
            )
            return self._check_fallback(flag_key, company, user, options)

        try:
            resp = self.features.check_and_reserve_flag(
                flag_key,
                company=company,
                user=user,
                quantity=options.usage,
                expires_at=dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=self._reservation_ttl),
                **_reservation_request_kwargs(options),
            )
            data = resp.data
        except Exception as e:
            if _is_payment_required(e):
                return _payment_required_result(flag_key, e)
            self.logger.error(f"Server reservation: check-and-reserve for flag {flag_key} failed: {e}")
            return failure("server_reservation_failed")

        result = _reservation_check_result(flag_key, data)

        # No hold comes back when the flag denied, the credits were short, or
        # the feature is not credit-metered. Nothing to release either way.
        held = data.reservation
        if not data.value or held is None:
            return result

        # The settling track event is named by the event subtype; the caller's
        # wins, otherwise the server names it on the hold. With neither, the
        # hold could never be settled, so release it now instead of parking
        # the credits until the TTL.
        event_subtype = options.event_subtype or held.event_subtype
        if not event_subtype:
            self.logger.error(
                f"Server reservation: reservation {held.id} for flag {flag_key} names no event subtype; "
                "releasing it, since it could never be settled"
            )
            try:
                self.credits.release_credit_reservation(held.id)
            except Exception as e:
                self.logger.warning(
                    f"Server reservation: failed to release {held.id} ({e}); its hold is refunded when it expires"
                )
            return _missing_event_subtype_result(options, result)

        result.reservation = _server_reservation(held, event_subtype, company, user)
        return result

    def identify(
        self,
        keys: Dict[str, str],
        company: Optional[EventBodyIdentifyCompany] = None,
        name: Optional[str] = None,
        traits: Optional[Dict[str, Any]] = None,
        options: Optional[IdentifyOptions] = None,
    ) -> None:
        self._enqueue_event(
            "identify",
            EventBodyIdentify(
                company=company,
                keys=keys,
                name=name,
                traits=traits,
            ),
            options=options,
        )

    def track(
        self,
        event: str,
        company: Optional[Dict[str, str]] = None,
        user: Optional[Dict[str, str]] = None,
        traits: Optional[Dict[str, Any]] = None,
        quantity: Optional[int] = None,
        options: Optional[TrackOptions] = None,
    ) -> None:
        self._enqueue_event(
            "track",
            EventBodyTrack(
                company=company,
                event=event,
                quantity=quantity,
                traits=traits,
                user=user,
            ),
            options=options,
        )

    def track_with_reservation(
        self,
        reservation: Optional[Reservation],
        actual_quantity: float,
        options: Optional[TrackWithReservationOptions] = None,
    ) -> None:
        """Settle a reservation issued by ``check`` with the actual usage.

        The track event carries the reservation ID, and the server settles the
        hold, refunding the unspent slice, when it processes the event. The
        event's idempotency key is derived from the reservation ID, so a
        duplicate or retried settle is dropped server-side rather than billed
        twice.
        """
        if self.offline:
            return
        # A check can allow without taking a hold, so a caller that settles
        # whatever check() handed back can land here with nothing to settle.
        # The usage still has to be recorded, but only a plain track() can.
        if reservation is None:
            self.logger.error(
                "track_with_reservation: no reservation to settle; the check allowed without taking a hold. "
                "Report the usage with track() instead"
            )
            return
        # A quantity the server cannot bill must reach neither the event nor
        # the hold: skip the settle and let the hold refund itself at its TTL.
        if not _is_valid_quantity(actual_quantity):
            self.logger.error(
                f"track_with_reservation: invalid actual_quantity {actual_quantity!r} for reservation "
                f"{reservation.id}; must be a finite, non-negative number. Skipping the settle, the hold is "
                "refunded at its TTL"
            )
            return
        self._enqueue_event(
            "track",
            _build_reservation_track_event(reservation, _settled_quantity(actual_quantity), options),
            options=TrackOptions(idempotency_key=f"{RESERVATION_TRACK_IDEMPOTENCY_PREFIX}{reservation.id}"),
        )

    def _enqueue_event(
        self,
        event_type: str,
        body: EventBody,
        options: Optional[Union[TrackOptions, IdentifyOptions]] = None,
    ) -> None:
        if self.offline:
            return
        try:
            event_body = CreateEventRequestBody(
                event_type=event_type,
                body=body,
                **_event_options_to_kwargs(options),
            )
            self.event_buffer.push(event_body)
        except Exception as e:
            self.logger.error(e)

    def _get_flag_default(self, flag_key: str) -> bool:
        return self.flag_defaults.get(flag_key, False)

    def set_flag_default(self, flag_key: str, value: bool) -> None:
        self.flag_defaults[flag_key] = value

    def set_flag_defaults(self, values: Dict[str, bool]) -> None:
        self.flag_defaults.update(values)

    def _resolve_default(self, flag_key: str, options: Optional[CheckFlagOptions] = None) -> bool:
        if options and options.default_value is not None:
            if callable(options.default_value):
                return options.default_value()
            return options.default_value
        return self._get_flag_default(flag_key)


@dataclass
class AsyncSchematicConfig:
    base_url: Optional[str] = None
    event_buffer_period: Optional[int] = None
    event_capture_url: Optional[str] = None
    flag_defaults: Optional[Dict[str, bool]] = None
    follow_redirects: Optional[bool] = True
    httpx_client: Optional[httpx.AsyncClient] = None
    logger: Optional[logging.Logger] = None
    # Level for the default logger; ignored when `logger` is provided so the
    # consumer's own logger configuration is the source of truth.
    log_level: LogLevel = DEFAULT_LOG_LEVEL
    offline: bool = False
    timeout: Optional[float] = None
    cache_providers: Optional[List[CacheProvider[CheckFlagResponseData]]] = None
    use_datastream: bool = False
    datastream: Optional[DataStreamConfig] = None
    credit_leases: Optional[CreditLeaseConfig] = None


class AsyncSchematic(AsyncBaseSchematic):
    """Async Schematic client for feature flags and event tracking.

    This client provides async methods for checking feature flags and tracking events.
    It automatically initializes on first use and maintains background tasks for
    event buffering that require proper cleanup.

    IMPORTANT: Always call shutdown() when done, or use as a context manager:

    # Recommended patterns:

    # 1. Context manager (automatic cleanup):
    async with AsyncSchematic(api_key, config) as client:
        result = await client.check_flag("my-flag")  # Auto-initializes

    # 2. Manual (explicit cleanup):
    client = AsyncSchematic(api_key, config)
    try:
        result = await client.check_flag("my-flag")  # Auto-initializes
    finally:
        await client.shutdown()  # REQUIRED for proper cleanup

    # 3. Web framework (lifecycle managed):
    # In startup: client = AsyncSchematic(api_key, config)
    # In shutdown: await client.shutdown()
    """

    def __init__(self, api_key: str, config: Optional[AsyncSchematicConfig] = None):
        self._initialized = False
        config = config or AsyncSchematicConfig()
        httpx_client = (
            AsyncOfflineHTTPClient() if config.offline else config.httpx_client
        )

        super().__init__(
            api_key=api_key,
            base_url=config.base_url,
            follow_redirects=config.follow_redirects,
            httpx_client=httpx_client,
            timeout=config.timeout,
        )
        self.event_buffer_period = config.event_buffer_period
        self.logger = config.logger or get_default_logger(level=config.log_level)
        self.flag_defaults = config.flag_defaults or {}
        self.event_capture_client = AsyncEventCaptureClient(
            api_key=api_key,
            base_url=config.event_capture_url,
            httpx_client=httpx_client,
            get_headers=self._client_wrapper.get_headers,
        )
        self.event_buffer = AsyncEventBuffer(
            event_sender=self.event_capture_client,
            logger=self.logger,
            period=self.event_buffer_period,
        )
        self.flag_check_cache_providers: List[CacheProvider[CheckFlagResponseData]] = (
            config.cache_providers if config.cache_providers is not None
            else [LocalCache[CheckFlagResponseData](DEFAULT_CACHE_SIZE, DEFAULT_CACHE_TTL)]
        )
        self.offline = config.offline
        self._shutdown_requested = False
        self._is_shutting_down = False
        self._credit_leases = config.credit_leases
        self._reservation_ttl = _resolve_reservation_ttl(self.logger, config.credit_leases)
        # Client-mode plumbing, built below once DataStream is wired so that
        # "auto" can resolve against it. Server mode builds none of it.
        self._lease_store: Optional[LeaseStore] = None
        self._reservations: Optional[ReservationStore] = None
        self._lease_manager: Optional[LeaseManager] = None
        self._lease_backend_shared = False
        self._prewarm_resolve_timeout = DEFAULT_PREWARM_RESOLVE_TIMEOUT
        self._background_tasks: set = set()

        # DataStream client
        self._datastream_client: Optional[DataStreamClient] = None
        if config.use_datastream and not config.offline:
            ds = config.datastream or DataStreamConfig()
            ds_opts = DataStreamClientOptions(
                api_key=api_key,
                base_url=config.base_url,
                logger=self.logger,
            )
            if ds.cache_ttl is not None:
                ds_opts.cache_ttl = ds.cache_ttl
            if ds.company_cache is not None:
                ds_opts.company_cache = ds.company_cache
            if ds.company_lookup_cache is not None:
                ds_opts.company_lookup_cache = ds.company_lookup_cache
            if ds.user_cache is not None:
                ds_opts.user_cache = ds.user_cache
            if ds.user_lookup_cache is not None:
                ds_opts.user_lookup_cache = ds.user_lookup_cache
            if ds.flag_cache is not None:
                ds_opts.flag_cache = ds.flag_cache
            ds_opts.replicator_mode = ds.replicator_mode
            if ds.replicator_health_url is not None:
                ds_opts.replicator_health_url = ds.replicator_health_url
            if ds.replicator_health_check is not None:
                ds_opts.replicator_health_check = ds.replicator_health_check
            if ds.max_message_size is not None:
                ds_opts.max_message_size = ds.max_message_size

            self._datastream_client = DataStreamClient(ds_opts)

        if config.credit_leases is not None:
            _warn_credit_lease_config(
                self.logger,
                config.credit_leases,
                self.offline,
                supports_client_mode=True,
                datastream_enabled=self._datastream_client is not None,
            )
            if not self.offline and _mode_uses_leases(
                config.credit_leases.mode, self._datastream_client is not None
            ):
                self._build_lease_plumbing(config.credit_leases, config.datastream)

        self._initialized = True

    async def __aenter__(self):
        await self._start_datastream()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.shutdown()

    def _build_lease_plumbing(
        self, credit_leases: CreditLeaseConfig, datastream: Optional[DataStreamConfig],
    ) -> None:
        """Build the lease store, the reservation table, and their manager.

        Lease state belongs in a shared cache so gating holds across pods. An
        explicit redis_client wins; otherwise the DataStream company cache's
        Redis is reused, so an existing setup backs leases with no second
        client to wire up.
        """
        redis_client = credit_leases.redis_client
        key_prefix = credit_leases.redis_key_prefix
        company_cache = datastream.company_cache if datastream is not None else None
        if redis_client is None and isinstance(company_cache, RedisCache):
            redis_client = company_cache.client
            if key_prefix is None:
                # RedisCache joins its prefix to a key with a colon, so lease
                # keys land in the same namespace as the cached entities.
                key_prefix = f"{company_cache.prefix}:"
            self.logger.debug(
                "credit_leases: reusing the DataStream cache's Redis client for lease and reservation state"
            )
        prefix = key_prefix or DEFAULT_LEASE_KEY_PREFIX
        if redis_client is not None:
            self._lease_backend_shared = True
            self._lease_store = RedisLeaseStore(
                redis_client,
                key_prefix=prefix,
                default_lease_duration=credit_leases.default_lease_duration or DEFAULT_LEASE_DURATION,
            )
            self._reservations = RedisReservationStore(redis_client, self._lease_store, key_prefix=prefix)
        else:
            self.logger.warning(
                "credit_leases is enabled without a shared Redis backend, so lease and reservation state stays "
                "per-process and gating holds within this process only. Set credit_leases.redis_client (or give "
                "datastream.company_cache a RedisCache) so leases gate across every SDK instance."
            )
            self._lease_store = InMemoryLeaseStore()
            self._reservations = InMemoryReservationStore(self._lease_store)
        self._lease_manager = LeaseManager(
            CreditsWireClient(self.credits),
            self._lease_store,
            reservation_store=self._reservations,
            config=LeaseConfig(
                lease_duration=credit_leases.default_lease_duration,
                reservation_ttl=credit_leases.default_reservation_ttl,
                lease_size=credit_leases.default_lease_size,
                low_water_mark=credit_leases.low_water_mark,
                sweep_interval=credit_leases.sweep_interval,
                overrides=credit_leases.overrides or {},
            ),
        )
        if credit_leases.prewarm_resolve_timeout is not None:
            self._prewarm_resolve_timeout = credit_leases.prewarm_resolve_timeout

    async def _start_datastream(self) -> None:
        if self._datastream_client is not None:
            try:
                await self._datastream_client.start()
            except Exception as e:
                self.logger.error(f"Failed to start DataStream client: {e}")
                self._datastream_client = None
                return
            # The sweeper needs a running loop, and it has nothing to sweep
            # until checks can reserve, which is once DataStream is up.
            if self._lease_manager is not None:
                self._lease_manager.start_sweep()

    async def initialize(self) -> None:
        await self._start_datastream()

    def _get_datastream(self) -> Optional[DataStreamClient]:
        return self._datastream_client

    async def check_flag(
        self,
        flag_key: str,
        company: Optional[Dict[str, str]] = None,
        user: Optional[Dict[str, str]] = None,
        options: Optional[CheckFlagOptions] = None,
    ) -> bool:
        resp = await self.check_flag_with_entitlement(flag_key, company=company, user=user, options=options)
        return resp.value

    async def check_flag_with_entitlement(
        self,
        flag_key: str,
        company: Optional[Dict[str, str]] = None,
        user: Optional[Dict[str, str]] = None,
        options: Optional[CheckFlagOptions] = None,
    ) -> CheckFlagResponseData:
        if self.offline:
            return self._default_response(flag_key, options, REASON_OFFLINE)

        # Try DataStream first if available
        ds = self._get_datastream()
        if ds is not None:
            try:
                resp = await ds.check_flag(
                    CheckFlagRequestBody(company=company, user=user),
                    flag_key,
                    options=options,
                )
                await self._enqueue_flag_check_event(flag_key, resp, company, user)
                return self._ds_result_to_response(flag_key, resp, options)
            except Exception as e:
                self.logger.warning(f"Datastream flag check failed ({e}), falling back to API")

        return await self._check_flag_via_api(flag_key, company, user, options)

    async def check_flags(
        self,
        flag_keys: Optional[List[str]] = None,
        company: Optional[Dict[str, str]] = None,
        user: Optional[Dict[str, str]] = None,
        options: Optional[CheckFlagOptions] = None,
    ) -> List[CheckFlagResponseData]:
        if self.offline:
            keys = flag_keys if flag_keys else list(self.flag_defaults.keys())
            return [self._default_response(k, options, REASON_OFFLINE) for k in keys]

        # DataStream evaluation only makes sense when specific keys are
        # requested AND the client is connected — the "give me everything"
        # semantic only exists via the bulk API.
        ds = self._get_datastream()
        if ds is not None and ds.is_connected() and flag_keys:
            try:
                results: List[CheckFlagResponseData] = []
                for flag_key in flag_keys:
                    resp = await ds.check_flag(
                        CheckFlagRequestBody(company=company, user=user),
                        flag_key,
                    )
                    results.append(self._ds_result_to_response(flag_key, resp, options))
                return results
            except Exception as e:
                self.logger.warning(f"Datastream check_flags failed ({e}), falling back to bulk API")

        return await self._check_flags_via_api(flag_keys, company, user, options)

    async def _check_flags_via_api(
        self,
        flag_keys: Optional[List[str]],
        company: Optional[Dict[str, str]],
        user: Optional[Dict[str, str]],
        options: Optional[CheckFlagOptions],
    ) -> List[CheckFlagResponseData]:
        try:
            # Build the evaluation context, omitting empty/None entries so we
            # don't send `null` fields on the wire.
            eval_body: Dict[str, Any] = {}
            if company:
                eval_body["company"] = company
            if user:
                eval_body["user"] = user

            # No specific keys requested — return every flag the API knows
            # about for this company/user context.
            if not flag_keys:
                resp = await self.features.check_flags(**eval_body)
                if resp is None or resp.data is None or resp.data.flags is None:
                    return []
                flags = list(resp.data.flags)
                for f in flags:
                    if f.flag:
                        self._safe_cache_set(_build_cache_key(f.flag, company, user), f)
                return flags

            cached_results: Dict[str, CheckFlagResponseData] = {}
            for flag_key in flag_keys:
                cached = self._safe_cache_get(_build_cache_key(flag_key, company, user))
                if cached is not None:
                    cached_results[flag_key] = cached

            if len(cached_results) == len(flag_keys):
                return [cached_results[k] for k in flag_keys]

            resp = await self.features.check_flags(**eval_body)
            api_by_key: Dict[str, CheckFlagResponseData] = {}
            if resp is not None and resp.data is not None and resp.data.flags is not None:
                for f in resp.data.flags:
                    if f.flag:
                        api_by_key[f.flag] = f
                        self._safe_cache_set(_build_cache_key(f.flag, company, user), f)

            # Once we've called the API, it's the source of truth: any key
            # that's no longer in the response is treated as deleted, even if
            # we still have a stale cached value for it.
            return [
                api_by_key[k] if k in api_by_key
                else self._default_response(k, options, REASON_FLAG_NOT_FOUND)
                for k in flag_keys
            ]
        except Exception as e:
            self.logger.error(e)
            reason = f"{REASON_ERROR}: {e}"
            return [self._default_response(k, options, reason) for k in (flag_keys or [])]

    def _default_response(
        self, flag_key: str, options: Optional[CheckFlagOptions], reason: str,
    ) -> CheckFlagResponseData:
        return CheckFlagResponseData(
            flag=flag_key,
            reason=reason,
            value=self._resolve_default(flag_key, options),
        )

    def _safe_cache_get(self, cache_key: str) -> Optional[CheckFlagResponseData]:
        """Try each cache provider in order; treat any provider error as a miss.

        Cache provider failures (e.g. Redis connection refused) must not poison
        the flag check — we log a warning and fall through to the next provider
        (or to the API).
        """
        for provider in self.flag_check_cache_providers:
            try:
                cached = provider.get(cache_key)
            except Exception as e:
                self.logger.warning(f"Cache provider get failed for {cache_key}: {e}")
                continue
            if cached is not None:
                return cached
        return None

    def _safe_cache_set(self, cache_key: str, value: CheckFlagResponseData) -> None:
        """Write to every cache provider; log but never propagate failures."""
        for provider in self.flag_check_cache_providers:
            try:
                provider.set(cache_key, value)
            except Exception as e:
                self.logger.warning(f"Cache provider set failed for {cache_key}: {e}")

    async def _enqueue_flag_check_event(
        self,
        flag_key: str,
        resp: RulesengineCheckFlagResult,
        company: Optional[Dict[str, str]],
        user: Optional[Dict[str, str]],
    ) -> None:
        """Enqueue a flag_check event for a DataStream-evaluated flag."""
        await self._enqueue_event(
            "flag_check",
            EventBodyFlagCheck(
                flag_key=flag_key,
                value=resp.value if resp.value is not None else False,
                reason=resp.reason if resp.reason else "unknown",
                rule_id=resp.rule_id,
                company_id=resp.company_id,
                user_id=resp.user_id,
                flag_id=resp.flag_id,
                req_company=company,
                req_user=user,
            ),
        )

    def _ds_result_to_response(
        self,
        flag_key: str,
        resp: RulesengineCheckFlagResult,
        options: Optional[CheckFlagOptions],
    ) -> CheckFlagResponseData:
        """Convert a RulesengineCheckFlagResult (from DataStream) into the
        public CheckFlagResponseData shape."""
        entitlement = (
            FeatureEntitlement.model_validate(resp.entitlement.model_dump())
            if resp.entitlement is not None else None
        )
        return CheckFlagResponseData(
            company_id=resp.company_id,
            entitlement=entitlement,
            error=resp.err,
            flag=resp.flag_key,
            flag_id=resp.flag_id,
            reason=resp.reason,
            rule_id=resp.rule_id,
            rule_type=resp.rule_type,
            user_id=resp.user_id,
            value=resp.value if resp.value is not None else self._resolve_default(flag_key, options),
        )

    async def _check_flag_via_api(
        self,
        flag_key: str,
        company: Optional[Dict[str, str]],
        user: Optional[Dict[str, str]],
        options: Optional[CheckFlagOptions] = None,
    ) -> CheckFlagResponseData:
        try:
            preflight = _build_preflight(options)
            cache_key = _build_cache_key(flag_key, company, user)

            # The cache is keyed by flag, company and user, and a preflighted
            # check asks a different question ("would this action be allowed?")
            # than the plain one, so it can neither be answered from the cache
            # nor written to it.
            if preflight is None:
                cached_value = self._safe_cache_get(cache_key)
                if cached_value is not None:
                    return cached_value

            preflight_kwargs: Dict[str, Any] = {} if preflight is None else {"preflight": preflight}
            resp = await self.features.check_flag(flag_key, company=company, user=user, **preflight_kwargs)
            if resp is None or resp.data is None or resp.data.value is None:
                return self._default_response(flag_key, options, REASON_FLAG_NOT_FOUND)

            if preflight is None:
                self._safe_cache_set(cache_key, resp.data)

            return resp.data
        except Exception as e:
            self.logger.error(e)
            return self._default_response(flag_key, options, f"{REASON_ERROR}: {e}")

    def _effective_lease_mode(self) -> Optional[Literal["client", "server"]]:
        """Which mode a check with usage resolves to right now.

        None means no credit gating at all. "auto" resolves per check rather
        than once at construction, so a DataStream whose start() failed, which
        clears the client, falls to server mode instead of leaving every check
        ungated.
        """
        if self._credit_leases is None or self.offline:
            return None
        mode = self._credit_leases.mode
        if mode == "server":
            return "server"
        plumbing_ready = (
            self._lease_manager is not None and self._lease_store is not None and self._reservations is not None
        )
        if mode == "client":
            return "client" if plumbing_ready else None
        return "client" if self._datastream_client is not None and plumbing_ready else "server"

    async def check(
        self,
        flag_key: str,
        company: Optional[Dict[str, str]] = None,
        user: Optional[Dict[str, str]] = None,
        options: Optional[CheckOptions] = None,
    ) -> CheckResult:
        """Credit-aware feature check.

        When ``credit_leases`` is configured and the caller passes ``usage``,
        this gates the check on the company's credit balance and returns a
        reservation handle on success; pass that handle to
        ``track_with_reservation`` when the work completes.

        Without either it falls through to a plain flag check and returns
        ``allowed = value`` with no reservation. The caller's preflight
        (``usage`` / ``event_subtype``) is still threaded through that plain
        check, so the verdict accounts for the usage about to be recorded, just
        without holding anything.
        """
        mode = self._effective_lease_mode()
        if options is None or options.usage is None or mode is None:
            return await self._check_fallback(flag_key, company, user, options)
        if mode == "server":
            return await self._check_with_server_reservation(flag_key, company, user, options)
        return await self._check_with_lease(flag_key, company, user, options)

    async def _check_with_lease(
        self,
        flag_key: str,
        company: Optional[Dict[str, str]],
        user: Optional[Dict[str, str]],
        options: CheckOptions,
    ) -> CheckResult:
        """Gate one check on a hold carved out of a local credit lease."""
        lease_store, reservations, manager = self._lease_store, self._reservations, self._lease_manager
        if lease_store is None or reservations is None or manager is None:
            return await self._check_fallback(flag_key, company, user, options)

        async def fallback() -> CheckResult:
            return await self._check_fallback(flag_key, company, user, options)

        async def enqueue_flag_check(body: EventBodyFlagCheck) -> None:
            await self._enqueue_event("flag_check", body)

        return await check_with_lease(
            CreditCheckDeps(
                datastream=self._datastream_client,
                lease_store=lease_store,
                reservations=reservations,
                manager=manager,
                logger=self.logger,
                enqueue_flag_check=enqueue_flag_check,
            ),
            flag_key,
            company,
            user,
            options,
            fallback,
        )

    async def prewarm(self, company: Dict[str, str], credit_type_ids: List[str]) -> None:
        """Acquire a lease per credit type up front, so a session's first
        check() does not pay the acquire round trip.

        Best effort: failures are logged, never raised. The company keys are
        looked up over DataStream, waiting up to
        ``credit_leases.prewarm_resolve_timeout`` for the company to surface,
        which covers a company the server has only just ingested.
        """
        if self._lease_manager is None:
            self.logger.debug(
                "prewarm is a no-op in server mode; there is no local lease to warm"
                if self._effective_lease_mode() == "server"
                else "prewarm called but client-mode credit leases are not configured"
            )
            return
        if not company:
            self.logger.debug("prewarm needs company keys")
            return
        company_id = await self._resolve_company_id_with_wait(company)
        if not company_id:
            self.logger.debug(
                f"prewarm: company {company} did not resolve within {self._prewarm_resolve_timeout}s; "
                "the first check() acquires instead"
            )
            return
        await asyncio.gather(*(self._prewarm_one(company_id, credit_type_id) for credit_type_id in credit_type_ids))

    async def _prewarm_one(self, company_id: str, credit_type_id: str) -> None:
        manager = self._lease_manager
        if manager is None:
            return
        if self._is_shutting_down:
            # shutdown() only cancels the prewarms it spawned; a caller
            # awaiting prewarm() directly would otherwise install a lease
            # after the release has already listed the store.
            self.logger.debug("prewarm: client is shutting down, skipping acquire")
            return
        try:
            await manager.acquire_if_needed(company_id, credit_type_id)
        except Exception as e:
            self.logger.warning(f"prewarm: failed to acquire a lease for {credit_type_id}: {e}")

    async def _resolve_company_id_with_wait(self, company: Dict[str, str]) -> Optional[str]:
        """Resolve company keys to an ID, waiting for the company to surface.

        Resolved in the server's order: every supplied key/value pair is an
        ordinary entity key and gets looked up first; only when nothing matches
        is a value read as the company's own id, by its ``comp_`` prefix rather
        than by the name of the key it sits under. An account is free to define
        a key called ``id`` holding its own identifier, so the name alone
        settles nothing.

        identify does not push a company into the DataStream cache, since
        companies are only streamed on request, so this fetches (cache first,
        then over the socket) rather than watching an empty cache. The fetch
        also primes the cache, so the first real check() takes the lease path.
        A prewarm_resolve_timeout of 0 keeps the cache lookup and skips the
        wait, so an already-seen company still warms.
        """
        datastream = self._datastream_client
        if datastream is None:
            return _schematic_id(company, COMPANY_ID_PREFIX)
        # An earlier check or prewarm may already have cached this company, and
        # that answer costs nothing.
        try:
            cached = await datastream.get_cached_company(company)
            if cached is not None and cached.id:
                return cached.id
        except Exception as e:
            self.logger.debug(f"prewarm: DataStream company cache lookup failed ({e})")
        if self._prewarm_resolve_timeout <= 0:
            return _schematic_id(company, COMPANY_ID_PREFIX)
        deadline = time.monotonic() + self._prewarm_resolve_timeout
        while True:
            try:
                resolved = await datastream.get_company(company)
                if resolved is not None and resolved.id:
                    return resolved.id
            except Exception as e:
                # Expected while the socket is still connecting, and while the
                # server has yet to ingest a preceding identify.
                self.logger.debug(f"prewarm: DataStream company fetch failed ({e})")
            if time.monotonic() >= deadline:
                # The keys never resolved, so fall back to a comp_ value the
                # way the server does once its own key lookup comes up empty.
                return _schematic_id(company, COMPANY_ID_PREFIX)
            await asyncio.sleep(PREWARM_POLL_INTERVAL)

    async def _check_fallback(
        self,
        flag_key: str,
        company: Optional[Dict[str, str]],
        user: Optional[Dict[str, str]],
        options: Optional[CheckOptions],
    ) -> CheckResult:
        resp = await self.check_flag_with_entitlement(
            flag_key, company=company, user=user, options=_check_options_to_flag_options(options),
        )
        return CheckResult(
            allowed=resp.value,
            value=resp.value,
            reason=resp.reason,
            flag_key=resp.flag or flag_key,
            entitlement=resp.entitlement,
            flag_id=resp.flag_id,
            error=resp.error,
        )

    async def _check_with_server_reservation(
        self,
        flag_key: str,
        company: Optional[Dict[str, str]],
        user: Optional[Dict[str, str]],
        options: CheckOptions,
    ) -> CheckResult:
        """Gate one check on the server: a single check-and-reserve call
        evaluates the flag against the company's real balance and takes the
        hold in the same round trip.

        ``fail-open`` here returns the caller's default rather than re-running
        the rules with an assumed-sufficient balance, since the call that would
        have answered is the one that failed. No flag_check event is enqueued:
        the server logs the check, the same way the plain REST path does.
        """
        def failure(reason: str) -> CheckResult:
            return _server_failure_result(
                flag_key, options, reason, self._resolve_default(flag_key, _check_options_to_flag_options(options)),
            )

        if not _is_valid_quantity(options.usage):
            self.logger.error(
                f"Server reservation: invalid usage {options.usage!r} for flag {flag_key}; "
                "must be a finite, non-negative number"
            )
            return failure("invalid_usage")

        if options.usage == 0:
            self.logger.debug(
                f"Server reservation: usage is 0 for flag {flag_key}, nothing to hold, using a plain check"
            )
            return await self._check_fallback(flag_key, company, user, options)

        try:
            resp = await self.features.check_and_reserve_flag(
                flag_key,
                company=company,
                user=user,
                quantity=options.usage,
                expires_at=dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=self._reservation_ttl),
                **_reservation_request_kwargs(options),
            )
            data = resp.data
        except Exception as e:
            if _is_payment_required(e):
                return _payment_required_result(flag_key, e)
            self.logger.error(f"Server reservation: check-and-reserve for flag {flag_key} failed: {e}")
            return failure("server_reservation_failed")

        result = _reservation_check_result(flag_key, data)

        # No hold comes back when the flag denied, the credits were short, or
        # the feature is not credit-metered. Nothing to release either way.
        held = data.reservation
        if not data.value or held is None:
            return result

        # The settling track event is named by the event subtype; the caller's
        # wins, otherwise the server names it on the hold. With neither, the
        # hold could never be settled, so release it now instead of parking
        # the credits until the TTL.
        event_subtype = options.event_subtype or held.event_subtype
        if not event_subtype:
            self.logger.error(
                f"Server reservation: reservation {held.id} for flag {flag_key} names no event subtype; "
                "releasing it, since it could never be settled"
            )
            try:
                await self.credits.release_credit_reservation(held.id)
            except Exception as e:
                self.logger.warning(
                    f"Server reservation: failed to release {held.id} ({e}); its hold is refunded when it expires"
                )
            return _missing_event_subtype_result(options, result)

        result.reservation = _server_reservation(held, event_subtype, company, user)
        return result

    async def identify(
        self,
        keys: Dict[str, str],
        company: Optional[EventBodyIdentifyCompany] = None,
        name: Optional[str] = None,
        traits: Optional[Dict[str, Any]] = None,
        options: Optional[IdentifyOptions] = None,
    ) -> None:
        await self._enqueue_event(
            "identify",
            EventBodyIdentify(
                company=company,
                keys=keys,
                name=name,
                traits=traits,
            ),
            options=options,
        )
        if options is not None and options.prewarm:
            company_keys = company.keys if company is not None else None
            if company_keys:
                # Push the identify out before warming. Left in the buffer it
                # would wait a whole flush period, and the prewarm's company
                # resolution polls a server that has not seen the company yet.
                try:
                    await self.event_buffer.flush()
                except Exception as e:
                    self.logger.debug(f"identify: flushing before prewarm failed: {e}")
                self._spawn_prewarm(company_keys, options.prewarm)
            else:
                self.logger.debug("identify: prewarm needs company keys on the identify event")

    def _spawn_prewarm(self, company: Dict[str, str], credit_type_ids: List[str]) -> None:
        """Warm the leases behind an identify without making the caller wait."""

        async def run() -> None:
            try:
                await self.prewarm(company, credit_type_ids)
            except Exception as e:
                self.logger.warning(f"identify prewarm failed: {e}")

        try:
            task = asyncio.ensure_future(run())
        except RuntimeError:
            self.logger.debug("identify: no running event loop, skipping prewarm")
            return
        # Held so the loop does not collect the task mid-flight.
        self._background_tasks.add(task)
        task.add_done_callback(self._background_tasks.discard)

    async def track(
        self,
        event: str,
        company: Optional[Dict[str, str]] = None,
        user: Optional[Dict[str, str]] = None,
        traits: Optional[Dict[str, Any]] = None,
        quantity: Optional[int] = None,
        options: Optional[TrackOptions] = None,
    ) -> None:
        await self._enqueue_event(
            "track",
            EventBodyTrack(
                company=company,
                event=event,
                quantity=quantity,
                traits=traits,
                user=user,
            ),
            options=options,
        )

        # Update company metrics in DataStream if available and connected
        await self._update_company_metrics(company, event, quantity)

    async def _update_company_metrics(
        self, company: Optional[Dict[str, str]], event: str, quantity: Optional[int],
    ) -> None:
        ds = self._get_datastream()
        if company and ds is not None and ds.is_connected():
            try:
                await ds.update_company_metrics(
                    company,
                    event,
                    quantity or 1,
                )
            except Exception as e:
                self.logger.error(f"Failed to update company metrics: {e}")

    async def track_with_reservation(
        self,
        reservation: Optional[Reservation],
        actual_quantity: float,
        options: Optional[TrackWithReservationOptions] = None,
    ) -> None:
        """Settle a reservation issued by ``check`` with the actual usage.

        A server-mode hold settles by id: the track event carries it and the
        server refunds the unspent slice when it processes the event. A
        client-mode hold is consumed against its local lease first, and the
        event carries the lease id so the server bills through the lease's
        sub-ledger rather than decrementing the pre-debited grant again.

        Either way the event's idempotency key is derived from the reservation
        ID, so a duplicate or retried settle is dropped server-side rather than
        billed twice.
        """
        if self.offline:
            return
        # A check can allow without taking a hold, so a caller that settles
        # whatever check() handed back can land here with nothing to settle.
        # The usage still has to be recorded, but only a plain track() can.
        if reservation is None:
            self.logger.error(
                "track_with_reservation: no reservation to settle; the check allowed without taking a hold. "
                "Report the usage with track() instead"
            )
            return
        # A quantity the server cannot bill must reach neither the event nor
        # the hold: skip the settle and let the hold refund itself at its TTL.
        if not _is_valid_quantity(actual_quantity):
            self.logger.error(
                f"track_with_reservation: invalid actual_quantity {actual_quantity!r} for reservation "
                f"{reservation.id}; must be a finite, non-negative number. Skipping the settle, the hold is "
                "refunded at its TTL"
            )
            return
        quantity = _settled_quantity(actual_quantity)
        if reservation.mode == "server":
            # Nothing local to consume: the server settles the hold by id, so
            # this event is the one that records the usage.
            event, settled_locally = _build_reservation_track_event(reservation, quantity, options), True
        else:
            event, settled_locally = await self._settle_client_reservation(
                reservation, actual_quantity, quantity, options,
            )
        await self._enqueue_event(
            "track",
            event,
            options=TrackOptions(idempotency_key=f"{RESERVATION_TRACK_IDEMPOTENCY_PREFIX}{reservation.id}"),
        )
        # The settled usage counts toward the company's metrics like any other
        # track event, but the cached metric moves only when this call moved
        # local state with it: the server drops a duplicate event on the
        # idempotency key, so bumping the metric for one would have a caller's
        # retry deny its own next numeric-limit check until the stream pushes
        # the real figure.
        if settled_locally:
            await self._update_company_metrics(reservation.company, reservation.event_subtype, quantity)

    async def _settle_client_reservation(
        self,
        reservation: Reservation,
        actual_quantity: float,
        quantity: int,
        options: Optional[TrackWithReservationOptions],
    ) -> Tuple[EventBodyTrack, bool]:
        """Consume a client-mode hold locally and hand back the event that bills
        it, with whether the hold actually moved.

        The server is the source of truth for real consumption, so a settle
        that cannot run locally still emits: the event's idempotency key keeps
        the retry from billing twice.
        """
        if self._reservations is None:
            # The handle came from a lease-configured client, so the event
            # still needs its lease id and dedupe key even though this client
            # holds nothing to settle. The usage is new all the same, so it
            # counts toward the cached metrics.
            self.logger.warning(
                "track_with_reservation: client-mode credit leases are not configured here, "
                "emitting an unsettled track"
            )
            return _build_reservation_track_event(reservation, quantity, options), True
        try:
            outcome = await consume_reservation_and_build_event(
                self._reservations, reservation, actual_quantity, options,
            )
        except Exception as e:
            self.logger.warning(
                f"track_with_reservation: failed to settle reservation {reservation.id} locally ({e}), "
                "emitting the track anyway"
            )
            return _build_reservation_track_event(reservation, quantity, options), False
        if not outcome.settled_locally:
            self.logger.debug(
                f"track_with_reservation: reservation {reservation.id} was not settled locally (swept at its "
                "TTL, already settled, or the store is unreachable); the track is keyed for server-side dedupe"
            )
        return outcome.track, outcome.settled_locally

    async def _enqueue_event(
        self,
        event_type: str,
        body: EventBody,
        options: Optional[Union[TrackOptions, IdentifyOptions]] = None,
    ) -> None:
        if self.offline:
            return
        try:
            event_body = CreateEventRequestBody(
                event_type=event_type,
                body=body,
                **_event_options_to_kwargs(options),
            )
            await self.event_buffer.push(event_body)
        except Exception as e:
            self.logger.error(e)

    def _get_flag_default(self, flag_key: str) -> bool:
        return self.flag_defaults.get(flag_key, False)

    def set_flag_default(self, flag_key: str, value: bool) -> None:
        self.flag_defaults[flag_key] = value

    def set_flag_defaults(self, values: Dict[str, bool]) -> None:
        self.flag_defaults.update(values)

    def _resolve_default(self, flag_key: str, options: Optional[CheckFlagOptions] = None) -> bool:
        if options and options.default_value is not None:
            if callable(options.default_value):
                return options.default_value()
            return options.default_value
        return self._get_flag_default(flag_key)

    async def shutdown(self) -> None:
        """Properly shutdown the client, flushing any pending events.

        This method should be called when you're done using the client to ensure:
        - All pending events are flushed to the server
        - Background tasks are properly terminated
        - Resources are cleaned up

        It's safe to call this method multiple times, even if the client was never used.
        """
        # Only do the shutdown once
        if self._is_shutting_down:
            self.logger.debug("Shutdown already in progress, skipping")
            return

        self._is_shutting_down = True

        # If we were never initialized, there's nothing to clean up
        if not self._initialized:
            self.logger.debug("Client was never initialized, nothing to clean up")
            return

        self.logger.info("Shutting down AsyncSchematic...")

        try:
            if self._lease_manager is not None:
                self._lease_manager.stop()
                # A prewarm is worthless to a process that is exiting, and
                # waiting out its company-resolve poll would stall shutdown for
                # seconds. Cancel it, then drain what it already put on the
                # wire, so a lease installed mid-shutdown is one
                # release_all_local_leases() can see. Both run for a shared
                # backend too: the work must not outlive the client.
                #
                # One budget across both waits, not each timeout in turn: a
                # caller closing a client wants a bounded shutdown, not the sum
                # of every wait inside it.
                deadline = time.monotonic() + SHUTDOWN_DRAIN_TIMEOUT
                pending = list(self._background_tasks)
                for task in pending:
                    task.cancel()
                if pending:
                    await asyncio.gather(*pending, return_exceptions=True)
                await self._lease_manager.drain(deadline - time.monotonic())
                if not self._lease_backend_shared:
                    # Per-process leases have no sibling drawing on them, so
                    # releasing hands the unspent remainder back to the company
                    # balance now instead of at expiry. A shared lease must
                    # survive this process's shutdown, or the release pulls the
                    # grant out from under the pods still drawing on it.
                    await self._lease_manager.release_all_local_leases(deadline - time.monotonic())
            if self._datastream_client is not None:
                try:
                    await self._datastream_client.close()
                except Exception as e:
                    self.logger.error(f"Error closing DataStream client: {e}")

            # Flush and stop the event buffer
            await self.event_buffer.stop()
            await self.event_capture_client.close()
            self.logger.info("Shutdown complete.")
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
        finally:
            self._shutdown_requested = True


def _build_cache_key(
    flag_key: str,
    company: Optional[Dict[str, str]] = None,
    user: Optional[Dict[str, str]] = None,
) -> str:
    parts = [flag_key]
    if company:
        parts.append("company:" + ";".join(f"{k}={v}" for k, v in sorted(company.items())))
    if user:
        parts.append("user:" + ";".join(f"{k}={v}" for k, v in sorted(user.items())))
    return ":".join(parts)


