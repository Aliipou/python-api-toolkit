# Retry Strategies

Handle transient failures gracefully with configurable retry logic.

## Exponential Backoff (Default)

```python
from api_toolkit import retry

@retry(max_attempts=3, backoff="exponential", base_delay=0.5)
async def fetch_data():
    return await client.get("/data")
```

Retry delays: 0.5s, 1.0s, 2.0s

## Jitter (Recommended for High Concurrency)

```python
@retry(max_attempts=5, backoff="exponential_jitter", base_delay=1.0, max_delay=30.0)
async def call_service():
    ...
```

Adds random jitter to prevent thundering herd.

## Custom Retry Condition

```python
from api_toolkit import retry, RetryOn

@retry(
    max_attempts=3,
    retry_on=RetryOn(status_codes=[429, 503], exceptions=[TimeoutError]),
    backoff="linear",
    base_delay=2.0,
)
async def resilient_call():
    ...
```
