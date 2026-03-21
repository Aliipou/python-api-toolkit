"""Token bucket rate limiter with Redis and in-memory backends."""
import time
import threading
from typing import Optional
from abc import ABC, abstractmethod


class RateLimiterBackend(ABC):
    @abstractmethod
    def is_allowed(self, key: str, limit: int, window: int) -> bool:
        ...


class InMemoryRateLimiter(RateLimiterBackend):
    """Thread-safe in-memory sliding window rate limiter."""

    def __init__(self):
        self._lock = threading.Lock()
        self._windows: dict[str, list[float]] = {}

    def is_allowed(self, key: str, limit: int, window: int) -> bool:
        now = time.time()
        with self._lock:
            timestamps = self._windows.get(key, [])
            # Remove old timestamps outside the window
            timestamps = [t for t in timestamps if now - t < window]
            if len(timestamps) >= limit:
                self._windows[key] = timestamps
                return False
            timestamps.append(now)
            self._windows[key] = timestamps
            return True


class RedisRateLimiter(RateLimiterBackend):
    """Redis-backed sliding window rate limiter using sorted sets."""

    def __init__(self, redis_client):
        self.redis = redis_client

    def is_allowed(self, key: str, limit: int, window: int) -> bool:
        now = time.time()
        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(key, 0, now - window)
        pipe.zadd(key, {str(now): now})
        pipe.zcard(key)
        pipe.expire(key, window)
        results = pipe.execute()
        count = results[2]
        return count <= limit


def get_rate_limiter(backend: str = "memory", redis_url: Optional[str] = None) -> RateLimiterBackend:
    """Factory: create rate limiter from backend name."""
    if backend == "redis":
        import redis
        client = redis.from_url(redis_url or "redis://localhost:6379")
        return RedisRateLimiter(client)
    return InMemoryRateLimiter()
