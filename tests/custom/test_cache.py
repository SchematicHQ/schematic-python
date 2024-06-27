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


if __name__ == "__main__":
    unittest.main()
