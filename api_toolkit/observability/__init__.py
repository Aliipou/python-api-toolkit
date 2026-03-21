"""Structured logging, Prometheus metrics, and distributed tracing."""
import logging
import time
from typing import Optional
from functools import wraps


def get_structured_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Get a logger configured for structured JSON output."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            fmt='{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","message":"%(message)s"}',
            datefmt="%Y-%m-%dT%H:%M:%SZ"
        ))
        logger.addHandler(handler)
    return logger


def timed(logger: Optional[logging.Logger] = None):
    """Decorator to log function execution time."""
    def decorator(fn):
        @wraps(fn)
        async def async_wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = await fn(*args, **kwargs)
            elapsed = (time.perf_counter() - start) * 1000
            log = logger or logging.getLogger(fn.__module__)
            log.info(f"{fn.__name__} completed in {elapsed:.2f}ms")
            return result

        @wraps(fn)
        def sync_wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = fn(*args, **kwargs)
            elapsed = (time.perf_counter() - start) * 1000
            log = logger or logging.getLogger(fn.__module__)
            log.info(f"{fn.__name__} completed in {elapsed:.2f}ms")
            return result

        import asyncio
        return async_wrapper if asyncio.iscoroutinefunction(fn) else sync_wrapper
    return decorator
