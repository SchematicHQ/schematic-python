from __future__ import annotations

from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class CacheProvider(Generic[T]):
    """Synchronous cache provider interface."""

    def get(self, key: str) -> Optional[T]:
        raise NotImplementedError

    def set(self, key: str, val: T, ttl_override: Optional[int] = None) -> None:
        raise NotImplementedError


class AsyncCacheProvider(Generic[T]):
    """Async cache provider interface for storing and retrieving entities."""

    async def get(self, key: str) -> Optional[T]:
        raise NotImplementedError

    async def set(self, key: str, value: T, ttl: Optional[int] = None) -> None:
        raise NotImplementedError

    async def delete(self, key: str) -> None:
        raise NotImplementedError

    async def delete_missing(self, keys_to_keep: List[str], *, scan_pattern: Optional[str] = None) -> None:
        """Delete all keys not in keys_to_keep. Optional for bulk operations."""
        raise NotImplementedError
