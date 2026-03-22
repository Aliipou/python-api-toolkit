"""Retry budget implementation to prevent retry storms in distributed systems.

A retry budget limits the total number of retries that can be in-flight
at any given time across all callers, preventing the thundering herd
problem where every client retries simultaneously.
"""
from __future__ import annotations
import threading
import time
from dataclasses import dataclass, field


@dataclass
class RetryBudget:
    """Shared retry budget across multiple callers.

    Limits total retries per time window to prevent cascading failures.

    Usage::

        budget = RetryBudget(max_retries=100, window_seconds=60)

        def call_external_service():
            for attempt in range(3):
                if not budget.acquire():
                    raise BudgetExhaustedError("Retry budget exhausted")
                try:
                    return make_request()
                except TransientError:
                    budget.record_retry()
                    continue
    """

    max_retries: int = 100
    window_seconds: float = 60.0
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    _retries: list[float] = field(default_factory=list, repr=False)

    def acquire(self) -> bool:
        """Try to acquire a retry slot. Returns False if budget is exhausted."""
        now = time.monotonic()
        with self._lock:
            self._retries = [t for t in self._retries if now - t < self.window_seconds]
            if len(self._retries) >= self.max_retries:
                return False
            self._retries.append(now)
            return True

    @property
    def available(self) -> int:
        """Number of retry slots remaining in the current window."""
        now = time.monotonic()
        with self._lock:
            active = sum(1 for t in self._retries if now - t < self.window_seconds)
            return max(0, self.max_retries - active)


class BudgetExhaustedError(Exception):
    """Raised when the retry budget is exhausted."""
