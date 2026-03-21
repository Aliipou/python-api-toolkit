"""Common validation helpers for API inputs."""
import re
from typing import Optional


EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")
PHONE_RE = re.compile(r"^\+?[1-9]\d{1,14}$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_RE.match(email.strip()))


def is_valid_phone(phone: str) -> bool:
    return bool(PHONE_RE.match(phone.strip()))


def is_valid_slug(slug: str) -> bool:
    return bool(SLUG_RE.match(slug))


def sanitize_string(value: str, max_length: int = 255, strip: bool = True) -> str:
    if strip:
        value = value.strip()
    return value[:max_length]


def validate_url(url: str) -> bool:
    return url.startswith(("http://", "https://")) and len(url) < 2048
