from __future__ import annotations

import json
import logging
from typing import Any, List, Optional, TypeVar

from .provider import AsyncCacheProvider

T = TypeVar("T")

logger = logging.getLogger(__name__)

class RedisCache(AsyncCacheProvider[T]):
    """Async Redis cache provider using redis.asyncio.

    Stores values as JSON strings. Supports TTL and pattern-based bulk deletion.

    Usage::

        import redis.asyncio as redis

        pool = redis.ConnectionPool.from_url("redis://localhost:6379")
        client = redis.Redis(connection_pool=pool)
        cache = RedisCache(client, prefix="schematic:flags")
    """

    def __init__(
        self,
        client: Any,
        *,
        prefix: str = "schematic",
        default_ttl_ms: Optional[int] = None,
    ) -> None:
        self._client = client
        self._prefix = prefix
        self._default_ttl_ms = default_ttl_ms

    def _prefixed(self, key: str) -> str:
        return f"{self._prefix}:{key}"

    async def get(self, key: str) -> Optional[T]:
        prefixed_key = self._prefixed(key)
        raw = await self._client.get(prefixed_key)
        logger.debug("Redis GET %s -> %s", prefixed_key, "hit" if raw is not None else "miss")
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            logger.warning("Failed to deserialize cache value for key: %s", key)
            return None

    async def set(self, key: str, value: T, ttl: Optional[int] = None) -> None:
        effective_ttl = ttl if ttl is not None else self._default_ttl_ms
        serialized = json.dumps(value, default=_json_default)
        prefixed = self._prefixed(key)
        if effective_ttl is not None:
            await self._client.psetex(prefixed, effective_ttl, serialized)
        else:
            await self._client.set(prefixed, serialized)

    async def delete(self, key: str) -> None:
        await self._client.delete(self._prefixed(key))

    async def delete_missing(self, keys_to_keep: List[str], *, scan_pattern: Optional[str] = None) -> None:
        """Delete all keys matching scan_pattern that are not in keys_to_keep.

        Uses SCAN to iterate keys without blocking the server.
        """
        pattern = self._prefixed(scan_pattern or "*")
        keep_set = {self._prefixed(k) for k in keys_to_keep}
        to_delete: list[str] = []

        async for key in self._client.scan_iter(match=pattern, count=100):
            key_str = key.decode("utf-8") if isinstance(key, bytes) else key
            if key_str not in keep_set:
                to_delete.append(key_str)

        if to_delete:
            await self._client.delete(*to_delete)


def _json_default(obj: Any) -> Any:
    """Default JSON serializer for Pydantic models and datetime objects."""
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json")
    if hasattr(obj, "dict"):
        return obj.dict()
    if hasattr(obj, "isoformat"):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")
