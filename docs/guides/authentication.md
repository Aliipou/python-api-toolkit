# Authentication

## JWT Authentication

```python
from api_toolkit.auth import JWTAuth, require_auth

auth = JWTAuth(secret_key=settings.secret_key, algorithm="HS256")
app.add_middleware(auth.middleware)

@app.get("/api/profile")
@require_auth
async def get_profile(user: User = Depends(auth.current_user)):
    return user
```

## API Key Authentication

```python
from api_toolkit.auth import ApiKeyAuth

auth = ApiKeyAuth(
    lookup=lambda key: db.get_user_by_api_key(key),
    header="X-API-Key",
)

@app.get("/api/data")
async def get_data(user: User = Depends(auth.verify)):
    return {"user": user.id, "data": [...]}
```

## OAuth2 / OIDC

```python
from api_toolkit.auth import OIDCAuth

auth = OIDCAuth(
    issuer="https://accounts.google.com",
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
)
```

## Role-Based Access Control

```python
from api_toolkit.auth import require_role

@app.delete("/api/users/{user_id}")
@require_role("admin")
async def delete_user(user_id: int, user: User = Depends(auth.current_user)):
    await db.delete_user(user_id)
```
