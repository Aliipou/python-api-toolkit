# Circuit Breaker Pattern

Prevent cascade failures with the circuit breaker.

## Basic Usage

```python
from api_toolkit import CircuitBreaker

breaker = CircuitBreaker(
    failure_threshold=5,     # open after 5 consecutive failures
    recovery_timeout=30,     # try again after 30 seconds
    half_open_limit=2,       # allow 2 test requests in half-open state
)

@breaker
async def call_external_service():
    return await httpx.get("https://api.example.com/data")
```

## States

- **Closed** — Normal operation, requests pass through
- **Open** — All requests fail immediately (fast fail)
- **Half-Open** — Limited test requests to check if service recovered

## Monitoring

```python
print(breaker.state)           # "closed" | "open" | "half_open"
print(breaker.failure_count)   # consecutive failures
print(breaker.success_rate)    # rolling 60s success rate
```
