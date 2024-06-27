import time
from collections import OrderedDict
from typing import Generic, Optional
from typing import OrderedDict as OrderedDictType
from typing import TypeVar

T = TypeVar("T")

DEFAULT_CACHE_SIZE = 1000  # 1000 items
DEFAULT_CACHE_TTL = 5000  # 5 seconds


class CacheProvider(Generic[T]):
    def get(self, key: str) -> Optional[T]:
        pass

    def set(self, key: str, val: T, ttl_override: Optional[int] = None) -> None:
        pass


class CachedItem(Generic[T]):
    def __init__(self, value: T, expiration: float):
        self.value = value
        self.expiration = expiration


class LocalCache(CacheProvider[T]):
    def __init__(self, max_size: int, ttl: int):
        self.cache: OrderedDictType[str, CachedItem[T]] = OrderedDict()
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

        # Move the accessed item to the end (most recently used)
        self.cache.move_to_end(key)
        return item.value

    def set(self, key: str, val: T, ttl_override: Optional[int] = None) -> None:
        if self.max_size == 0:
            return

        ttl = self.ttl if ttl_override is None else ttl_override
        expiration = time.time() * 1000 + ttl

        # If the key already exists, update it and move it to the end
        if key in self.cache:
            self.cache[key] = CachedItem(val, expiration)
            self.cache.move_to_end(key)
        else:
            # If we're at capacity, remove the least recently used item
            if len(self.cache) >= self.max_size:
                self.cache.popitem(last=False)

            # Add the new item
            self.cache[key] = CachedItem(val, expiration)

    def clean_expired(self):
        current_time = time.time() * 1000
        self.cache = OrderedDict(
            (k, v) for k, v in self.cache.items() if v.expiration > current_time
        )
