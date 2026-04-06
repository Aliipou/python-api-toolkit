# Rate Limiting

Protect your API from abuse with built-in rate limiters.

## Sliding Window

```python
from api_toolkit.rate_limit import SlidingWindowLimiter

limiter = SlidingWindowLimiter(requests=100, window_seconds=60)

@app.get("/api/resource")
async def endpoint(request: Request):
    client_ip = request.client.host
    if not await limiter.allow(key=client_ip):
        raise HTTPException(429, "Rate limit exceeded")
    return {"data": "..."}
```

## Token Bucket

```python
from api_toolkit.rate_limit import TokenBucketLimiter

limiter = TokenBucketLimiter(
    capacity=10,         # burst capacity
    refill_rate=1,       # tokens per second
)
```

## Redis-Backed (Distributed)

```python
from api_toolkit.rate_limit import RedisRateLimiter

limiter = RedisRateLimiter(
    redis_url="redis://localhost:6379",
    requests=1000,
    window_seconds=3600,
)
```
