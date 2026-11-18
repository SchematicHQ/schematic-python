import asyncio

import pytest

from schematic.cache import AsyncLocalCache


@pytest.mark.parametrize(
    "pattern,keep,expected",
    [
        ("flags:*", [], {"companies:one", "Flags:case"}),
        ("flags:*", ["flags:one"], {"flags:one", "companies:one", "Flags:case"}),
        ("companies:*", [], {"flags:one", "flags:two", "Flags:case"}),
        ("missing:*", [], {"flags:one", "flags:two", "companies:one", "Flags:case"}),
        (None, ["flags:one"], {"flags:one"}),
        ("*", ["flags:one"], {"flags:one"}),
    ],
)
def test_delete_missing_respects_scan_pattern(pattern, keep, expected):
    async def scenario():
        cache = AsyncLocalCache()
        keys = ["flags:one", "flags:two", "companies:one", "Flags:case"]
        for key in keys:
            await cache.set(key, key)

        await cache.delete_missing(keep, scan_pattern=pattern)

        remaining = {key for key in keys if await cache.get(key) is not None}
        assert remaining == expected

    asyncio.run(scenario())
