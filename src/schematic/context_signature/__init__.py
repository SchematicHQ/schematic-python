"""Context signing for Schematic.

This module signs the context a browser SDK sends with a publishable key, for
environments that require context signatures.
"""

from .signing import (
    CONTEXT_SIGNATURE_HEADER,
    DEFAULT_CONTEXT_SIGNATURE_LIFETIME_SECONDS,
    MAX_CONTEXT_SIGNATURE_LIFETIME_SECONDS,
    ContextSignatureError,
    SignableContext,
    canonicalize_context,
    sign_context,
)

__all__ = [
    "CONTEXT_SIGNATURE_HEADER",
    "DEFAULT_CONTEXT_SIGNATURE_LIFETIME_SECONDS",
    "MAX_CONTEXT_SIGNATURE_LIFETIME_SECONDS",
    "ContextSignatureError",
    "SignableContext",
    "canonicalize_context",
    "sign_context",
]
