# API Versioning

## URL Path Versioning (Recommended)

```python
from api_toolkit.versioning import VersionedAPI

api = VersionedAPI(app, prefix="/api")

@api.route("/v1/users", version=1)
async def get_users_v1():
    return {"users": [...]}  # old format

@api.route("/v2/users", version=2)
async def get_users_v2():
    return {"data": [...], "meta": {"total": 100}}  # new format
```

## Header Versioning

```python
from api_toolkit.versioning import HeaderVersionedAPI

api = HeaderVersionedAPI(app, header="API-Version", default="2024-01")

@api.version("2024-01")
async def get_users_2024_01():
    ...

@api.version("2024-06")
async def get_users_2024_06():
    ...
```

## Deprecation Notices

```python
@api.route("/v1/users", version=1, deprecated=True, sunset="2025-01-01")
async def get_users_v1():
    # Adds Deprecation and Sunset headers to response
    ...
```

Clients receive:
```
Deprecation: true
Sunset: Sun, 01 Jan 2025 00:00:00 GMT
Link: </api/v2/users>; rel="successor-version"
```
