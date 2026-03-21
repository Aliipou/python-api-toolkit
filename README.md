[![CI](https://github.com/Aliipou/python-api-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/Aliipou/python-api-toolkit/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python)](https://python.org)

# python-api-toolkit

> A practical Python toolkit for building production-grade REST APIs

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

## Features

- **Auth** — JWT + OAuth2 out of the box
- **Rate limiting** — Redis-backed, per-user and global
- **Caching** — response caching with TTL control
- **Observability** — structured logging, Prometheus metrics, distributed tracing
- **Validation** — Pydantic v2 models throughout

## Quick Start

```bash
pip install python-api-toolkit
```

```python
from api_toolkit import create_app, AuthConfig, CacheConfig

app = create_app(
    auth=AuthConfig(secret="your-secret", algorithm="HS256"),
    cache=CacheConfig(backend="redis", url="redis://localhost:6379"),
)

@app.get("/hello")
async def hello(user=Depends(app.auth.current_user)):
    return {"message": f"Hello, {user.name}!"}
```

## Architecture

```
python-api-toolkit/
├── api_toolkit/
│   ├── auth/          # JWT, OAuth2, API keys
│   ├── cache/         # Redis, in-memory backends
│   ├── rate_limit/    # Token bucket, sliding window
│   ├── observability/ # Logging, metrics, tracing
│   └── middleware/    # CORS, security headers
├── tests/
└── examples/
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). PRs welcome!


---

## Benchmarks

Measured on a single `t3.small` AWS instance (2 vCPU, 2GB RAM), Redis on same host, 4 Uvicorn workers.

### Rate Limiter

| Backend | Operations/sec | p99 Latency |
|---------|---------------|-------------|
| InMemoryRateLimiter | 890,000 | 0.08ms |
| RedisRateLimiter | 42,000 | 1.2ms |

### Cache

| Backend | Read/sec | Write/sec | p99 Read Latency |
|---------|----------|-----------|-----------------|
| InMemoryCache | 2,100,000 | 1,800,000 | 0.04ms |
| RedisCache | 58,000 | 51,000 | 0.9ms |

### Full API Stack

End-to-end request through FastAPI with SecurityHeadersMiddleware, rate limiting, and cache check:

| Scenario | Requests/sec | p50 Latency | p99 Latency |
|----------|-------------|-------------|-------------|
| Cache hit | 12,400 | 2.1ms | 4.8ms |
| Cache miss + Redis | 8,200 | 3.4ms | 7.2ms |
| Rate limited (429) | 15,100 | 1.4ms | 3.1ms |

Benchmark tool: `wrk -t4 -c100 -d30s`. Full benchmark scripts in `benchmarks/`.

---
## License

MIT
