"""Tests for async HTTP client."""
import pytest
from api_toolkit.http_client import AsyncHttpClient, HttpClientError


@pytest.mark.asyncio
async def test_client_context_manager():
    async with AsyncHttpClient(base_url="https://example.com") as client:
        assert client.base_url == "https://example.com"


@pytest.mark.asyncio
async def test_get_calls_request():
    client = AsyncHttpClient(base_url="https://api.example.com")
    called = []

    async def mock_request(method, path, **kwargs):
        called.append(method)
        return {"ok": True}

    client.request = mock_request
    result = await client.get("/test")
    assert called == ["GET"]
    assert result == {"ok": True}


@pytest.mark.asyncio
async def test_post_calls_request():
    client = AsyncHttpClient()
    called = []

    async def mock_request(method, path, **kwargs):
        called.append((method, kwargs.get("json")))
        return {}

    client.request = mock_request
    await client.post("/items", json={"name": "test"})
    assert called == [("POST", {"name": "test"})]


def test_client_default_headers():
    client = AsyncHttpClient(headers={"Authorization": "Bearer token123"})
    assert client.default_headers["Authorization"] == "Bearer token123"


def test_client_strips_trailing_slash():
    client = AsyncHttpClient(base_url="https://api.example.com/")
    assert client.base_url == "https://api.example.com"
