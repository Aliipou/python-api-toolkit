# Error Handling

## Standard Error Responses

```python
from api_toolkit.errors import APIError, ErrorCode

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await db.get_user(user_id)
    if not user:
        raise APIError(
            code=ErrorCode.NOT_FOUND,
            message="User not found",
            details={"user_id": user_id}
        )
    return user
```

Response:
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "User not found",
    "details": {"user_id": 42},
    "request_id": "req-abc123",
    "timestamp": "2024-01-15T10:23:45Z"
  }
}
```

## Global Error Handler

```python
from api_toolkit.errors import setup_error_handlers

setup_error_handlers(app, include_stacktrace=settings.debug)
```

Handles: `APIError`, `ValidationError`, `HTTPException`, unhandled exceptions.

## Error Codes

| Code | HTTP Status | Meaning |
|---|---|---|
| `NOT_FOUND` | 404 | Resource not found |
| `UNAUTHORIZED` | 401 | Missing authentication |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `VALIDATION_ERROR` | 422 | Invalid request data |
| `RATE_LIMITED` | 429 | Rate limit exceeded |
| `SERVICE_UNAVAILABLE` | 503 | Circuit breaker open |
| `INTERNAL_ERROR` | 500 | Unexpected error |
