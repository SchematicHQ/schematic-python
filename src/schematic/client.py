import atexit
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import httpx

from .base_client import AsyncBaseSchematic, BaseSchematic
from .cache import DEFAULT_CACHE_SIZE, DEFAULT_CACHE_TTL, CacheProvider, LocalCache
from .event_buffer import AsyncEventBuffer, EventBuffer
from .http_client import AsyncOfflineHTTPClient, OfflineHTTPClient
from .logging import get_default_logger
from .types import (
    CreateEventRequestBody,
    EventBody,
    EventBodyIdentify,
    EventBodyIdentifyCompany,
    EventBodyTrack,
)


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
    cache_providers: Optional[List[CacheProvider[bool]]] = None


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
        self.flag_check_cache_providers = config.cache_providers or [
            LocalCache[bool](DEFAULT_CACHE_SIZE, DEFAULT_CACHE_TTL)
        ]
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
    ) -> bool:
        if self.offline:
            return self._get_flag_default(flag_key)

        try:
            cache_key = (
                flag_key + ":" + str(company) + ":" + str(user)
                if (company or user)
                else flag_key
            )

            for provider in self.flag_check_cache_providers:
                cached_value = provider.get(cache_key)
                if cached_value is not None:
                    return cached_value

            resp = self.features.check_flag(flag_key, company=company, user=user)
            if resp is None:
                return self._get_flag_default(flag_key)

            for provider in self.flag_check_cache_providers:
                provider.set(cache_key, resp.data.value)

            return resp.data.value
        except Exception as e:
            self.logger.error(e)
            return self._get_flag_default(flag_key)

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
    cache_providers: Optional[List[CacheProvider[bool]]] = None


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
        self.flag_check_cache_providers = config.cache_providers or [
            LocalCache[bool](DEFAULT_CACHE_SIZE, DEFAULT_CACHE_TTL)
        ]
        self.offline = config.offline
        self._shutdown_requested = False
        self._is_shutting_down = False
        self._initialized = True

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.shutdown()

    async def initialize(self) -> None:
      pass

    async def check_flag(
        self,
        flag_key: str,
        company: Optional[Dict[str, str]] = None,
        user: Optional[Dict[str, str]] = None,
    ) -> bool:
        if self.offline:
            return self._get_flag_default(flag_key)

        try:
            cache_key = (
                flag_key + ":" + str(company) + ":" + str(user)
                if (company or user)
                else flag_key
            )

            for provider in self.flag_check_cache_providers:
                cached_value = provider.get(cache_key)
                if cached_value is not None:
                    return cached_value

            resp = await self.features.check_flag(flag_key, company=company, user=user)
            if resp is None:
                return self._get_flag_default(flag_key)

            for provider in self.flag_check_cache_providers:
                provider.set(cache_key, resp.data.value)

            return resp.data.value
        except Exception as e:
            self.logger.error(e)
            return self._get_flag_default(flag_key)

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
            # Flush and stop the event buffer
            await self.event_buffer.stop()
            self.logger.info("Shutdown complete.")
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
        finally:
            self._shutdown_requested = True
            
