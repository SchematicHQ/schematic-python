from __future__ import annotations

import asyncio
import httpx
import logging
import typing

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from ..types.check_flag_request_body import CheckFlagRequestBody
from ..types.rulesengine_check_flag_result import RulesengineCheckFlagResult
from ..types.rulesengine_company import RulesengineCompany
from ..types.rulesengine_flag import RulesengineFlag
from ..types.rulesengine_user import RulesengineUser
from ..cache import AsyncCacheProvider, AsyncLocalCache
from .merge import partial_company, partial_user
from .rules_engine import RulesEngineClient
from .types import DataStreamBaseReq, DataStreamReq, DataStreamResp, EntityType, KeyConflictError, MessageType
from .websocket_client import ClientOptions as WSClientOptions, DatastreamWSClient


_hints_cache: Dict[type, Dict[str, Any]] = {}


def _get_type_hints(model_cls: type) -> Dict[str, Any]:
    """Cached wrapper around typing.get_type_hints to avoid repeated introspection."""
    if model_cls not in _hints_cache:
        _hints_cache[model_cls] = typing.get_type_hints(model_cls)
    return _hints_cache[model_cls]


def _coerce_nulls(data: dict, model_cls: type) -> dict:
    """Convert null values to empty lists for required list fields.

    Go serializes nil slices as JSON null, but our Pydantic models require
    lists. This recursively fixes nulls before model_validate.
    """
    if not hasattr(model_cls, "__annotations__"):
        return data

    hints = _get_type_hints(model_cls)
    result = dict(data)
    for field_name, field_type in hints.items():
        if field_name not in result:
            continue
        origin = getattr(field_type, "__origin__", None)
        args = getattr(field_type, "__args__", ())

        # typing.List[X] — coerce None to []
        if origin is list and result[field_name] is None:
            result[field_name] = []
        # typing.List[Model] — recurse into each element
        elif origin is list and args and isinstance(result[field_name], list):
            inner = args[0]
            if hasattr(inner, "__annotations__"):
                result[field_name] = [
                    _coerce_nulls(item, inner) if isinstance(item, dict) else item
                    for item in result[field_name]
                ]
    return result


def _validate(model_cls: type, raw: Any) -> Any:
    """Validate raw data into a Pydantic model, coercing Go-style nulls first."""
    if isinstance(raw, dict):
        return model_cls.model_validate(_coerce_nulls(raw, model_cls))  # type: ignore[attr-defined]
    return raw


# Cache key prefixes
_PREFIX_COMPANY = "company"
_PREFIX_USER = "user"
_PREFIX_FLAGS = "flags"

# Timing constants (milliseconds)
RESOURCE_TIMEOUT_MS = 2_000  # 2 seconds
DEFAULT_TTL_MS = 24 * 60 * 60 * 1000  # 24 hours
MAX_CACHE_TTL_MS = 30 * 24 * 60 * 60 * 1000  # 30 days
DEFAULT_REPLICATOR_HEALTH_CHECK_MS = 30_000  # 30 seconds
REPLICATOR_HEALTH_TIMEOUT_S = 5.0
REPLICATOR_CACHE_VERSION_TIMEOUT_S = 2.0


@dataclass
class DataStreamClientOptions:
    """Configuration for the DataStream client."""

    api_key: str
    logger: logging.Logger
    base_url: Optional[str] = None
    cache_ttl: Optional[int] = DEFAULT_TTL_MS

    # Custom cache providers (override defaults)
    company_cache: Optional[AsyncCacheProvider[Any]] = None
    company_lookup_cache: Optional[AsyncCacheProvider[str]] = None
    user_cache: Optional[AsyncCacheProvider[Any]] = None
    user_lookup_cache: Optional[AsyncCacheProvider[str]] = None
    flag_cache: Optional[AsyncCacheProvider[Any]] = None

    # Replicator mode
    replicator_mode: bool = False
    replicator_health_url: Optional[str] = "http://localhost:8090/ready"
    replicator_health_check: int = DEFAULT_REPLICATOR_HEALTH_CHECK_MS

    # Event callbacks
    on_connected: Optional[Callable[[], None]] = None
    on_disconnected: Optional[Callable[[], None]] = None
    on_ready: Optional[Callable[[], None]] = None
    on_not_ready: Optional[Callable[[], None]] = None
    on_error: Optional[Callable[[Exception], None]] = None
    on_replicator_health_changed: Optional[Callable[[bool], None]] = None


