"""Tests for validation helpers."""
import pytest
from api_toolkit.validation import (
    is_valid_email, is_valid_phone, is_valid_slug, sanitize_string, validate_url
)


@pytest.mark.parametrize("email", ["ali@example.com", "user+tag@sub.domain.org"])
def test_valid_emails(email):
    assert is_valid_email(email)


@pytest.mark.parametrize("email", ["notanemail", "@no.com", ""])
def test_invalid_emails(email):
    assert not is_valid_email(email)


@pytest.mark.parametrize("slug", ["hello-world", "abc-123"])
def test_valid_slugs(slug):
    assert is_valid_slug(slug)


@pytest.mark.parametrize("slug", ["Hello", "a b", "a_b", ""])
def test_invalid_slugs(slug):
    assert not is_valid_slug(slug)


def test_sanitize_truncates():
    assert len(sanitize_string("x" * 300, max_length=255)) == 255


def test_sanitize_strips():
    assert sanitize_string("  hi  ") == "hi"


def test_validate_url_valid():
    assert validate_url("https://example.com/path?q=1")


def test_validate_url_invalid():
    assert not validate_url("ftp://bad.com")
    assert not validate_url("not-a-url")
