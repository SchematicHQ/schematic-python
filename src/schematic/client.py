import atexit
import logging
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union

import httpx

from .base_client import AsyncBaseSchematic, BaseSchematic
from .cache import DEFAULT_CACHE_SIZE, DEFAULT_CACHE_TTL, AsyncCacheProvider, CacheProvider, LocalCache
from .datastream import DataStreamClient, DataStreamClientOptions
from .event_buffer import AsyncEventBuffer, EventBuffer
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
)


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
        self.event_buffer = EventBuffer(
            events_api=self.events,
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
        default_value = self._resolve_default(flag_key, options)

        if self.offline:
            return CheckFlagResponseData(
                flag=flag_key,
                reason="flag default",
                value=default_value,
            )

        return self._check_flag_via_api(flag_key, company, user, default_value)

    def _check_flag_via_api(
        self,
        flag_key: str,
        company: Optional[Dict[str, str]],
        user: Optional[Dict[str, str]],
        default_value: bool,
    ) -> CheckFlagResponseData:
        try:
            cache_key = _build_cache_key(flag_key, company, user)

            for provider in self.flag_check_cache_providers:
                cached_value = provider.get(cache_key)
                if cached_value is not None:
                    return cached_value

            resp = self.features.check_flag(flag_key, company=company, user=user)
            if resp is None or resp.data.value is None:
                return CheckFlagResponseData(
                    flag=flag_key,
                    reason="flag default",
                    value=default_value,
                )

            for provider in self.flag_check_cache_providers:
                provider.set(cache_key, resp.data)

            return resp.data
        except Exception as e:
            self.logger.error(e)
            return CheckFlagResponseData(
                flag=flag_key,
                reason="flag default",
                value=default_value,
            )

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
        self.event_buffer = AsyncEventBuffer(
            events_api=self.events,
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
        default_value = self._resolve_default(flag_key, options)

        if self.offline:
            return CheckFlagResponseData(
                flag=flag_key,
                reason="flag default",
                value=default_value,
            )

        # Try DataStream first if available
        ds = self._get_datastream()
        if ds is not None:
            try:
                resp = await ds.check_flag(
                    CheckFlagRequestBody(company=company, user=user),
                    flag_key,
                )

                # Enqueue flag_check event
                await self._enqueue_event(
                    "flag_check",
                    EventBodyFlagCheck(
                        flag_key=flag_key,
                        value=resp.value if resp.value is not None else False,
                        reason=resp.reason if resp.reason else "unknown",
                        rule_id=getattr(resp, "rule_id", None),
                        company_id=getattr(resp, "company_id", None),
                        user_id=getattr(resp, "user_id", None),
                        flag_id=getattr(resp, "flag_id", None),
                        req_company=company,
                        req_user=user,
                    ),
                )

                return CheckFlagResponseData(
                    company_id=getattr(resp, "company_id", None),
                    entitlement=getattr(resp, "entitlement", None),
                    error=getattr(resp, "err", None),
                    flag=getattr(resp, "flag", flag_key),
                    flag_id=getattr(resp, "flag_id", None),
                    reason=resp.reason,
                    rule_id=getattr(resp, "rule_id", None),
                    rule_type=getattr(resp, "rule_type", None),
                    user_id=getattr(resp, "user_id", None),
                    value=resp.value if resp.value is not None else self._get_flag_default(flag_key),
                )
            except Exception as e:
                self.logger.debug(f"Datastream flag check failed ({e}), falling back to API")

        return await self._check_flag_via_api(flag_key, company, user, default_value)

    async def _check_flag_via_api(
        self,
        flag_key: str,
        company: Optional[Dict[str, str]],
        user: Optional[Dict[str, str]],
        default_value: bool,
    ) -> CheckFlagResponseData:
        try:
            cache_key = _build_cache_key(flag_key, company, user)

            for provider in self.flag_check_cache_providers:
                cached_value = provider.get(cache_key)
                if cached_value is not None:
                    return cached_value

            resp = await self.features.check_flag(flag_key, company=company, user=user)
            if resp is None or resp.data.value is None:
                return CheckFlagResponseData(
                    flag=flag_key,
                    reason="flag default",
                    value=default_value,
                )

            for provider in self.flag_check_cache_providers:
                provider.set(cache_key, resp.data)

            return resp.data
        except Exception as e:
            self.logger.error(e)
            return CheckFlagResponseData(
                flag=flag_key,
                reason="flag default",
                value=default_value,
            )

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
                    await self._datastream_client.close_async()
                except Exception as e:
                    self.logger.error(f"Error closing DataStream client: {e}")

            # Flush and stop the event buffer
            await self.event_buffer.stop()
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
    if company or user:
        return flag_key + ":" + str(company) + ":" + str(user)
    return flag_key
