from __future__ import annotations

import time
from collections import OrderedDict
from typing import Any, Generic, List, Optional, Set, TypeVar

from .provider import AsyncCacheProvider, CacheProvider

T = TypeVar("T")

DEFAULT_CACHE_SIZE = 1000
DEFAULT_CACHE_TTL = 5000  # 5 seconds
DEFAULT_MAX_ITEMS = 1000
DEFAULT_TTL_MS = 5000


class CachedItem(Generic[T]):
    __slots__ = ("value", "expiration")

    def __init__(self, value: T, expiration: float) -> None:
        self.value = value
        self.expiration = expiration


class LocalCache(CacheProvider[T]):
    """In-memory synchronous cache with LRU eviction and TTL support."""

    def __init__(self, max_size: int = DEFAULT_CACHE_SIZE, ttl: int = DEFAULT_CACHE_TTL) -> None:
        self.cache: OrderedDict[str, CachedItem[Any]] = OrderedDict()
        self.max_size = max_size
        self.ttl = ttl

    def get(self, key: str) -> Optional[T]:
        if self.max_size == 0 or key not in self.cache:
            return None

        item = self.cache[key]
        current_time = time.time() * 1000

        if current_time > item.expiration:
            del self.cache[key]
            return None

        self.cache.move_to_end(key)
        return item.value

    def set(self, key: str, val: T, ttl_override: Optional[int] = None) -> None:
        if self.max_size == 0:
            return

        ttl = self.ttl if ttl_override is None else ttl_override
        expiration = time.time() * 1000 + ttl

        if key in self.cache:
            self.cache[key] = CachedItem(val, expiration)
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.max_size:
                self.cache.popitem(last=False)
            self.cache[key] = CachedItem(val, expiration)

    def clean_expired(self) -> None:
        current_time = time.time() * 1000
        self.cache = OrderedDict(
            (k, v) for k, v in self.cache.items() if v.expiration > current_time
        )


class _AsyncCacheItem(Generic[T]):
    __slots__ = ("value", "access_counter", "expiration")

    def __init__(self, value: T, access_counter: int, expiration: float) -> None:
        self.value = value
        self.access_counter = access_counter
        self.expiration = expiration


class AsyncLocalCache(AsyncCacheProvider[T]):
    """In-memory async cache with LRU eviction and TTL support."""

    def __init__(self, *, max_items: int = DEFAULT_MAX_ITEMS, ttl: int = DEFAULT_TTL_MS) -> None:
        self._cache: OrderedDict[str, _AsyncCacheItem[Any]] = OrderedDict()
        self._max_items = max_items
        self._default_ttl = ttl
        self._access_counter = 0

    async def get(self, key: str) -> Optional[T]:
        item = self._cache.get(key)
        if item is None:
            return None

        now_ms = time.time() * 1000
        if now_ms >= item.expiration:
            del self._cache[key]
            return None

        self._access_counter += 1
        item.access_counter = self._access_counter
        self._cache.move_to_end(key)
        return item.value

    async def set(self, key: str, value: T, ttl: Optional[int] = None) -> None:
        if self._max_items == 0:
            return

        effective_ttl = ttl if ttl is not None else self._default_ttl

        if key in self._cache:
            del self._cache[key]

        self._evict_expired()

        while len(self._cache) >= self._max_items:
            oldest_key: Optional[str] = None
            oldest_counter = float("inf")
            for k, item in self._cache.items():
                if item.access_counter < oldest_counter:
                    oldest_key = k
                    oldest_counter = item.access_counter
            if oldest_key is not None:
                del self._cache[oldest_key]
            else:
                break

        self._access_counter += 1
        now_ms = time.time() * 1000
        self._cache[key] = _AsyncCacheItem(
            value=value,
            access_counter=self._access_counter,
            expiration=now_ms + effective_ttl,
        )

    async def delete(self, key: str) -> None:
        self._cache.pop(key, None)

    async def delete_missing(self, keys_to_keep: List[str], *, scan_pattern: Optional[str] = None) -> None:
        keep_set: Set[str] = set(keys_to_keep)
        to_delete = [k for k in self._cache if k not in keep_set]
        for k in to_delete:
            del self._cache[k]

    def _evict_expired(self) -> None:
        now_ms = time.time() * 1000
        expired = [k for k, item in self._cache.items() if now_ms >= item.expiration]
        for k in expired:
            del self._cache[k]
