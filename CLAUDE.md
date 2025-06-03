# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository contains the Schematic Python SDK, which provides a convenient interface to the Schematic API for Python applications. The library includes type definitions for all request and response fields, and offers both synchronous and asynchronous clients powered by httpx.

## Environment Setup

```bash
# Install dependencies using Poetry
poetry install

# Or install via pip
pip install schematichq
```

## Development Commands

### Building and Testing

```bash
# Run all tests
poetry run pytest

# Run a specific test file
poetry run pytest tests/custom/test_client.py

# Run tests with specific markers (e.g. asyncio)
poetry run pytest -m asyncio

# Run tests with more verbose output
poetry run pytest -v
```

### Code Quality

```bash
# Type checking
poetry run mypy src

# Run linter
poetry run ruff check src
```

## Project Structure

- `src/schematic/` - Main SDK code
    - `client.py` - Main client entry point, provides Schematic and AsyncSchematic classes
    - `base_client.py` - Base client implementation
    - `event_buffer.py` - Buffer for events with retry logic
    - `cache.py` - Local cache implementation for flag checks
    - `core/` - Core functionality like HTTP client, API error handling
    - `webhook_utils/` - Utilities for webhook verification
    - Various services organized by API section (companies, events, features, etc.)

## Key Components

### Clients

The SDK provides two main client classes:

1. `Schematic` - Synchronous client
2. `AsyncSchematic` - Asynchronous client

Both clients have the same interface but the async client returns awaitable objects.

### Event Buffer

The SDK implements an event buffer for batching events before sending them to the API. Events are automatically flushed periodically or when the buffer is full. The event buffer includes retry logic with exponential backoff.

### Configuration

Clients can be configured with:

- Custom HTTP clients
- Flag defaults for offline/fallback mode
- Cache settings
- Timeout settings
- Retry settings

### Webhook Verification

The SDK provides utilities for verifying webhook signatures from Schematic to ensure security:

- `verify_webhook_signature` - For web request verification
- `verify_signature` - For manual signature verification
