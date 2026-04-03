# SDK E2E Test App for schematic-python.
#
# A lightweight HTTP server implementing the standard test app contract
# defined in the SDK E2E spec (SchematicHQ/actions/sdk-e2e).
#
# The E2E harness calls POST /configure after startup to pass an
# env-scoped API key, then runs assertions against the other endpoints.
#
# Usage:
#     python testapp/app.py

import asyncio
import json
import logging
import os
import signal
import sys
from typing import Any, Dict, Optional

from aiohttp import web

# Ensure the local src/ is importable when running from the repo root.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from schematic.client import (  # noqa: E402
    AsyncSchematic,
    AsyncSchematicConfig,
    DataStreamConfig,
)
from schematic.cache import LocalCache, RedisCache  # noqa: E402

logger = logging.getLogger("testapp")

CACHE_TTL_MS = 2000  # Short TTL for E2E — tests sleep past this to verify cache expiration


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

client: Optional[AsyncSchematic] = None
current_config: Dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_config_string(key: str) -> str:
    return current_config.get(key, "") or ""


def get_config_bool(key: str) -> bool:
    return bool(current_config.get(key, False))


def get_map_from_body(body: Dict[str, Any], key: str) -> Optional[Dict[str, str]]:
    raw = body.get(key)
    if not isinstance(raw, dict):
        return None
    return {k: str(v) for k, v in raw.items()}


# ---------------------------------------------------------------------------
# Route handlers
# ---------------------------------------------------------------------------

async def handle_health(request: web.Request) -> web.Response:
    status = "waiting" if client is None else "configured"
    return web.json_response({
        "status": status,
        "config": {
            "offline": get_config_bool("offline"),
            "useDataStream": get_config_bool("useDataStream"),
            "cacheTtlMs": CACHE_TTL_MS,
        },
    })


async def handle_configure(request: web.Request) -> web.Response:
    global client, current_config

    try:
        config = await request.json()
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=400)

    # Close existing client
    if client is not None:
        try:
            await client.shutdown()
        except Exception:
            pass

    current_config = config
    api_key = get_config_string("apiKey")

    cfg = AsyncSchematicConfig()
    cfg.flag_defaults = {}

    base_url = get_config_string("baseUrl")
    if base_url:
        cfg.base_url = base_url

    # Flag defaults
    raw_defaults = config.get("flagDefaults")
    if isinstance(raw_defaults, dict):
        cfg.flag_defaults = {k: bool(v) for k, v in raw_defaults.items()}

    # Offline mode
    if get_config_bool("offline"):
        cfg.offline = True

    # Cache configuration
    redis_url = get_config_string("redisUrl")
    if get_config_bool("noCache"):
        cfg.cache_providers = []
    else:
        # Use local cache with short TTL for flag check cache.
        # The sync CacheProvider interface does not support Redis directly;
        # Redis is used via DataStream cache providers below.
        cfg.cache_providers = [LocalCache(ttl=CACHE_TTL_MS)]

    # DataStream / Replicator
    if get_config_bool("useDataStream"):
        cfg.use_datastream = True
        ds = DataStreamConfig()
        ds.cache_ttl = CACHE_TTL_MS

        if redis_url:
            import redis.asyncio as aioredis

            redis_client = aioredis.from_url(redis_url)
            ds.company_cache = RedisCache(redis_client, default_ttl_ms=CACHE_TTL_MS)
            ds.company_lookup_cache = RedisCache(redis_client, default_ttl_ms=CACHE_TTL_MS)
            ds.user_cache = RedisCache(redis_client, default_ttl_ms=CACHE_TTL_MS)
            ds.user_lookup_cache = RedisCache(redis_client, default_ttl_ms=CACHE_TTL_MS)
            ds.flag_cache = RedisCache(redis_client, default_ttl_ms=CACHE_TTL_MS)

        replicator_url = get_config_string("replicatorUrl")
        if replicator_url:
            ds.replicator_mode = True
            ds.replicator_health_url = replicator_url + "/ready"

        cfg.datastream = ds

    client = AsyncSchematic(api_key, cfg)
    await client.initialize()

    return web.json_response({"success": True, "cacheTtlMs": CACHE_TTL_MS})


async def handle_check_flag(request: web.Request) -> web.Response:
    if client is None:
        return web.json_response({"error": "not configured"}, status=503)

    try:
        body = await request.json()
    except Exception as e:
        return web.json_response({"error": str(e)}, status=400)

    flag_key = body.get("flagKey", "")
    company = get_map_from_body(body, "company")
    user = get_map_from_body(body, "user")

    value = await client.check_flag(flag_key, company=company, user=user)
    return web.json_response({"value": value})


async def handle_identify(request: web.Request) -> web.Response:
    if client is None:
        return web.json_response({"error": "not configured"}, status=503)

    try:
        body = await request.json()
    except Exception as e:
        return web.json_response({"error": str(e)}, status=400)

    # Translate E2E contract to SDK:
    #   E2E:  { company: {k:v}, user: {k:v}, keys: {k:v} }
    #   SDK:  identify(keys, company=EventBodyIdentifyCompany(keys=...))
    keys = get_map_from_body(body, "keys") or get_map_from_body(body, "user")
    company_keys = get_map_from_body(body, "company")

    from schematic.types import EventBodyIdentifyCompany
    company_arg = EventBodyIdentifyCompany(keys=company_keys) if company_keys else None

    await client.identify(keys=keys or {}, company=company_arg)
    return web.json_response({"success": True})


async def handle_track(request: web.Request) -> web.Response:
    if client is None:
        return web.json_response({"error": "not configured"}, status=503)

    try:
        body = await request.json()
    except Exception as e:
        return web.json_response({"error": str(e)}, status=400)

    event = body.get("event", "")
    company = get_map_from_body(body, "company")
    user = get_map_from_body(body, "user")
    quantity = body.get("quantity")
    if quantity is not None:
        quantity = int(quantity)

    await client.track(event, company=company, user=user, quantity=quantity)
    return web.json_response({"success": True})


async def handle_set_flag_default(request: web.Request) -> web.Response:
    if client is None:
        return web.json_response({"error": "not configured"}, status=503)

    try:
        body = await request.json()
    except Exception as e:
        return web.json_response({"error": str(e)}, status=400)

    flag_key = body.get("flagKey", "")
    value = bool(body.get("value", False))

    client.flag_defaults[flag_key] = value
    return web.json_response({"success": True})


# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------

async def on_shutdown(app: web.Application) -> None:
    global client
    if client is not None:
        try:
            await client.shutdown()
        except Exception:
            pass
        client = None


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    port = int(os.environ.get("PORT", "8080"))

    app = web.Application()
    app.router.add_get("/health", handle_health)
    app.router.add_post("/configure", handle_configure)
    app.router.add_post("/check-flag", handle_check_flag)
    app.router.add_post("/identify", handle_identify)
    app.router.add_post("/track", handle_track)
    app.router.add_post("/set-flag-default", handle_set_flag_default)
    app.on_shutdown.append(on_shutdown)

    print(f"SDK E2E test app listening on http://localhost:{port}")
    print("Waiting for POST /configure to initialize SchematicClient...")
    web.run_app(app, host="0.0.0.0", port=port, print=None)


if __name__ == "__main__":
    main()
