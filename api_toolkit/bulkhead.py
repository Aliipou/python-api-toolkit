"""Bulkhead pattern for isolating resources between callers.

Prevents one slow external service from consuming all thread pool
resources and starving other callers (the 'bulkhead' metaphor from
ship design — compartments that contain flooding).
"""
from __future__ import annotations
import threading
import functools
from typing import Callable, Any


class BulkheadError(Exception):
    """Raised when all bulkhead slots are in use."""


class Bulkhead:
    """Limits concurrent calls to a resource.

    Usage::

        payment_bulkhead = Bulkhead(name="payment-service", max_concurrent=10)

        @payment_bulkhead
        def charge_card(amount: float) -> dict:
            return payment_api.charge(amount)
    """

    def __init__(self, name: str, max_concurrent: int = 10) -> None:
        self.name = name
        self.max_concurrent = max_concurrent
        self._semaphore = threading.Semaphore(max_concurrent)
        self._active = 0
        self._lock = threading.Lock()

    @property
    def active_calls(self) -> int:
        return self._active

    def __call__(self, fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            acquired = self._semaphore.acquire(blocking=False)
            if not acquired:
                raise BulkheadError(
                    f"Bulkhead [{self.name}] full — "
                    f"{self.max_concurrent} concurrent calls in progress"
                )
            with self._lock:
                self._active += 1
            try:
                return fn(*args, **kwargs)
            finally:
                self._semaphore.release()
                with self._lock:
                    self._active -= 1
        return wrapper
