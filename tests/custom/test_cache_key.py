"""Tests for flag check cache key generation.

Corresponds to Go flags/flags_test.go TestFlagCheckCacheKey.
"""

import unittest

from schematic.client import _build_cache_key


class TestBuildCacheKey(unittest.TestCase):
    """Corresponds to Go TestFlagCheckCacheKey."""

    def test_empty_context_and_flag_key(self):
        result = _build_cache_key("")
        self.assertEqual(result, "")

    def test_flag_key_only(self):
        result = _build_cache_key("feature_flag_1")
        self.assertEqual(result, "feature_flag_1")

    def test_with_company_and_user(self):
        result = _build_cache_key(
            "feature_flag_1",
            company={"id": "123", "name": "ACME Inc."},
            user={"id": "456", "email": "john@example.com"},
        )
        # Should include flag key, company, and user in the cache key
        self.assertIn("feature_flag_1", result)
        self.assertIn("123", result)
        self.assertIn("ACME Inc.", result)
        self.assertIn("456", result)
        self.assertIn("john@example.com", result)

    def test_with_company_only(self):
        result = _build_cache_key(
            "feature_flag_2",
            company={"id": "789", "name": "XYZ Corp."},
        )
        self.assertIn("feature_flag_2", result)
        self.assertIn("789", result)
        self.assertIn("XYZ Corp.", result)

    def test_with_user_only(self):
        result = _build_cache_key(
            "feature_flag_3",
            user={"id": "abc", "email": "jane@example.com"},
        )
        self.assertIn("feature_flag_3", result)
        self.assertIn("abc", result)
        self.assertIn("jane@example.com", result)

    def test_different_contexts_produce_different_keys(self):
        """Different company/user contexts should produce different cache keys."""
        key1 = _build_cache_key("flag", company={"id": "comp-1"})
        key2 = _build_cache_key("flag", company={"id": "comp-2"})
        key3 = _build_cache_key("flag", user={"id": "user-1"})
        self.assertNotEqual(key1, key2)
        self.assertNotEqual(key1, key3)

    def test_same_context_produces_same_key(self):
        """Same inputs should always produce the same cache key."""
        key1 = _build_cache_key("flag", company={"id": "comp-1"}, user={"id": "user-1"})
        key2 = _build_cache_key("flag", company={"id": "comp-1"}, user={"id": "user-1"})
        self.assertEqual(key1, key2)


if __name__ == "__main__":
    unittest.main()
