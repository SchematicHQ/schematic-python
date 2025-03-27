"""Tests for webhook signature verification"""

import json
import unittest
from unittest.mock import MagicMock

from schematic.webhook_utils import (
    WEBHOOK_SIGNATURE_HEADER,
    WEBHOOK_TIMESTAMP_HEADER,
    WebhookSignatureError,
    compute_hex_signature,
    verify_signature,
    verify_webhook_signature,
)


class TestWebhookVerification(unittest.TestCase):
    """Test webhook verification functionality"""

    def setUp(self):
        """Set up test data"""
        self.webhook_secret = "test_secret"
        self.body = json.dumps({"event": "test_event"})
        self.timestamp = "1234567890"
        # Compute a valid signature for our test data
        self.valid_signature = compute_hex_signature(
            self.body, self.timestamp, self.webhook_secret
        )
        self.invalid_secret = "wrong_secret"

    def test_compute_hex_signature(self):
        """Test computing a hex signature"""
        # Test with string body
        sig1 = compute_hex_signature(self.body, self.timestamp, self.webhook_secret)
        self.assertIsInstance(sig1, str)

        # Test with bytes body
        sig2 = compute_hex_signature(self.body.encode(), self.timestamp, self.webhook_secret)
        self.assertEqual(sig1, sig2)

    def test_verify_signature_valid(self):
        """Test verifying a valid signature"""
        # Should not raise an error
        verify_signature(self.body, self.valid_signature, self.timestamp, self.webhook_secret)

    def test_verify_signature_invalid(self):
        """Test verifying an invalid signature"""
        # Invalid signature
        with self.assertRaises(WebhookSignatureError):
            verify_signature(self.body, "invalid", self.timestamp, self.webhook_secret)

        # Missing signature
        with self.assertRaises(WebhookSignatureError):
            verify_signature(self.body, "", self.timestamp, self.webhook_secret)

        # Missing timestamp
        with self.assertRaises(WebhookSignatureError):
            verify_signature(self.body, self.valid_signature, "", self.webhook_secret)

        # Tampered body
        tampered_body = json.dumps({"event": "tampered_event"})
        with self.assertRaises(WebhookSignatureError):
            verify_signature(tampered_body, self.valid_signature, self.timestamp, self.webhook_secret)

    def test_verify_webhook_signature_flask(self):
        """Test verifying a webhook signature with a Flask-like request"""
        # Create a mock Flask request
        mock_request = MagicMock()
        mock_request.headers = {
            WEBHOOK_SIGNATURE_HEADER: self.valid_signature,
            WEBHOOK_TIMESTAMP_HEADER: self.timestamp,
        }
        mock_request.get_data.return_value = self.body.encode()

        # Should not raise an error
        verify_webhook_signature(mock_request, self.webhook_secret)

    def test_verify_webhook_signature_fastapi(self):
        """Test verifying a webhook signature with a FastAPI-like request"""
        # Create a mock FastAPI request
        mock_request = MagicMock()
        mock_request.headers = {
            WEBHOOK_SIGNATURE_HEADER: self.valid_signature,
            WEBHOOK_TIMESTAMP_HEADER: self.timestamp,
        }

        # Pass the body directly since FastAPI may have already consumed it
        verify_webhook_signature(mock_request, self.webhook_secret, self.body.encode())

    def test_verify_signature_with_invalid_secret(self):
        """Test verifying a signature with an invalid (empty) secret"""
        # An empty secret should raise an error
        with self.assertRaises(WebhookSignatureError):
            verify_signature(self.body, self.valid_signature, self.timestamp, self.invalid_secret)

        # Create a signature with the invalid secret
        invalid_sig = compute_hex_signature(self.body, self.timestamp, self.invalid_secret)

        # Verify with the valid secret should fail
        with self.assertRaises(WebhookSignatureError):
            verify_signature(self.body, invalid_sig, self.timestamp, self.webhook_secret)


if __name__ == "__main__":
    unittest.main()
