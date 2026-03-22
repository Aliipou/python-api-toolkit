# Testing Guide

```python
import pytest
from api_toolkit.testing import TestClient

@pytest.mark.asyncio
async def test_get_users(client: TestClient):
    response = await client.get('/api/users')
    assert response.status_code == 200
```
