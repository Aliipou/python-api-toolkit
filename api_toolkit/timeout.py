"""Timeout decorator for wrapping external calls with a hard deadline."""
from __future__ import annotations
import concurrent.futures
import functools
from typing import Callable, Any


class TimeoutError(Exception):
    """Raised when a function exceeds its time limit."""


def timeout(seconds: float) -> Callable:
    """Decorator that enforces a hard deadline on a function call.

    Runs the function in a thread pool executor and raises TimeoutError
    if it does not complete within the specified number of seconds.

    Usage::

        @timeout(seconds=5.0)
        def call_slow_api() -> dict:
            return requests.get("https://slow-service.example.com/data").json()
    """
    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(fn, *args, **kwargs)
                try:
                    return future.result(timeout=seconds)
                except concurrent.futures.TimeoutError:
                    future.cancel()
                    raise TimeoutError(
                        f"{fn.__name__} exceeded {seconds}s deadline"
                    ) from None
        return wrapper
    return decorator
