# Middleware Guide

## Request ID Middleware

Automatically add request IDs to all requests and responses.

```python
from api_toolkit.middleware import RequestIdMiddleware

app.add_middleware(RequestIdMiddleware, header="X-Request-ID")
```

All logs within a request context automatically include the request ID.

## Timeout Middleware

```python
from api_toolkit.middleware import TimeoutMiddleware

app.add_middleware(TimeoutMiddleware, timeout=30.0)
```

Returns 504 if a request takes longer than 30 seconds.

## Correlation ID Propagation

```python
from api_toolkit.middleware import CorrelationMiddleware

app.add_middleware(CorrelationMiddleware,
    header="X-Correlation-ID",
    propagate_to=["X-Request-ID", "traceparent"]
)
```

## Combined Stack

```python
# Recommended middleware order
app.add_middleware(RequestIdMiddleware)
app.add_middleware(CorrelationMiddleware)
app.add_middleware(TimeoutMiddleware, timeout=30.0)
app.add_middleware(RateLimitMiddleware, limiter=limiter)
```
