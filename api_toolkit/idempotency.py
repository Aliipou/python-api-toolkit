"""Idempotency key middleware for making POST endpoints safe to retry.

Stores results keyed by Idempotency-Key header. Subsequent requests
with the same key return the cached result instead of re-executing.
"""
from __future__ import annotations
import hashlib
import json
import time
from typing import Any


class IdempotencyStore:
    """In-memory idempotency store. Replace with Redis for production."""

    def __init__(self, ttl_seconds: float = 86400) -> None:
        self._store: dict[str, tuple[Any, float]] = {}
        self._ttl = ttl_seconds

    def get(self, key: str) -> Any | None:
        entry = self._store.get(key)
        if entry is None:
            return None
        result, expires_at = entry
        if time.monotonic() > expires_at:
            del self._store[key]
            return None
        return result

    def set(self, key: str, result: Any) -> None:
        self._store[key] = (result, time.monotonic() + self._ttl)

    def make_key(self, endpoint: str, body: bytes) -> str:
        h = hashlib.sha256(endpoint.encode() + body).hexdigest()
        return h[:16]
