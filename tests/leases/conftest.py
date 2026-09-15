from __future__ import annotations

from typing import Iterator
from unittest import mock

import pytest
from lease_support import VirtualClock, make_fake_redis


@pytest.fixture
def clock() -> VirtualClock:
    return VirtualClock()


@pytest.fixture
def frozen_clock(clock: VirtualClock) -> Iterator[VirtualClock]:
    """A virtual clock that is also the process clock.

    The Redis stores decide expiry against the store's own clock (Redis TIME),
    which fakeredis reads from ``time.time``, so a test that moves the virtual
    clock has to move that one too.
    """
    with mock.patch("time.time", clock):
        yield clock


@pytest.fixture
def redis_client(frozen_clock: VirtualClock) -> object:
    return make_fake_redis()