class DataStreamClient:
    """Datastream client with caching, WASM flag evaluation, and replicator support.

    Manages a WebSocket connection to Schematic's datastream, caches entities
    locally, and evaluates feature flags using the WASM rules engine.

    In **replicator mode** no WebSocket connection is established — the client
    relies entirely on a shared cache populated by an external replicator
    service and performs health checks against a configurable URL.

    Usage::

        client = DataStreamClient(DataStreamClientOptions(
            api_key="your-api-key",
            base_url="https://api.schematichq.com",
            logger=logging.getLogger(__name__),
        ))
        await client.start()
        result = await client.check_flag(CheckFlagRequestBody(company={"id": "co_123"}), "premium-feature")
        await client.close()
    """

    def __init__(self, options: DataStreamClientOptions) -> None:
        self._api_key = options.api_key
        self._base_url = options.base_url
        self._logger = options.logger
        self._cache_ttl = options.cache_ttl

        # Callbacks
        self._on_connected = options.on_connected
        self._on_disconnected = options.on_disconnected
        self._on_ready = options.on_ready
        self._on_not_ready = options.on_not_ready
        self._on_error = options.on_error
        self._on_replicator_health_changed = options.on_replicator_health_changed

        # Replicator mode
        self._replicator_mode = options.replicator_mode
        self._replicator_health_url = options.replicator_health_url
        self._replicator_health_check_ms = options.replicator_health_check
        self._health_check_client: Optional[httpx.AsyncClient] = None
        self._replicator_ready = False
        self._replicator_health_task: Optional[asyncio.Task[None]] = None
        self._replicator_cache_version: Optional[str] = None

        if self._replicator_mode:
            caches = [
                options.company_cache, options.company_lookup_cache,
                options.user_cache, options.user_lookup_cache,
                options.flag_cache,
            ]
            if not all(caches):
                raise ValueError(
                    "Replicator mode requires custom cache providers for company, company_lookup, "
                    "user, user_lookup, and flag caches"
                )
            for c in caches:
                if isinstance(c, AsyncLocalCache):
                    raise TypeError(
                        "Replicator mode requires shared cache providers (e.g. RedisCache), "
                        "not AsyncLocalCache, to ensure shared state across processes"
                    )

        # Cache providers
        local_ttl = self._cache_ttl if self._cache_ttl is not None else DEFAULT_TTL_MS
        flag_ttl = max(MAX_CACHE_TTL_MS, local_ttl)
        self._company_cache: AsyncCacheProvider[RulesengineCompany] = options.company_cache or AsyncLocalCache(ttl=local_ttl)
        self._user_cache: AsyncCacheProvider[RulesengineUser] = options.user_cache or AsyncLocalCache(ttl=local_ttl)
        self._flag_cache: AsyncCacheProvider[RulesengineFlag] = options.flag_cache or AsyncLocalCache(ttl=flag_ttl)

        # Key -> ID mapping caches (two-level caching)
        self._company_key_cache: AsyncCacheProvider[str] = options.company_lookup_cache or AsyncLocalCache(ttl=local_ttl)
        self._user_key_cache: AsyncCacheProvider[str] = options.user_lookup_cache or AsyncLocalCache(ttl=local_ttl)

        # WebSocket client
        self._ws_client: Optional[DatastreamWSClient] = None

        # Rules engine
        self._rules_engine = RulesEngineClient()

        # Pending requests — maps cache key to list of asyncio Futures
        self._pending_company: Dict[str, List[asyncio.Future[RulesengineCompany]]] = {}
        self._pending_user: Dict[str, List[asyncio.Future[RulesengineUser]]] = {}
        self._pending_flags: Optional[asyncio.Future[bool]] = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def start(self) -> None:
        """Initialise and start the datastream client."""
        # Initialise the rules engine
        try:
            await self._rules_engine.initialize()
            self._logger.debug("Rules engine initialized successfully")
        except Exception as exc:
            self._logger.warning("Failed to initialize rules engine: %s", exc)

        # Replicator mode — no WebSocket
        if self._replicator_mode:
            self._logger.info("Replicator mode enabled — skipping WebSocket connection")
            if self._replicator_health_url:
                # Run an initial health check synchronously so the cache version
                # is available before the first flag check arrives.
                await self._check_replicator_health()
                self._start_replicator_health_check()
            return

        if not self._base_url:
            raise ValueError("base_url is required when not in replicator mode")

        self._logger.info("Starting DataStream client")

        self._ws_client = DatastreamWSClient(WSClientOptions(
            url=self._base_url,
            api_key=self._api_key,
            message_handler=self._handle_message,
            logger=self._logger,
            connection_ready_handler=self._handle_connection_ready,
            on_connected=self._on_ws_connected,
            on_disconnected=self._on_ws_disconnected,
            on_ready=self._on_ready,
            on_not_ready=self._on_not_ready,
            on_error=self._on_ws_error,
        ))
        self._ws_client.start()

    def is_connected(self) -> bool:
        if self._replicator_mode:
            return self._replicator_ready
        return self._ws_client.is_connected() if self._ws_client else False

    def is_replicator_ready(self) -> bool:
        return self._replicator_ready

    def is_replicator_mode(self) -> bool:
        return self._replicator_mode

    @property
    def replicator_cache_version(self) -> Optional[str]:
        return self._replicator_cache_version

    async def get_company(self, keys: Dict[str, str]) -> RulesengineCompany:
        """Retrieve a company by keys, using cache or datastream."""
        cached = await self._get_company_from_cache(keys)
        if cached is not None:
            self._logger.debug("Company found in cache for keys: %s", keys)
            return cached

        if self._replicator_mode:
            raise RuntimeError("Company not found in cache and replicator mode is enabled")

        if not self.is_connected():
            raise RuntimeError("DataStream client is not connected")

        cache_keys = self._generate_company_cache_keys(keys)
        existing = any(k in self._pending_company for k in cache_keys)

        loop = asyncio.get_running_loop()
        future: asyncio.Future[Any] = loop.create_future()

        for ck in cache_keys:
            self._pending_company.setdefault(ck, []).append(future)

        if not existing:
            try:
                await self._send_request(DataStreamReq(entity_type=EntityType.COMPANY, keys=keys))
            except Exception as exc:
                self._cleanup_pending_company(cache_keys, future)
                raise

        try:
            return await asyncio.wait_for(asyncio.shield(future), timeout=RESOURCE_TIMEOUT_MS / 1000)
        except asyncio.TimeoutError:
            self._cleanup_pending_company(cache_keys, future)
            raise TimeoutError("Timeout while waiting for company data")

    async def get_user(self, keys: Dict[str, str]) -> RulesengineUser:
        """Retrieve a user by keys, using cache or datastream."""
        cached = await self._get_user_from_cache(keys)
        if cached is not None:
            self._logger.debug("User found in cache for keys: %s", keys)
            return cached

        if self._replicator_mode:
            raise RuntimeError("User not found in cache and replicator mode is enabled")

        if not self.is_connected():
            raise RuntimeError("DataStream client is not connected")

        cache_keys = self._generate_user_cache_keys(keys)
        existing = any(k in self._pending_user for k in cache_keys)

        loop = asyncio.get_running_loop()
        future: asyncio.Future[Any] = loop.create_future()

        for ck in cache_keys:
            self._pending_user.setdefault(ck, []).append(future)

        if not existing:
            try:
                await self._send_request(DataStreamReq(entity_type=EntityType.USER, keys=keys))
            except Exception as exc:
                self._cleanup_pending_user(cache_keys, future)
                raise

        try:
            return await asyncio.wait_for(asyncio.shield(future), timeout=RESOURCE_TIMEOUT_MS / 1000)
        except asyncio.TimeoutError:
            self._cleanup_pending_user(cache_keys, future)
            raise TimeoutError("Timeout while waiting for user data")

    async def get_flag(self, flag_key: str) -> Optional[RulesengineFlag]:
        """Retrieve a flag by key from cache."""
        cache_key = self._flag_cache_key(flag_key)
        self._logger.debug("Looking up flag cache key: %s (version=%s)", cache_key, self._get_version_key())
        try:
            raw = await self._flag_cache.get(cache_key)
            if raw is None:
                self._logger.debug("Flag cache miss for key: %s", cache_key)
                return None
            self._logger.debug("Flag cache hit for key: %s, validating...", cache_key)
            result = _validate(RulesengineFlag, raw)
            self._logger.debug("Flag validated successfully: %s", cache_key)
            return result
        except Exception as exc:
            self._logger.warning("Failed to retrieve/validate flag from cache: %s (key=%s)", exc, cache_key)
            return None

    async def get_all_flags(self) -> None:
        """Request a refresh of all flags from the datastream."""
        if self._pending_flags is not None and not self._pending_flags.done():
            # Wait for existing request
            await asyncio.wait_for(asyncio.shield(self._pending_flags), timeout=RESOURCE_TIMEOUT_MS / 1000)
            return

        loop = asyncio.get_running_loop()
        self._pending_flags = loop.create_future()

        try:
            await self._send_request(DataStreamReq(entity_type=EntityType.FLAGS))
        except Exception:
            fut = self._pending_flags
            self._pending_flags = None
            if not fut.done():
                fut.set_result(False)
            raise

        try:
            await asyncio.wait_for(asyncio.shield(self._pending_flags), timeout=RESOURCE_TIMEOUT_MS / 1000)
        except asyncio.TimeoutError:
            fut = self._pending_flags
            self._pending_flags = None
            if fut is not None and not fut.done():
                fut.set_result(False)
            raise TimeoutError("Timeout while waiting for flags data")

    async def check_flag(
        self,
        eval_ctx: CheckFlagRequestBody,
        flag_key: str,
    ) -> RulesengineCheckFlagResult:
        """Evaluate a flag for a company and/or user context."""
        flag = await self.get_flag(flag_key)
        if flag is None:
            raise RuntimeError(f"Flag not found: {flag_key}")

        company_keys = eval_ctx.company
        user_keys = eval_ctx.user
        needs_company = bool(company_keys)
        needs_user = bool(user_keys)

        cached_company: Optional[Any] = None
        cached_user: Optional[Any] = None

        try:
            if needs_company:
                cached_company = await self._get_company_from_cache(company_keys)  # type: ignore[arg-type]
            if needs_user:
                cached_user = await self._get_user_from_cache(user_keys)  # type: ignore[arg-type]
        except KeyConflictError as exc:
            self._logger.warning("Key conflict for flag %s: %s", flag_key, exc)
            return RulesengineCheckFlagResult(
                value=flag.default_value,
                reason="key conflict",
                flag_key=flag.key,
                flag_id=flag.id,
                err=str(exc),
            )

        # Replicator mode — evaluate with whatever is cached
        if self._replicator_mode:
            return self._evaluate_flag(flag, cached_company, cached_user)

        # If we have all required entities cached, evaluate immediately
        if (not needs_company or cached_company) and (not needs_user or cached_user):
            return self._evaluate_flag(flag, cached_company, cached_user)

        if not self.is_connected():
            raise RuntimeError("Datastream not connected and required entities not in cache")

        # Fetch missing data in parallel
        tasks = []
        if needs_company and not cached_company:
            tasks.append(self.get_company(company_keys))  # type: ignore[arg-type]
        else:
            tasks.append(_resolved(cached_company))

        if needs_user and not cached_user:
            tasks.append(self.get_user(user_keys))  # type: ignore[arg-type]
        else:
            tasks.append(_resolved(cached_user))

        results: list = await asyncio.gather(*tasks)
        return self._evaluate_flag(flag, results[0], results[1])

    async def update_company_metrics(self, keys: Dict[str, str], event: str, quantity: int) -> None:
        """Update company metrics locally in cache (for track events)."""
        company = await self._get_company_from_cache(keys)
        if company is None:
            return

        updated = company.model_copy(deep=True)
        if updated.metrics:
            new_metrics = [
                metric.model_copy(update={"value": (metric.value or 0) + quantity})
                if metric.event_subtype == event else metric
                for metric in updated.metrics
            ]
            updated = updated.model_copy(update={"metrics": new_metrics})

        await self._cache_company(updated)

    async def close(self) -> None:
        """Gracefully close the datastream client."""
        self._logger.info("Closing DataStream client")

        if self._replicator_health_task is not None:
            self._replicator_health_task.cancel()
            self._replicator_health_task = None

        if self._health_check_client is not None:
            await self._health_check_client.aclose()
            self._health_check_client = None

        self._clear_pending_requests()

        if self._ws_client is not None:
            await self._ws_client.close()
            self._ws_client = None

        self._logger.info("DataStream client closed")

    # ------------------------------------------------------------------
    # WebSocket callbacks
    # ------------------------------------------------------------------

    def _on_ws_connected(self) -> None:
        if self._on_connected:
            self._on_connected()

    def _on_ws_disconnected(self) -> None:
        self._clear_pending_requests()
        if self._on_disconnected:
            self._on_disconnected()

    def _on_ws_error(self, error: Exception) -> None:
        if self._on_error:
            self._on_error(error)

    # ------------------------------------------------------------------
    # Message handling
    # ------------------------------------------------------------------

    async def _handle_message(self, message: DataStreamResp) -> None:
        self._logger.debug(
            "Processing datastream message: EntityType=%s, MessageType=%s",
            message.entity_type, message.message_type,
        )
        try:
            if message.message_type == MessageType.ERROR.value:
                await self._handle_error_message(message)
                return

            et = message.entity_type
            if et == EntityType.COMPANY.value:
                await self._handle_company_message(message)
            elif et == EntityType.USER.value:
                await self._handle_user_message(message)
            elif et == EntityType.FLAGS.value:
                await self._handle_flags_message(message)
            elif et == EntityType.FLAG.value:
                await self._handle_flag_message(message)
            else:
                self._logger.warning("Unknown entity type: %s", et)
        except Exception as exc:
            self._logger.error("Error processing datastream message: %s", exc)
            if self._on_error:
                self._on_error(exc if isinstance(exc, Exception) else Exception(str(exc)))

    async def _handle_company_message(self, message: DataStreamResp) -> None:
        raw = message.data
        if not raw:
            return

        # For partial updates, look up the cached entity by envelope entity_id
        # and merge the wrapped data payload into it.
        if message.message_type == MessageType.PARTIAL.value:
            entity_id = message.entity_id
            if not entity_id:
                self._logger.warning("Partial company message missing entity_id")
                return

            rk = self._resource_id_cache_key(_PREFIX_COMPANY, entity_id)
            raw_existing = await self._company_cache.get(rk)
            if raw_existing is None:
                self._logger.warning("Partial company update for unknown entity: %s", entity_id)
                return

            existing = _validate(RulesengineCompany, raw_existing)
            partial_data = raw if isinstance(raw, dict) else raw.model_dump()
            try:
                company = partial_company(existing, partial_data)
            except Exception as exc:
                self._logger.error("Failed to merge partial company: %s", exc)
                return
        else:
            company = _validate(RulesengineCompany, raw)

        if message.message_type == MessageType.DELETE.value:
            await self._delete_entity(
                company.id, company.keys, _PREFIX_COMPANY, self._company_cache, self._company_key_cache,
            )
            return

        await self._cache_company(company)
        self._notify_pending_company(company.keys or {}, company)

    async def _handle_user_message(self, message: DataStreamResp) -> None:
        raw = message.data
        if not raw:
            return

        # For partial updates, look up the cached entity by envelope entity_id
        # and merge the wrapped data payload into it.
        if message.message_type == MessageType.PARTIAL.value:
            entity_id = message.entity_id
            if not entity_id:
                self._logger.warning("Partial user message missing entity_id")
                return

            rk = self._resource_id_cache_key(_PREFIX_USER, entity_id)
            raw_existing = await self._user_cache.get(rk)
            if raw_existing is None:
                self._logger.warning("Partial user update for unknown entity: %s", entity_id)
                return

            existing = _validate(RulesengineUser, raw_existing)
            partial_data = raw if isinstance(raw, dict) else raw.model_dump()
            try:
                user = partial_user(existing, partial_data)
            except Exception as exc:
                self._logger.error("Failed to merge partial user: %s", exc)
                return
        else:
            user = _validate(RulesengineUser, raw)

        if message.message_type == MessageType.DELETE.value:
            await self._delete_entity(
                user.id, user.keys, _PREFIX_USER, self._user_cache, self._user_key_cache,
            )
            return

        await self._cache_user(user)
        self._notify_pending_user(user.keys or {}, user)

    async def _handle_flags_message(self, message: DataStreamResp) -> None:
        raw_flags = message.data
        if not isinstance(raw_flags, list):
            self._logger.warning("Expected flags array in bulk flags message")
            return

        cached_keys: List[str] = []
        for raw_flag in raw_flags:
            flag = _validate(RulesengineFlag, raw_flag)
            flag_key = flag.key
            if not flag_key:
                continue
            ck = self._flag_cache_key(flag_key)
            try:
                await self._flag_cache.set(ck, flag)
                cached_keys.append(ck)
            except Exception as exc:
                self._logger.warning("Failed to cache flag: %s", exc)

        # Delete flags not in the response
        try:
            await self._flag_cache.delete_missing(cached_keys, scan_pattern="flags:*")
        except Exception as exc:
            self._logger.debug("delete_missing not supported or failed: %s", exc)

        if self._pending_flags is not None and not self._pending_flags.done():
            self._pending_flags.set_result(True)

    async def _handle_flag_message(self, message: DataStreamResp) -> None:
        raw = message.data
        flag = _validate(RulesengineFlag, raw)
        flag_key = flag.key
        if not flag_key:
            return

        ck = self._flag_cache_key(flag_key)
        try:
            if message.message_type == MessageType.DELETE.value:
                await self._flag_cache.delete(ck)
            elif message.message_type == MessageType.FULL.value:
                await self._flag_cache.set(ck, flag)
        except Exception as exc:
            self._logger.warning("Failed to update flag cache: %s", exc)

        if self._pending_flags is not None and not self._pending_flags.done():
            self._pending_flags.set_result(True)

    async def _handle_error_message(self, message: DataStreamResp) -> None:
        error_data = message.data
        if isinstance(error_data, dict):
            keys = error_data.get("keys")
            entity_type = error_data.get("entity_type")
            if keys and entity_type:
                if entity_type == EntityType.COMPANY.value:
                    self._notify_pending_company(keys, None)
                elif entity_type == EntityType.USER.value:
                    self._notify_pending_user(keys, None)

            error_msg = error_data.get("error", "Unknown datastream error")
            self._logger.warning("DataStream error received: %s", error_msg)

    async def _handle_connection_ready(self) -> None:
        self._logger.info("DataStream connection is ready")
        try:
            # Only send the flags request — don't await the response here.
            # The response will be processed by the message loop, which hasn't
            # started yet (it begins after this handler returns).
            loop = asyncio.get_running_loop()
            self._pending_flags = loop.create_future()
            await self._send_request(DataStreamReq(entity_type=EntityType.FLAGS))
            self._logger.debug("Sent initial flag data request")
        except Exception as exc:
            self._logger.error("Failed to request initial flag data: %s", exc)
            self._pending_flags = None
            raise

    # ------------------------------------------------------------------
    # Request sending
    # ------------------------------------------------------------------

    async def _send_request(self, request: DataStreamReq) -> None:
        if self._ws_client is None or not self._ws_client.is_connected():
            raise RuntimeError("DataStream client is not connected")

        self._logger.debug(
            "Sending datastream request: EntityType=%s, Keys=%s",
            request.entity_type, request.keys,
        )
        await self._ws_client.send_message(DataStreamBaseReq(data=request))

    # ------------------------------------------------------------------
    # Cache helpers
    # ------------------------------------------------------------------

    async def _get_company_from_cache(self, keys: Dict[str, str]) -> Optional[RulesengineCompany]:
        matched_id: Optional[str] = None
        for key, value in keys.items():
            ck = self._resource_key_to_cache_key(_PREFIX_COMPANY, key, value)
            try:
                company_id = await self._company_key_cache.get(ck)
            except Exception as exc:
                self._logger.warning("Failed to retrieve company from cache: %s", exc)
                continue
            self._logger.debug("Company lookup key %s -> %s", ck, company_id)
            if not company_id:
                continue
            if matched_id is None:
                matched_id = company_id
            elif matched_id != company_id:
                raise KeyConflictError(
                    f"Company keys match multiple entities: {matched_id} and {company_id}"
                )

        if matched_id is None:
            return None

        try:
            rk = self._resource_id_cache_key(_PREFIX_COMPANY, matched_id)
            raw = await self._company_cache.get(rk)
            self._logger.debug("Company ID key %s -> %s", rk, "hit" if raw is not None else "miss")
            if raw is not None:
                return _validate(RulesengineCompany, raw).model_copy(deep=True)
        except Exception as exc:
            self._logger.warning("Failed to retrieve company from cache: %s", exc)
        return None

    async def _get_user_from_cache(self, keys: Dict[str, str]) -> Optional[RulesengineUser]:
        matched_id: Optional[str] = None
        for key, value in keys.items():
            ck = self._resource_key_to_cache_key(_PREFIX_USER, key, value)
            try:
                user_id = await self._user_key_cache.get(ck)
            except Exception as exc:
                self._logger.warning("Failed to retrieve user from cache: %s", exc)
                continue
            if not user_id:
                continue
            if matched_id is None:
                matched_id = user_id
            elif matched_id != user_id:
                raise KeyConflictError(
                    f"User keys match multiple entities: {matched_id} and {user_id}"
                )

        if matched_id is None:
            return None

        try:
            rk = self._resource_id_cache_key(_PREFIX_USER, matched_id)
            raw = await self._user_cache.get(rk)
            if raw is not None:
                return _validate(RulesengineUser, raw).model_copy(deep=True)
        except Exception as exc:
            self._logger.warning("Failed to retrieve user from cache: %s", exc)
        return None

    async def _cache_company(self, company: RulesengineCompany) -> None:
        keys = company.keys
        company_id = company.id
        if not keys:
            return

        rk = self._resource_id_cache_key(_PREFIX_COMPANY, company_id)

        # Clean up stale lookup keys by diffing old vs new
        raw = await self._company_cache.get(rk)
        if raw is not None:
            old = _validate(RulesengineCompany, raw)
            old_keys = old.keys or {}
            await self._delete_stale_lookup_keys(
                self._company_key_cache, _PREFIX_COMPANY, old_keys, keys,
            )

        await self._company_cache.set(rk, company, self._cache_ttl)

        for key, value in keys.items():
            ck = self._resource_key_to_cache_key(_PREFIX_COMPANY, key, value)
            try:
                await self._company_key_cache.set(ck, company_id, self._cache_ttl)
            except Exception as exc:
                self._logger.warning("Failed to cache company key mapping '%s': %s", ck, exc)

    async def _cache_user(self, user: RulesengineUser) -> None:
        keys = user.keys
        user_id = user.id
        if not keys:
            return

        rk = self._resource_id_cache_key(_PREFIX_USER, user_id)

        # Clean up stale lookup keys by diffing old vs new
        raw = await self._user_cache.get(rk)
        if raw is not None:
            old = _validate(RulesengineUser, raw)
            old_keys = old.keys or {}
            await self._delete_stale_lookup_keys(
                self._user_key_cache, _PREFIX_USER, old_keys, keys,
            )

        await self._user_cache.set(rk, user, self._cache_ttl)

        for key, value in keys.items():
            ck = self._resource_key_to_cache_key(_PREFIX_USER, key, value)
            try:
                await self._user_key_cache.set(ck, user_id, self._cache_ttl)
            except Exception as exc:
                self._logger.warning("Failed to cache user key mapping '%s': %s", ck, exc)

    async def _delete_entity(
        self,
        entity_id: Optional[str],
        message_keys: Optional[Dict[str, str]],
        prefix: str,
        entity_cache: AsyncCacheProvider[Any],
        lookup_cache: AsyncCacheProvider[str],
    ) -> None:
        """Delete an entity and all its lookup keys from cache.

        Fetches the cached entity first to discover all lookup keys,
        since the delete message may not include them all.
        """
        all_keys = message_keys
        if entity_id:
            rk = self._resource_id_cache_key(prefix, entity_id)
            cached = await entity_cache.get(rk)
            if cached is not None:
                if isinstance(cached, dict):
                    all_keys = cached.get("keys") or message_keys
                else:
                    all_keys = cached.keys or message_keys

        if all_keys:
            for key, value in all_keys.items():
                ck = self._resource_key_to_cache_key(prefix, key, value)
                try:
                    await lookup_cache.delete(ck)
                except Exception as exc:
                    self._logger.warning("Failed to delete %s key mapping: %s", prefix, exc)

        if entity_id:
            rk = self._resource_id_cache_key(prefix, entity_id)
            try:
                await entity_cache.delete(rk)
            except Exception as exc:
                self._logger.warning("Failed to delete %s resource: %s", prefix, exc)

    async def _delete_stale_lookup_keys(
        self,
        lookup_cache: AsyncCacheProvider[str],
        prefix: str,
        old_keys: Dict[str, str],
        new_keys: Dict[str, str],
    ) -> None:
        """Delete lookup cache entries for keys that are no longer present."""
        old_set = {(k, v) for k, v in old_keys.items()}
        new_set = {(k, v) for k, v in new_keys.items()}
        for key, value in old_set - new_set:
            ck = self._resource_key_to_cache_key(prefix, key, value)
            try:
                await lookup_cache.delete(ck)
            except Exception as exc:
                self._logger.warning("Failed to delete stale lookup key '%s': %s", ck, exc)

    # ------------------------------------------------------------------
    # Cache key generation
    # ------------------------------------------------------------------

    def _flag_cache_key(self, key: str) -> str:
        version = self._get_version_key()
        return f"{_PREFIX_FLAGS}:{version}:{key.lower()}"

    def _resource_id_cache_key(self, resource_type: str, entity_id: str) -> str:
        version = self._get_version_key()
        return f"{resource_type}:{version}:{entity_id}"

    def _resource_key_to_cache_key(self, resource_type: str, key: str, value: str) -> str:
        version = self._get_version_key()
        return f"{resource_type}:{version}:{key.lower()}:{value.lower()}"

    def _get_version_key(self) -> str:
        if self._replicator_mode and self._replicator_cache_version:
            return self._replicator_cache_version
        try:
            if self._rules_engine.is_initialized():
                return self._rules_engine.get_version_key()
        except Exception:
            pass
        if self._replicator_mode:
            self._logger.warning(
                "Replicator mode active but cache version unknown — "
                "cache lookups will use fallback version '1' and likely miss"
            )
        return "1"

    def _generate_company_cache_keys(self, keys: Dict[str, str]) -> List[str]:
        return [self._resource_key_to_cache_key(_PREFIX_COMPANY, k, v) for k, v in keys.items()]

    def _generate_user_cache_keys(self, keys: Dict[str, str]) -> List[str]:
        return [self._resource_key_to_cache_key(_PREFIX_USER, k, v) for k, v in keys.items()]

    # ------------------------------------------------------------------
    # Pending request management
    # ------------------------------------------------------------------

    def _notify_pending_company(self, keys: Dict[str, str], company: Any) -> None:
        for key, value in keys.items():
            ck = self._resource_key_to_cache_key(_PREFIX_COMPANY, key, value)
            futures = self._pending_company.pop(ck, [])
            for fut in futures:
                if not fut.done():
                    if company is not None:
                        fut.set_result(company)
                    else:
                        fut.set_exception(RuntimeError("Company not found"))

    def _notify_pending_user(self, keys: Dict[str, str], user: Any) -> None:
        for key, value in keys.items():
            ck = self._resource_key_to_cache_key(_PREFIX_USER, key, value)
            futures = self._pending_user.pop(ck, [])
            for fut in futures:
                if not fut.done():
                    if user is not None:
                        fut.set_result(user)
                    else:
                        fut.set_exception(RuntimeError("User not found"))

    def _cleanup_pending_company(self, cache_keys: List[str], future: asyncio.Future[Any]) -> None:
        for ck in cache_keys:
            futures = self._pending_company.get(ck)
            if futures:
                try:
                    futures.remove(future)
                except ValueError:
                    pass
                if not futures:
                    del self._pending_company[ck]

    def _cleanup_pending_user(self, cache_keys: List[str], future: asyncio.Future[Any]) -> None:
        for ck in cache_keys:
            futures = self._pending_user.get(ck)
            if futures:
                try:
                    futures.remove(future)
                except ValueError:
                    pass
                if not futures:
                    del self._pending_user[ck]

    def _clear_pending_requests(self) -> None:
        for futures in self._pending_company.values():
            for fut in futures:
                if not fut.done():
                    fut.set_exception(RuntimeError("DataStream client disconnected"))
        self._pending_company.clear()

        for user_futures in self._pending_user.values():
            for user_fut in user_futures:
                if not user_fut.done():
                    user_fut.set_exception(RuntimeError("DataStream client disconnected"))
        self._pending_user.clear()

        if self._pending_flags is not None and not self._pending_flags.done():
            self._pending_flags.set_result(False)
        self._pending_flags = None

    # ------------------------------------------------------------------
    # Flag evaluation
    # ------------------------------------------------------------------

    def _evaluate_flag(
        self,
        flag: RulesengineFlag,
        company: Optional[RulesengineCompany],
        user: Optional[RulesengineUser],
    ) -> RulesengineCheckFlagResult:
        default_value = flag.default_value

        try:
            if self._rules_engine.is_initialized():
                return self._rules_engine.check_flag(flag, company, user)
            else:
                self._logger.warning("Rules engine not initialized, using default flag value")
                return self._make_default_result(flag, company, user, default_value, "RULES_ENGINE_UNAVAILABLE")
        except Exception as exc:
            self._logger.error("Rules engine evaluation failed: %s", exc)
            return self._make_default_result(flag, company, user, default_value, "RULES_ENGINE_ERROR")

    @staticmethod
    def _make_default_result(
        flag: RulesengineFlag,
        company: Optional[RulesengineCompany],
        user: Optional[RulesengineUser],
        value: bool,
        reason: str,
    ) -> RulesengineCheckFlagResult:
        return RulesengineCheckFlagResult(
            value=value,
            reason=reason,
            flag_key=flag.key,
            flag_id=flag.id,
            company_id=company.id if company else None,
            user_id=user.id if user else None,
        )

    # ------------------------------------------------------------------
    # Replicator health checking
    # ------------------------------------------------------------------

    def _start_replicator_health_check(self) -> None:
        if not self._replicator_health_url:
            return
        if self._health_check_client is None:
            self._health_check_client = httpx.AsyncClient(timeout=REPLICATOR_HEALTH_TIMEOUT_S)
        self._logger.info(
            "Starting replicator health check: url=%s, interval=%dms",
            self._replicator_health_url, self._replicator_health_check_ms,
        )
        self._replicator_health_task = asyncio.ensure_future(self._replicator_health_loop())

    async def _replicator_health_loop(self) -> None:
        interval_s = self._replicator_health_check_ms / 1000
        while True:
            await self._check_replicator_health()
            try:
                await asyncio.sleep(interval_s)
            except asyncio.CancelledError:
                break

    async def _check_replicator_health(self) -> None:
        if not self._replicator_health_url:
            return
        try:
            if not self._health_check_client:
                self._health_check_client = httpx.AsyncClient(timeout=REPLICATOR_HEALTH_TIMEOUT_S)
            resp = await self._health_check_client.get(self._replicator_health_url)
            resp.raise_for_status()
            health_data = resp.json()

            self._logger.debug("Replicator health response: %s", health_data)

            was_ready = self._replicator_ready
            self._replicator_ready = health_data.get("ready", False)

            new_version = health_data.get("cache_version") or health_data.get("cacheVersion")
            if new_version and new_version != self._replicator_cache_version:
                old = self._replicator_cache_version
                self._replicator_cache_version = new_version
                self._logger.info("Cache version changed from %s to %s", old, new_version)

            if self._replicator_ready and not was_ready:
                self._logger.info("External replicator is now ready")
                if self._on_replicator_health_changed:
                    self._on_replicator_health_changed(True)
            elif not self._replicator_ready and was_ready:
                self._logger.info("External replicator is no longer ready")
                if self._on_replicator_health_changed:
                    self._on_replicator_health_changed(False)

        except Exception as exc:
            if self._replicator_ready:
                self._replicator_ready = False
                self._logger.info("External replicator is no longer ready")
                if self._on_replicator_health_changed:
                    self._on_replicator_health_changed(False)
            self._logger.debug("Replicator health check failed: %s", exc)

    async def get_replicator_cache_version_async(self, timeout_s: float = REPLICATOR_CACHE_VERSION_TIMEOUT_S) -> Optional[str]:
        """Attempt to fetch cache version immediately if not already available."""
        if self._replicator_cache_version:
            return self._replicator_cache_version

        if self._replicator_mode and self._replicator_health_url:
            try:
                if not self._health_check_client:
                    self._health_check_client = httpx.AsyncClient(timeout=timeout_s)
                resp = await self._health_check_client.get(self._replicator_health_url)
                if resp.status_code == 200:
                    data = resp.json()
                    version = data.get("cache_version") or data.get("cacheVersion")
                    if version:
                        self._replicator_cache_version = version
                        return version
            except Exception as exc:
                self._logger.debug("Failed to fetch replicator cache version: %s", exc)

        return None


async def _resolved(value: Any) -> Any:
    """Helper that acts like an immediately-resolved coroutine."""
    return value
