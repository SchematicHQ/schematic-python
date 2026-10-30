"""Tests for context signing

context-signing.json is copied verbatim from api/lib/contextsig/testdata in the
Schematic API, which generates it from the verifier and checks it in its own
tests. Don't edit it here.
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Tuple

import pytest

from schematic.context_signature import (
    DEFAULT_CONTEXT_SIGNATURE_LIFETIME_SECONDS,
    MAX_CONTEXT_SIGNATURE_LIFETIME_SECONDS,
    ContextSignatureError,
    canonicalize_context,
    sign_context,
)
from schematic.context_signature.signing import _sign_context_at

VECTORS: Dict[str, Any] = json.loads(
    (Path(__file__).parent / "context-signing.json").read_text(encoding="utf-8")
)


def _window(signature: str) -> Tuple[int, int]:
    iat, exp, _ = signature.split(".")
    return int(iat), int(exp)


def test_caps_the_lifetime_where_the_api_does():
    assert MAX_CONTEXT_SIGNATURE_LIFETIME_SECONDS == VECTORS["max_lifetime_seconds"]


@pytest.mark.parametrize("vector", VECTORS["vectors"], ids=[v["name"] for v in VECTORS["vectors"]])
def test_signing_vectors(vector):
    assert canonicalize_context(vector["context"]) == vector["canonical"]
    assert _sign_context_at(vector["secret"], vector["context"], vector["iat"], vector["exp"]) == vector["signature"]


CONTEXT = {"company": {"id": "comp_1"}}


def test_signs_for_the_default_lifetime_from_now():
    before = int(time.time())
    iat, exp = _window(sign_context("secret", CONTEXT))

    assert before <= iat <= int(time.time())
    assert exp - iat == DEFAULT_CONTEXT_SIGNATURE_LIFETIME_SECONDS


def test_signs_from_the_time_and_for_the_lifetime_given():
    issued_at = datetime.fromtimestamp(1_700_000_000.5, tz=timezone.utc)
    signature = sign_context("secret", CONTEXT, issued_at=issued_at, lifetime_seconds=300)

    assert signature == _sign_context_at("secret", CONTEXT, 1_700_000_000, 1_700_000_300)


@pytest.mark.parametrize("lifetime_seconds", [0, -60, 1.5, True, MAX_CONTEXT_SIGNATURE_LIFETIME_SECONDS + 1, 86_400])
def test_refuses_a_lifetime_the_api_would_reject(lifetime_seconds):
    with pytest.raises(ContextSignatureError):
        sign_context("secret", CONTEXT, lifetime_seconds=lifetime_seconds)


def test_refuses_a_missing_secret():
    with pytest.raises(ContextSignatureError):
        sign_context("", CONTEXT)


@pytest.mark.parametrize("keys", [{"id": 123}, {"id": None}, {1: "a"}])
def test_refuses_a_key_or_value_that_isnt_a_string(keys):
    with pytest.raises(ContextSignatureError):
        sign_context("secret", {"company": keys})


def test_leaves_out_a_company_or_user_that_is_none():
    assert canonicalize_context({"company": None, "user": None}) == "{}"


def test_signs_a_lone_surrogate_as_the_replacement_character():
    assert canonicalize_context({"company": {"name": "a\ud800b"}}) == '{"company":{"name":"a\ufffdb"}}'
    assert canonicalize_context({"company": {"name": "a\udc00"}}) == '{"company":{"name":"a\ufffd"}}'


def test_joins_a_surrogate_pair_into_its_character():
    assert canonicalize_context({"company": {"name": "\ud83d\ude00"}}) == '{"company":{"name":"\U0001f600"}}'
    assert canonicalize_context({"company": {"name": "\U0001f600"}}) == '{"company":{"name":"\U0001f600"}}'
