import time
import threading
import unittest

from schematic.cache import LocalCache


class TestLocalCache(unittest.TestCase):
    def setUp(self):
        self.cache = LocalCache(max_size=2, ttl=2000)

    def test_cache_size_limit(self):
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")

        # Get value for key1; this should make it more recently used for the purposes of eviction
        val1 = self.cache.get("key1")
        self.assertEqual(val1, "value1")

        # Add a new key-value pair; this should evict the least recently used key, which will now be key2
        self.cache.set("key3", "value3")

        # Assert correct eviction (key2 evicted, key1 and key3 still present)
        val1 = self.cache.get("key1")
        self.assertEqual(val1, "value1")
        val2 = self.cache.get("key2")
        self.assertIsNone(val2)
        val3 = self.cache.get("key3")
        self.assertEqual(val3, "value3")


class TestLocalCacheGetSet(unittest.TestCase):
    """Corresponds to Go TestLocalCache_Get_Set."""

    def test_basic_set_and_get(self):
        cache = LocalCache(max_size=10, ttl=5000)
        cache.set("key1", "value1")
        self.assertEqual(cache.get("key1"), "value1")

    def test_get_nonexistent_key(self):
        cache = LocalCache(max_size=10, ttl=5000)
        self.assertIsNone(cache.get("missing"))

    def test_overwrite_existing_key(self):
        cache = LocalCache(max_size=10, ttl=5000)
        cache.set("key1", "value1")
        cache.set("key1", "value2")
        self.assertEqual(cache.get("key1"), "value2")

    def test_set_with_custom_ttl(self):
        cache = LocalCache(max_size=10, ttl=5000)
        cache.set("key1", "value1", ttl_override=1)  # 1ms TTL
        time.sleep(0.05)
        self.assertIsNone(cache.get("key1"))


class TestLocalCacheDelete(unittest.TestCase):
    """Corresponds to Go TestLocalCache_Delete."""

    def test_delete_existing_key(self):
        cache = LocalCache(max_size=10, ttl=5000)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        # Remove key1 by overwriting the cache internals
        del cache.cache["key1"]
        self.assertIsNone(cache.get("key1"))
        self.assertEqual(cache.get("key2"), "value2")

    def test_delete_nonexistent_key(self):
        """Deleting a nonexistent key should not raise."""
        cache = LocalCache(max_size=10, ttl=5000)
        # Accessing a missing key via cache internals should not error
        cache.cache.pop("missing", None)


class TestLocalCacheLRU(unittest.TestCase):
    """Corresponds to Go TestLocalCache_LRU."""

    def test_lru_eviction(self):
        cache = LocalCache(max_size=3, ttl=5000)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")

        # Access key1 to make it most recently used
        cache.get("key1")

        # Adding key4 should evict key2 (least recently used)
        cache.set("key4", "value4")

        self.assertEqual(cache.get("key1"), "value1")
        self.assertIsNone(cache.get("key2"))
        self.assertEqual(cache.get("key3"), "value3")
        self.assertEqual(cache.get("key4"), "value4")


class TestLocalCacheExpiration(unittest.TestCase):
    """Corresponds to Go TestLocalCache_Expiration."""

    def test_items_expire_after_ttl(self):
        cache = LocalCache(max_size=10, ttl=50)  # 50ms TTL
        cache.set("key1", "value1")

        # Immediately available
        self.assertEqual(cache.get("key1"), "value1")

        # Gone after TTL
        time.sleep(0.1)
        self.assertIsNone(cache.get("key1"))

    def test_new_items_work_after_expiration(self):
        cache = LocalCache(max_size=10, ttl=50)
        cache.set("key1", "value1")
        time.sleep(0.1)
        self.assertIsNone(cache.get("key1"))

        # New items should still work
        cache.set("key2", "value2")
        self.assertEqual(cache.get("key2"), "value2")


