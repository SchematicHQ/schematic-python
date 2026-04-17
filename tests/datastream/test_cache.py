from __future__ import annotations

import asyncio
import time

import pytest

from schematic.cache import AsyncCacheProvider as CacheProvider, AsyncLocalCache as LocalCache


class TestLocalCacheGet:
    async def test_returns_none_for_missing_key(self) -> None:
        cache: LocalCache[str] = LocalCache(ttl=5000)
        assert await cache.get("nonexistent") is None

    async def test_returns_stored_value(self) -> None:
        cache: LocalCache[str] = LocalCache(ttl=5000)
        await cache.set("key1", "value1")
        assert await cache.get("key1") == "value1"

    async def test_returns_none_for_expired_item(self) -> None:
        cache: LocalCache[str] = LocalCache(ttl=1)  # 1ms TTL
        await cache.set("key1", "value1")
        await asyncio.sleep(0.01)  # Wait for expiration
        assert await cache.get("key1") is None


class TestLocalCacheSet:
    async def test_overwrites_existing_value(self) -> None:
        cache: LocalCache[str] = LocalCache(ttl=5000)
        await cache.set("key1", "value1")
        await cache.set("key1", "value2")
        assert await cache.get("key1") == "value2"

    async def test_respects_max_items_with_lru_eviction(self) -> None:
        cache: LocalCache[str] = LocalCache(max_items=2, ttl=5000)
        await cache.set("a", "1")
        await cache.set("b", "2")
        # Access 'a' to make it recently used
        await cache.get("a")
        # Adding 'c' should evict 'b' (least recently used)
        await cache.set("c", "3")
        assert await cache.get("a") == "1"
        assert await cache.get("b") is None
        assert await cache.get("c") == "3"

    async def test_disabled_cache_when_max_items_zero(self) -> None:
        cache: LocalCache[str] = LocalCache(max_items=0, ttl=5000)
        await cache.set("key1", "value1")
        assert await cache.get("key1") is None

    async def test_ttl_override(self) -> None:
        cache: LocalCache[str] = LocalCache(ttl=5000)
        await cache.set("key1", "value1", ttl=1)  # 1ms override
        await asyncio.sleep(0.01)
        assert await cache.get("key1") is None


class TestLocalCacheDelete:
    async def test_deletes_existing_key(self) -> None:
        cache: LocalCache[str] = LocalCache(ttl=5000)
        await cache.set("key1", "value1")
        await cache.delete("key1")
        assert await cache.get("key1") is None

    async def test_no_error_deleting_nonexistent_key(self) -> None:
        cache: LocalCache[str] = LocalCache(ttl=5000)
        await cache.delete("nonexistent")  # Should not raise


class TestLocalCacheDeleteMissing:
    async def test_removes_keys_not_in_keep_list(self) -> None:
        cache: LocalCache[str] = LocalCache(ttl=5000)
        await cache.set("a", "1")
        await cache.set("b", "2")
        await cache.set("c", "3")
        await cache.delete_missing(["a", "c"])
        assert await cache.get("a") == "1"
        assert await cache.get("b") is None
        assert await cache.get("c") == "3"


class TestCacheProviderInterface:
    async def test_raises_not_implemented(self) -> None:
        provider: CacheProvider[str] = CacheProvider()
        with pytest.raises(NotImplementedError):
            await provider.get("key")
        with pytest.raises(NotImplementedError):
            await provider.set("key", "value")
        with pytest.raises(NotImplementedError):
            await provider.delete("key")
        with pytest.raises(NotImplementedError):
            await provider.delete_missing(["key"])
