#!/usr/bin/env python
"""
Webhook Test Server for Schematic

This script runs a simple HTTP server that can receive webhook requests from Schematic
and verify their signatures. It's useful for testing and debugging Schematic webhooks.

Usage:
    python webhook_test_server.py [--port PORT] [--secret SECRET]

Options:
    --port PORT     Port to listen on (default: 8080)
    --secret SECRET Webhook secret (default: reads from SCHEMATIC_WEBHOOK_SECRET env var)

Examples:
    python webhook_test_server.py --port 8080 --secret my_webhook_secret

    # Or using environment variables:
    export SCHEMATIC_WEBHOOK_SECRET=my_webhook_secret
    python webhook_test_server.py

Notes:
    For testing with Schematic, you can use a tool like ngrok to expose
    your local server to the internet.
"""

import argparse
import http.server
import json
import os
import sys
from typing import Dict, Optional

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schematic.webhook_utils import (
    WEBHOOK_SIGNATURE_HEADER,
    WEBHOOK_TIMESTAMP_HEADER,
    WebhookSignatureError,
    verify_signature
)


class WebhookHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler for Schematic webhooks."""

    def __init__(self, *args, webhook_secret: Optional[str] = None, **kwargs):
        self.webhook_secret = webhook_secret
        super().__init__(*args, **kwargs)

    def do_POST(self):
        """Handle POST requests."""
        # Only handle requests to /webhook
        if self.path != "/webhook":
            self.send_response(404)
            self.end_headers()
            return

        # Read the request body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        # Log headers
        print("Headers:")
        for header, value in self.headers.items():
            print(f"  {header}: {value}")

        # Get signature and timestamp headers
        signature = self.headers.get(WEBHOOK_SIGNATURE_HEADER, "")
        timestamp = self.headers.get(WEBHOOK_TIMESTAMP_HEADER, "")

        # Verify signature if webhook secret is provided
        if self.webhook_secret:
            try:
                verify_signature(body, signature, timestamp, self.webhook_secret)
                print("✅ Signature verification successful!")
            except WebhookSignatureError as e:
                print(f"❌ Signature verification failed: {e}")
                self.send_response(401)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_response = json.dumps({"error": str(e)})
                self.wfile.write(error_response.encode('utf-8'))
                return
        else:
            print("⚠️ No webhook secret provided, skipping signature verification")

        # Log the payload
        try:
            payload = json.loads(body)
            print("\nPayload:")
            print(json.dumps(payload, indent=2))
        except json.JSONDecodeError:
            print("\nRaw body (not JSON):")
            print(body.decode('utf-8', errors='replace'))

        # Send a successful response
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = json.dumps({"status": "success"})
        self.wfile.write(response.encode('utf-8'))


def create_handler_class(webhook_secret: Optional[str]) -> type:
    """Create a handler class with the webhook secret."""
    return type(
        'WebhookHandlerWithSecret',
        (WebhookHandler,),
        {'webhook_secret': webhook_secret}
    )


def parse_args() -> Dict:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Webhook Test Server for Schematic")
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port to listen on (default: 8080)"
    )
    parser.add_argument(
        "--secret",
        type=str,
        default=os.environ.get("SCHEMATIC_WEBHOOK_SECRET"),
        help="Webhook secret (default: reads from SCHEMATIC_WEBHOOK_SECRET env var)"
    )
    return vars(parser.parse_args())


def main():
    """Run the webhook test server."""
    args = parse_args()
    port = args["port"]
    webhook_secret = args["secret"]

    if not webhook_secret:
        print("⚠️ No webhook secret provided. Signature verification will be skipped.")
        print("   Set the SCHEMATIC_WEBHOOK_SECRET environment variable or use --secret")

    handler_class = create_handler_class(webhook_secret)
    server = http.server.HTTPServer(("", port), handler_class)

    print(f"Starting webhook test server on port {port}")
    print(f"Ready to receive webhooks at http://localhost:{port}/webhook")
    print("Press Ctrl+C to stop the server")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server")
        server.server_close()


if __name__ == "__main__":
    main()