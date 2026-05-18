"""Tests for the caching module."""
import time
from api_toolkit.cache import InMemoryCache, make_cache_key


def test_set_and_get():
    c = InMemoryCache()
    c.set("k", {"v": 42}, ttl=60)
    assert c.get("k") == {"v": 42}


def test_missing_returns_none():
    assert InMemoryCache().get("nope") is None


def test_ttl_expiry():
    c = InMemoryCache()
    c.set("k", "v", ttl=1)
    time.sleep(1.1)
    assert c.get("k") is None


def test_delete():
    c = InMemoryCache()
    c.set("k", "v", ttl=60)
    c.delete("k")
    assert c.get("k") is None


def test_cache_key_deterministic():
    assert make_cache_key("p", "a", x=1) == make_cache_key("p", "a", x=1)


def test_cache_key_differs_on_args():
    assert make_cache_key("p", "a") != make_cache_key("p", "b")
