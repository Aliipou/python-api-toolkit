# Health Checks

## Basic Health Endpoint

```python
from api_toolkit.health import HealthCheck, HealthStatus

health = HealthCheck()

@app.get("/health")
async def health_check():
    return await health.check()
```

## Adding Checks

```python
from api_toolkit.health import DatabaseCheck, RedisCheck, HttpCheck

health = HealthCheck()
health.add(DatabaseCheck(engine=db_engine, name="postgres"))
health.add(RedisCheck(url="redis://localhost:6379", name="cache"))
health.add(HttpCheck(url="https://api.stripe.com/v1", name="stripe"))
```

## Response Format

```json
{
  "status": "healthy",
  "checks": {
    "postgres": {"status": "healthy", "latency_ms": 2.1},
    "cache": {"status": "healthy", "latency_ms": 0.8},
    "stripe": {"status": "degraded", "latency_ms": 245.0, "error": "slow response"}
  },
  "timestamp": "2024-01-15T10:23:45Z"
}
```

Status codes: 200 (healthy), 207 (degraded), 503 (unhealthy).

## Kubernetes Probes

```python
@app.get("/health/live")   # liveness: is the process alive?
async def liveness(): return {"status": "ok"}

@app.get("/health/ready")  # readiness: can it handle traffic?
async def readiness(): return await health.check()
```
