# Observability Guide

## OpenTelemetry Integration

```python
from api_toolkit.observability import OtelMiddleware
from opentelemetry import trace

app.add_middleware(OtelMiddleware, service_name="my-api")

@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    with trace.get_tracer(__name__).start_as_current_span("fetch_user"):
        user = await db.get_user(user_id)
    return user
```

## Prometheus Metrics

```python
from api_toolkit.metrics import MetricsMiddleware, Counter, Histogram

app.add_middleware(MetricsMiddleware)  # exposes /metrics

# Custom metrics
orders_processed = Counter("orders_processed_total", ["status", "region"])
order_duration = Histogram("order_duration_seconds", buckets=[.1, .5, 1, 5])

@app.post("/orders")
async def create_order(order: Order):
    with order_duration.time():
        result = await process(order)
    orders_processed.inc(labels={"status": result.status, "region": order.region})
    return result
```

## Structured Logging

```python
from api_toolkit.logging import get_logger

logger = get_logger(__name__)

@app.get("/api/data")
async def get_data(request: Request):
    logger.info("request", path=request.url.path, method=request.method)
    # Automatically includes trace_id, request_id
```
