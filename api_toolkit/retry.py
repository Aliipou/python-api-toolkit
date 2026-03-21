"""Exponential backoff retry decorator."""
import time, logging, functools
from typing import Callable, Type

logger = logging.getLogger(__name__)


def retry(
    exceptions: tuple = (Exception,),
    max_attempts: int = 3,
    base_delay: float = 0.5,
    max_delay: float = 30.0,
    backoff: float = 2.0,
):
    """Retry with exponential backoff. Logs each retry attempt."""
    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as exc:
                    if attempt == max_attempts:
                        raise
                    wait = min(delay, max_delay)
                    logger.warning("Retrying", extra={"fn": fn.__name__, "attempt": attempt, "wait": wait})
                    time.sleep(wait)
                    delay *= backoff
        return wrapper
    return decorator
