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

## License

MIT
