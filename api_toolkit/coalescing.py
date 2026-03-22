"""Request coalescing — deduplicate concurrent identical in-flight requests.

When multiple callers request the same resource simultaneously,
only one actual network call is made. All callers wait for and
receive the same result.

This eliminates the thundering herd on cache misses.
"""
from __future__ import annotations
import threading
from typing import Any, Callable


class RequestCoalescer:
    """Deduplicates concurrent calls with identical keys.

    Usage::

        coalescer = RequestCoalescer()

        def get_user(user_id: int) -> dict:
            def fetch():
                return db.query("SELECT * FROM users WHERE id = ?", user_id)
            return coalescer.execute(key=f"user:{user_id}", fn=fetch)
    """

    def __init__(self) -> None:
        self._in_flight: dict[str, threading.Event] = {}
        self._results: dict[str, Any] = {}
        self._errors: dict[str, Exception] = {}
        self._lock = threading.Lock()

    def execute(self, key: str, fn: Callable[[], Any]) -> Any:
        with self._lock:
            if key in self._in_flight:
                event = self._in_flight[key]
                is_leader = False
            else:
                event = threading.Event()
                self._in_flight[key] = event
                is_leader = True

        if is_leader:
            try:
                result = fn()
                self._results[key] = result
            except Exception as exc:
                self._errors[key] = exc
            finally:
                with self._lock:
                    del self._in_flight[key]
                event.set()
        else:
            event.wait()

        with self._lock:
            if key in self._errors:
                raise self._errors.pop(key)
            return self._results.pop(key, None)
