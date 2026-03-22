# Pagination

## Cursor-Based Pagination (Recommended)

```python
from api_toolkit.pagination import CursorPage, cursor_paginate

@app.get("/api/logs", response_model=CursorPage[LogEntry])
async def get_logs(cursor: str | None = None, limit: int = 50):
    return await cursor_paginate(
        query=db.logs.select().order_by(desc("created_at")),
        cursor=cursor,
        limit=limit,
        cursor_field="id",
    )
```

Response:
```json
{
  "items": [...],
  "next_cursor": "eyJpZCI6IDEyM30=",
  "has_more": true,
  "limit": 50
}
```

## Offset Pagination

```python
from api_toolkit.pagination import Page, paginate

@app.get("/api/users", response_model=Page[User])
async def get_users(page: int = 1, size: int = 20):
    return await paginate(db.users.select(), page=page, size=size)
```

Response:
```json
{
  "items": [...],
  "total": 1234,
  "page": 1,
  "size": 20,
  "pages": 62
}
```

## Recommendation

Use cursor-based for real-time data (logs, events). Use offset for admin panels with known total counts.
