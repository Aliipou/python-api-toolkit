"""Circuit breaker pattern for protecting against cascading failures."""
import time
import threading
import logging
from enum import Enum
from typing import Callable, Any

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    CLOSED = "closed"       # Normal operation
    OPEN = "open"           # Failing — reject requests immediately
    HALF_OPEN = "half_open" # Testing if service recovered


class CircuitBreakerError(Exception):
    """Raised when a call is rejected because the circuit is open."""


class CircuitBreaker:
    """Protects external service calls from cascading failures.

    Transitions:
        CLOSED -> OPEN when failure_threshold consecutive failures occur.
        OPEN -> HALF_OPEN after recovery_timeout seconds.
        HALF_OPEN -> CLOSED if the probe call succeeds.
        HALF_OPEN -> OPEN if the probe call fails.

    Example::

        breaker = CircuitBreaker(name="payment-service", failure_threshold=5)

        @breaker
        def charge_card(amount: float) -> dict:
            return payment_api.charge(amount)
    """

    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: float = 0.0
        self._lock = threading.Lock()

    @property
    def state(self) -> CircuitState:
        with self._lock:
            if self._state == CircuitState.OPEN:
                if time.time() - self._last_failure_time >= self.recovery_timeout:
                    self._state = CircuitState.HALF_OPEN
                    logger.info("Circuit half-open", extra={"breaker": self.name})
            return self._state

    def __call__(self, fn: Callable) -> Callable:
        import functools

        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            state = self.state
            if state == CircuitState.OPEN:
                raise CircuitBreakerError(
                    f"Circuit breaker [{self.name}] is OPEN — call rejected"
                )
            try:
                result = fn(*args, **kwargs)
                self._on_success()
                return result
            except CircuitBreakerError:
                raise
            except Exception as exc:
                self._on_failure(exc)
                raise

        return wrapper

    def _on_success(self) -> None:
        with self._lock:
            self._failure_count = 0
            if self._state == CircuitState.HALF_OPEN:
                self._state = CircuitState.CLOSED
                logger.info("Circuit closed", extra={"breaker": self.name})

    def _on_failure(self, exc: Exception) -> None:
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()
            if self._failure_count >= self.failure_threshold:
                self._state = CircuitState.OPEN
                logger.error(
                    "Circuit opened",
                    extra={"breaker": self.name, "failures": self._failure_count, "error": str(exc)},
                )
