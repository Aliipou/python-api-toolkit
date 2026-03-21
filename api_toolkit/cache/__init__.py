"""Response caching with in-memory and Redis backends."""
import time
import hashlib
import json
from typing import Any, Optional
from abc import ABC, abstractmethod


class CacheBackend(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[Any]: ...
    @abstractmethod
    def set(self, key: str, value: Any, ttl: int) -> None: ...
    @abstractmethod
    def delete(self, key: str) -> None: ...


class InMemoryCache(CacheBackend):
    def __init__(self):
        self._store: dict[str, tuple[Any, float]] = {}

    def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if entry is None:
            return None
        value, expires_at = entry
        if time.time() > expires_at:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        self._store[key] = (value, time.time() + ttl)

    def delete(self, key: str) -> None:
        self._store.pop(key, None)

    def clear(self) -> None:
        self._store.clear()


class RedisCache(CacheBackend):
    def __init__(self, redis_client):
        self.redis = redis_client

    def get(self, key: str) -> Optional[Any]:
        val = self.redis.get(key)
        return json.loads(val) if val else None

    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        self.redis.setex(key, ttl, json.dumps(value))

    def delete(self, key: str) -> None:
        self.redis.delete(key)


def make_cache_key(prefix: str, *args, **kwargs) -> str:
    """Generate a deterministic cache key from arguments."""
    raw = f"{prefix}:{args}:{sorted(kwargs.items())}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def get_cache(backend: str = "memory", redis_url: Optional[str] = None) -> CacheBackend:
    if backend == "redis":
        import redis
        return RedisCache(redis.from_url(redis_url or "redis://localhost:6379"))
    return InMemoryCache()
