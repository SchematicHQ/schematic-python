"""Context signing for Schematic.

Signs the context a browser SDK sends with a publishable key, for environments
that require context signatures.

A publishable key is public, so the API can't trust the company and user a
browser names with it. When the environment requires signatures, your backend,
which holds the secret API key, signs the logged-in user's own company and
user, and the browser SDK sends that signature in the X-Schematic-Context-Sig
header. Sign the context from your own authenticated session, never from what
the browser asks for.

The signature is ``iat.exp.sig``, where ``sig`` is the unpadded base64url
HMAC-SHA256 of ``canonical(context).iat.exp`` keyed with the secret API key,
and ``canonical`` is the context's JSON with keys sorted by code point and no
whitespace. It matches the Go and Node.js SDKs.
"""

import base64
import hashlib
import hmac
import json
import math
import time
from datetime import datetime
from typing import Mapping, Optional, TypedDict

CONTEXT_SIGNATURE_HEADER = "X-Schematic-Context-Sig"
"""Request header the browser SDK sends the signature in."""

DEFAULT_CONTEXT_SIGNATURE_LIFETIME_SECONDS = 600
"""How long a signature is valid for unless ``lifetime_seconds`` says otherwise.
It matches how long the browser SDK reuses one."""

MAX_CONTEXT_SIGNATURE_LIFETIME_SECONDS = 3600
"""The longest the API accepts a signature as valid for."""


class SignableContext(TypedDict, total=False):
    """The company and user a browser SDK checks flags and sends events for,
    by their keys. Leave one out, or set it to None, when it's absent; an empty
    dict is signed as empty. It must match the context the browser SDK is given
    exactly."""

    company: Optional[Mapping[str, str]]
    user: Optional[Mapping[str, str]]


class ContextSignatureError(Exception):
    """Exception raised when a context can't be signed."""

    pass


def sign_context(
    secret: str,
    context: SignableContext,
    *,
    lifetime_seconds: int = DEFAULT_CONTEXT_SIGNATURE_LIFETIME_SECONDS,
    issued_at: Optional[datetime] = None,
) -> str:
    """Return the X-Schematic-Context-Sig value for a context.

    Args:
        secret: The secret API key for the environment the browser SDK's
            publishable key belongs to
        context: The logged-in user's company and user keys
        lifetime_seconds: How long the signature is valid for, in whole
            seconds, from 1 up to MAX_CONTEXT_SIGNATURE_LIFETIME_SECONDS
        issued_at: When the signature is valid from; now by default. A naive
            datetime is read as local time. Counted in whole seconds.

    Returns:
        The signature, ``iat.exp.sig``

    Raises:
        ContextSignatureError: If the secret is missing, the lifetime is out
            of range, or a key's value isn't a string
    """
    if not secret:
        raise ContextSignatureError("A secret API key is required to sign a context.")

    if (
        isinstance(lifetime_seconds, bool)
        or not isinstance(lifetime_seconds, int)
        or not 1 <= lifetime_seconds <= MAX_CONTEXT_SIGNATURE_LIFETIME_SECONDS
    ):
        raise ContextSignatureError(
            f"lifetime_seconds must be a whole number from 1 to {MAX_CONTEXT_SIGNATURE_LIFETIME_SECONDS}."
        )

    timestamp = time.time() if issued_at is None else issued_at.timestamp()
    iat = math.floor(timestamp)
    return _sign_context_at(secret, context, iat, iat + lifetime_seconds)


def _sign_context_at(secret: str, context: SignableContext, iat: int, exp: int) -> str:
    payload = f"{canonicalize_context(context)}.{iat}.{exp}"
    digest = hmac.new(secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).digest()
    sig = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return f"{iat}.{exp}.{sig}"


def canonicalize_context(context: SignableContext) -> str:
    """Encode a context the way the API does before verifying it: keys sorted
    by code point, no whitespace, ``<``, ``>``, ``&`` and ``/`` left literal,
    non-ASCII characters left raw, and U+2028 and U+2029 escaped."""
    parts = []
    # "company" sorts before "user".
    company = context.get("company")
    if company is not None:
        parts.append(f'"company":{_canonicalize_keys(company)}')
    user = context.get("user")
    if user is not None:
        parts.append(f'"user":{_canonicalize_keys(user)}')
    return "{" + ",".join(parts) + "}"


def _canonicalize_keys(keys: Mapping[str, str]) -> str:
    normalized = {}
    for name, value in keys.items():
        if not isinstance(name, str) or not isinstance(value, str):
            raise ContextSignatureError(f"The context key {name!r} and its value must be strings.")
        normalized[_normalize(name)] = _normalize(value)
    # Python compares strings by code point, the order the API sorts in.
    entries = [f"{_encode_string(name)}:{_encode_string(normalized[name])}" for name in sorted(normalized)]
    return "{" + ",".join(entries) + "}"


def _normalize(value: str) -> str:
    # The API reads a lone surrogate as U+FFFD and joins a surrogate pair into
    # the character it encodes; Python strings can hold either.
    return value.encode("utf-16-le", "surrogatepass").decode("utf-16-le", "replace")


def _encode_string(value: str) -> str:
    # json.dumps escapes quotes, backslashes and control characters the way the
    # API does. ensure_ascii=False keeps other characters raw, as the API does,
    # except U+2028 and U+2029, which the API escapes.
    encoded = json.dumps(value, ensure_ascii=False)
    return encoded.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
