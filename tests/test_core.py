"""Tests for python-api-toolkit."""
import pytest
from fastapi.testclient import TestClient
from api_toolkit import create_app, AuthConfig, CacheConfig
from api_toolkit.auth import create_token, verify_token, TokenData


@pytest.fixture
def app():
    return create_app(
        auth=AuthConfig(secret="test-secret-key"),
        cache=CacheConfig(backend="memory"),
    )


@pytest.fixture
def client(app):
    return TestClient(app)


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_verify_token():
    secret = "test-secret"
    data = TokenData(user_id="user-123", email="ali@example.com", scopes=["read"])
    token = create_token(data, secret)
    decoded = verify_token(token, secret)
    assert decoded.user_id == "user-123"
    assert decoded.email == "ali@example.com"


def test_expired_token_raises():
    import time
    secret = "test-secret"
    data = TokenData(user_id="user-123")
    # Create token that expires in 0 minutes (immediate)
    token = create_token(data, secret, expires_in=-1)
    with pytest.raises(ValueError, match="expired"):
        verify_token(token, secret)
