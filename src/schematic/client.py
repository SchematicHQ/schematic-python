import atexit
import logging
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union

import httpx
from .base_client import AsyncBaseSchematic, BaseSchematic
from .cache import DEFAULT_CACHE_SIZE, DEFAULT_CACHE_TTL, AsyncCacheProvider, CacheProvider, LocalCache
from .datastream import DataStreamClient, DataStreamClientOptions
from .event_buffer import AsyncEventBuffer, EventBuffer
from .event_capture import AsyncEventCaptureClient, EventCaptureClient
from .http_client import AsyncOfflineHTTPClient, OfflineHTTPClient
from .logging import get_default_logger
from .types import (
    CheckFlagRequestBody,
    CheckFlagResponseData,
    CreateEventRequestBody,
    EventBody,
    EventBodyFlagCheck,
    EventBodyIdentify,
    EventBodyIdentifyCompany,
    EventBodyTrack,
    FeatureEntitlement,
    RulesengineCheckFlagResult,
)

# Reason strings used when returning a fallback / default flag value.
# Kept descriptive (rather than "flag default") so callers reading the reason
# field can distinguish *why* a default was returned.
REASON_OFFLINE = "Offline mode - using default value"
REASON_FLAG_NOT_FOUND = "Flag not found - using default value"
REASON_ERROR = "Error occurred - using default value"


@dataclass
class CheckFlagOptions:
    """Options for flag check methods."""

    default_value: Optional[Union[bool, Callable[[], bool]]] = None
    timeout: Optional[float] = None


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


@dataclass
class SchematicConfig:
    base_url: Optional[str] = None
    event_buffer_period: Optional[int] = None
    event_capture_url: Optional[str] = None
    flag_defaults: Optional[Dict[str, bool]] = None
    follow_redirects: Optional[bool] = True
    httpx_client: Optional[httpx.Client] = None
    logger: Optional[logging.Logger] = None
    offline: bool = False
    timeout: Optional[float] = None
    cache_providers: Optional[List[CacheProvider[CheckFlagResponseData]]] = None


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
        self.logger = config.logger or get_default_logger()
        self.flag_defaults = config.flag_defaults or {}
        self.event_capture_client = EventCaptureClient(
            api_key=api_key,
            base_url=config.event_capture_url,
            httpx_client=httpx_client,
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
            cache_key = _build_cache_key(flag_key, company, user)

            cached_value = self._safe_cache_get(cache_key)
            if cached_value is not None:
                return cached_value

            resp = self.features.check_flag(flag_key, company=company, user=user)
            if resp is None or resp.data is None or resp.data.value is None:
                return self._default_response(flag_key, options, REASON_FLAG_NOT_FOUND)

            self._safe_cache_set(cache_key, resp.data)

            return resp.data
        except Exception as e:
            self.logger.error(e)
            return self._default_response(flag_key, options, f"{REASON_ERROR}: {e}")

    def identify(
        self,
        keys: Dict[str, str],
        company: Optional[EventBodyIdentifyCompany] = None,
        name: Optional[str] = None,
        traits: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._enqueue_event(
            "identify",
            EventBodyIdentify(
                company=company,
                keys=keys,
                name=name,
                traits=traits,
            ),
        )

    def track(
        self,
        event: str,
        company: Optional[Dict[str, str]] = None,
        user: Optional[Dict[str, str]] = None,
        traits: Optional[Dict[str, Any]] = None,
        quantity: Optional[int] = None,
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
        )

    def _enqueue_event(self, event_type: str, body: EventBody) -> None:
        if self.offline:
            return
        try:
            event_body = CreateEventRequestBody(event_type=event_type, body=body)
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
    offline: bool = False
    timeout: Optional[float] = None
    cache_providers: Optional[List[CacheProvider[CheckFlagResponseData]]] = None
    use_datastream: bool = False
    datastream: Optional[DataStreamConfig] = None


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
        self.logger = config.logger or get_default_logger()
        self.flag_defaults = config.flag_defaults or {}
        self.event_capture_client = AsyncEventCaptureClient(
            api_key=api_key,
            base_url=config.event_capture_url,
            httpx_client=httpx_client,
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

            self._datastream_client = DataStreamClient(ds_opts)

        self._initialized = True

    async def __aenter__(self):
        await self._start_datastream()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.shutdown()

    async def _start_datastream(self) -> None:
        if self._datastream_client is not None:
            try:
                await self._datastream_client.start()
            except Exception as e:
                self.logger.error(f"Failed to start DataStream client: {e}")
                self._datastream_client = None

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
                )
                await self._enqueue_flag_check_event(flag_key, resp, company, user)
                return self._ds_result_to_response(flag_key, resp, options)
            except Exception as e:
                self.logger.debug(f"Datastream flag check failed ({e}), falling back to API")

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
                self.logger.debug(f"Datastream check_flags failed ({e}), falling back to bulk API")

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
            cache_key = _build_cache_key(flag_key, company, user)

            cached_value = self._safe_cache_get(cache_key)
            if cached_value is not None:
                return cached_value

            resp = await self.features.check_flag(flag_key, company=company, user=user)
            if resp is None or resp.data is None or resp.data.value is None:
                return self._default_response(flag_key, options, REASON_FLAG_NOT_FOUND)

            self._safe_cache_set(cache_key, resp.data)

            return resp.data
        except Exception as e:
            self.logger.error(e)
            return self._default_response(flag_key, options, f"{REASON_ERROR}: {e}")

    async def identify(
        self,
        keys: Dict[str, str],
        company: Optional[EventBodyIdentifyCompany] = None,
        name: Optional[str] = None,
        traits: Optional[Dict[str, Any]] = None,
    ) -> None:
        await self._enqueue_event(
            "identify",
            EventBodyIdentify(
                company=company,
                keys=keys,
                name=name,
                traits=traits,
            ),
        )

    async def track(
        self,
        event: str,
        company: Optional[Dict[str, str]] = None,
        user: Optional[Dict[str, str]] = None,
        traits: Optional[Dict[str, Any]] = None,
        quantity: Optional[int] = None,
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
        )

        # Update company metrics in DataStream if available and connected
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

    async def _enqueue_event(self, event_type: str, body: EventBody) -> None:
        if self.offline:
            return
        try:
            event_body = CreateEventRequestBody(event_type=event_type, body=body)
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


