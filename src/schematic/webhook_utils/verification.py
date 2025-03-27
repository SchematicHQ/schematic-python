"""Webhook signature verification for Schematic.

This module provides utility functions to verify the signatures of incoming webhooks from Schematic.
It implements the same verification logic as the Go and Node.js SDKs.
"""

import hashlib
import hmac
from typing import Any, Dict, Optional, Union


# Constants for header names
WEBHOOK_SIGNATURE_HEADER = "X-Schematic-Webhook-Signature"
WEBHOOK_TIMESTAMP_HEADER = "X-Schematic-Webhook-Timestamp"


class WebhookSignatureError(Exception):
    """Exception raised for webhook signature verification errors."""
    pass


def compute_signature(body: Union[str, bytes], timestamp: str, secret: str) -> bytes:
    """Compute the HMAC-SHA256 signature for a webhook payload and timestamp.

    Args:
        body: The webhook request body as a string or bytes
        timestamp: The timestamp from the webhook request
        secret: The webhook secret

    Returns:
        The computed signature as bytes
    """
    # Convert body to bytes if it's a string
    if isinstance(body, str):
        body_bytes = body.encode('utf-8')
    else:
        body_bytes = body

    # Create the message by concatenating body and timestamp
    message = body_bytes + b"+" + timestamp.encode('utf-8')

    # Compute the HMAC-SHA256 signature
    secret_bytes = secret.encode('utf-8')
    return hmac.new(secret_bytes, message, hashlib.sha256).digest()


def compute_hex_signature(body: Union[str, bytes], timestamp: str, secret: str) -> str:
    """Compute the hex-encoded HMAC-SHA256 signature for a webhook payload and timestamp.

    Args:
        body: The webhook request body as a string or bytes
        timestamp: The timestamp from the webhook request
        secret: The webhook secret

    Returns:
        The computed signature as a hex-encoded string
    """
    signature = compute_signature(body, timestamp, secret)
    return signature.hex()


def verify_signature(
    body: Union[str, bytes],
    signature: str,
    timestamp: str,
    secret: str
) -> None:
    """Verify the signature of a webhook request.

    Args:
        body: The webhook request body as a string or bytes
        signature: The signature from the webhook request headers
        timestamp: The timestamp from the webhook request headers
        secret: The webhook secret

    Raises:
        WebhookSignatureError: If the signature is invalid
    """
    # Check if signature and timestamp are provided
    if not signature:
        raise WebhookSignatureError("Missing webhook signature")
    if not timestamp:
        raise WebhookSignatureError("Missing webhook timestamp")

    # Compute the expected signature
    expected_signature = compute_hex_signature(body, timestamp, secret)

    # Convert both signatures to bytes for comparison
    expected_bytes = bytes.fromhex(expected_signature)

    try:
        actual_bytes = bytes.fromhex(signature)
    except ValueError:
        raise WebhookSignatureError("Invalid signature format")

    # Compare signatures using constant-time comparison
    if not hmac.compare_digest(expected_bytes, actual_bytes):
        raise WebhookSignatureError("Invalid signature")


def verify_webhook_signature(request: Any, secret: str, body: Optional[Union[str, bytes]] = None) -> None:
    """Verify the signature of an incoming webhook request.

    This function works with various Python web frameworks by extracting the necessary
    headers and request body.

    Args:
        request: The HTTP request object (from Flask, Django, FastAPI, etc.)
        secret: The webhook secret
        body: The raw request body if already read from the request

    Raises:
        WebhookSignatureError: If the signature is invalid

    Notes:
        Different web frameworks handle request bodies differently. This function
        attempts to handle these differences, but in some cases you may need to
        pass the raw body explicitly.
    """
    # Extract the signature and timestamp headers
    signature = _get_header(request, WEBHOOK_SIGNATURE_HEADER)
    timestamp = _get_header(request, WEBHOOK_TIMESTAMP_HEADER)

    # Get the request body
    if body is None:
        body = _get_request_body(request)

    # Verify the signature
    verify_signature(body, signature, timestamp, secret)


def _get_header(request: Any, header_name: str) -> str:
    """Extract a header value from a request object.

    This function attempts to handle different web frameworks' request objects.

    Args:
        request: The HTTP request object
        header_name: The name of the header to extract

    Returns:
        The header value as a string, or an empty string if not found
    """
    # Try different methods to get headers depending on the framework

    # Flask/Werkzeug style
    if hasattr(request, 'headers') and hasattr(request.headers, 'get'):
        return request.headers.get(header_name, '')

    # Django style
    if hasattr(request, 'META'):
        django_header = f'HTTP_{header_name.replace("-", "_").upper()}'
        return request.META.get(django_header, '')

    # FastAPI/Starlette style
    if hasattr(request, 'headers') and isinstance(request.headers, dict):
        return request.headers.get(header_name, '')

    # Try to treat request as a dict-like object
    try:
        return request.get(header_name, '')
    except (AttributeError, TypeError):
        pass

    # If all else fails
    return ''


def _get_request_body(request: Any) -> Union[str, bytes]:
    """Extract the body from a request object.

    This function attempts to handle different web frameworks' request objects.

    Args:
        request: The HTTP request object

    Returns:
        The request body as a string or bytes

    Raises:
        WebhookSignatureError: If the body cannot be extracted
    """
    # Flask/Werkzeug style
    if hasattr(request, 'get_data'):
        return request.get_data()

    # Django style
    if hasattr(request, 'body'):
        return request.body

    # FastAPI/Starlette style (already read body)
    if hasattr(request, '_body'):
        return request._body

    # Try common body attributes
    for attr in ['data', 'content', 'raw_body']:
        if hasattr(request, attr):
            body = getattr(request, attr)
            if body is not None:
                return body

    raise WebhookSignatureError("Could not extract request body")
