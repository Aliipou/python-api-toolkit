# Configuration

```python
from fastenv import Settings

class AppConfig(Settings):
    database_url: str
    port: int = 8000
    debug: bool = False
    secret_key: str
    rate_limit_requests: int = 1000

config = AppConfig()
```