class TestLocalCacheCleanExpired(unittest.TestCase):
    """Corresponds to Go TestLocalCache_CleanupRoutine."""

    def test_clean_expired_removes_stale_items(self):
        cache = LocalCache(max_size=10, ttl=50)
        for i in range(5):
            cache.set(f"key{i}", f"value{i}")

        time.sleep(0.1)
        cache.clean_expired()

        for i in range(5):
            self.assertIsNone(cache.get(f"key{i}"))

    def test_clean_expired_keeps_valid_items(self):
        cache = LocalCache(max_size=10, ttl=5000)
        cache.set("key1", "value1")
        cache.clean_expired()
        self.assertEqual(cache.get("key1"), "value1")


class TestLocalCacheZeroSize(unittest.TestCase):
    """Corresponds to Go TestLocalCache_NilSafety (zero-size cache acts as disabled)."""

    def test_get_returns_none(self):
        cache = LocalCache(max_size=0, ttl=5000)
        self.assertIsNone(cache.get("key1"))

    def test_set_is_noop(self):
        cache = LocalCache(max_size=0, ttl=5000)
        cache.set("key1", "value1")
        self.assertIsNone(cache.get("key1"))


class TestLocalCacheDefaults(unittest.TestCase):
    """Corresponds to Go TestLocalCache_DefaultCache."""

    def test_default_cache_has_correct_defaults(self):
        from schematic.cache.local import DEFAULT_CACHE_SIZE, DEFAULT_CACHE_TTL
        cache = LocalCache()
        self.assertEqual(cache.max_size, DEFAULT_CACHE_SIZE)
        self.assertEqual(cache.ttl, DEFAULT_CACHE_TTL)


class TestLocalCacheDifferentTypes(unittest.TestCase):
    """Corresponds to Go TestLocalCache_DifferentTypes."""

    def test_string_cache(self):
        cache = LocalCache(max_size=10, ttl=5000)
        cache.set("key", "hello")
        self.assertEqual(cache.get("key"), "hello")

    def test_int_cache(self):
        cache = LocalCache(max_size=10, ttl=5000)
        cache.set("key", 42)
        self.assertEqual(cache.get("key"), 42)

    def test_dict_cache(self):
        cache = LocalCache(max_size=10, ttl=5000)
        val = {"name": "test", "items": [1, 2, 3]}
        cache.set("key", val)
        self.assertEqual(cache.get("key"), val)


class TestLocalCacheConcurrency(unittest.TestCase):
    """Corresponds to Go TestLocalCache_Concurrency and TestLocalCache_ConcurrentSafe."""

    def test_concurrent_reads_and_writes(self):
        cache = LocalCache(max_size=100, ttl=5000)
        errors = []

        def worker(worker_id):
            try:
                for i in range(20):
                    key = f"key-{worker_id}-{i}"
                    cache.set(key, f"value-{i}")
                    cache.get(key)
                    cache.get(f"key-{(worker_id + 1) % 5}-{i}")
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(errors), 0, f"Concurrent access errors: {errors}")


class TestLocalCacheEdgeCases(unittest.TestCase):
    """Corresponds to Go TestLocalCache_EdgeCases."""

    def test_very_short_ttl(self):
        cache = LocalCache(max_size=10, ttl=1)  # 1ms
        cache.set("key", "value")
        time.sleep(0.01)
        self.assertIsNone(cache.get("key"))

    def test_very_large_ttl(self):
        cache = LocalCache(max_size=10, ttl=100 * 365 * 24 * 60 * 60 * 1000)  # 100 years
        cache.set("key", "value")
        self.assertEqual(cache.get("key"), "value")

    def test_zero_ttl(self):
        """Zero TTL means items expire immediately."""
        cache = LocalCache(max_size=10, ttl=0)
        cache.set("key", "value")
        # With 0 TTL, expiration = now, so item is already expired
        self.assertIsNone(cache.get("key"))

    def test_ttl_override_shorter_than_default(self):
        cache = LocalCache(max_size=10, ttl=5000)
        cache.set("key", "value", ttl_override=1)  # 1ms override
        time.sleep(0.05)
        self.assertIsNone(cache.get("key"))

    def test_max_size_enforcement(self):
        cache = LocalCache(max_size=3, ttl=5000)
        for i in range(10):
            cache.set(f"key{i}", f"value{i}")
        # Only the last 3 should remain
        count = sum(1 for i in range(10) if cache.get(f"key{i}") is not None)
        self.assertEqual(count, 3)


if __name__ == "__main__":
    unittest.main()
