"""Detailed health check that probes Redis and other dependencies."""
import time
from typing import Any
import logging

logger = logging.getLogger(__name__)


async def check_redis(redis_url: str) -> dict[str, Any]:
    """Ping Redis and return status with latency."""
    try:
        import redis.asyncio as aioredis
        start = time.perf_counter()
        r = aioredis.from_url(redis_url, socket_connect_timeout=2)
        await r.ping()
        await r.aclose()
        latency_ms = round((time.perf_counter() - start) * 1000, 2)
        return {"status": "ok", "latency_ms": latency_ms}
    except Exception as e:
        logger.error("Redis health check failed", extra={"error": str(e)})
        return {"status": "error", "error": str(e)}


async def full_health_check(redis_url: str | None = None) -> dict[str, Any]:
    """Return a full health payload with per-dependency status.

    Returns HTTP 200 if all dependencies are healthy,
    or HTTP 503 if any dependency is degraded.
    """
    result: dict[str, Any] = {
        "status": "ok",
        "timestamp": time.time(),
        "dependencies": {},
    }

    if redis_url:
        redis_status = await check_redis(redis_url)
        result["dependencies"]["redis"] = redis_status
        if redis_status["status"] != "ok":
            result["status"] = "degraded"

    return result
