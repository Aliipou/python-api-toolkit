# Response Caching

## In-Memory Cache

```python
from api_toolkit.cache import InMemoryCache

cache = InMemoryCache(max_size=1000, ttl=300)  # 300 second TTL

@app.get("/api/products")
@cache.cached(key_fn=lambda req: f"products:{req.query_params}")
async def get_products():
    return await db.fetch_all_products()
```

## Redis Cache

```python
from api_toolkit.cache import RedisCache

cache = RedisCache(url="redis://localhost:6379", ttl=300)

@app.get("/api/products/{product_id}")
@cache.cached(key_fn=lambda req, product_id: f"product:{product_id}")
async def get_product(product_id: int):
    return await db.get_product(product_id)
```

## Cache Invalidation

```python
# Invalidate on write
@app.post("/api/products")
async def create_product(product: ProductCreate):
    result = await db.create_product(product)
    await cache.delete(f"product:{result.id}")
    await cache.delete_pattern("products:*")
    return result
```

## Conditional Caching

```python
@cache.cached(
    key_fn=...,
    condition=lambda req: req.headers.get("Cache-Control") != "no-cache",
    ttl_fn=lambda result: 3600 if result.is_stable else 60,
)
async def dynamic_cached_endpoint():
    ...
```
