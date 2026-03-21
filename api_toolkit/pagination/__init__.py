"""Cursor-based and offset pagination for FastAPI."""
import base64
from typing import TypeVar, Generic, Optional
from pydantic import BaseModel


T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_prev: bool


class CursorPage(BaseModel, Generic[T]):
    items: list[T]
    next_cursor: Optional[str]
    has_next: bool


def encode_cursor(value: str) -> str:
    return base64.urlsafe_b64encode(value.encode()).decode()


def decode_cursor(cursor: str) -> str:
    return base64.urlsafe_b64decode(cursor.encode()).decode()


def paginate(items: list, page: int = 1, page_size: int = 20) -> Page:
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    return Page(
        items=items[start:end],
        total=total,
        page=page,
        page_size=page_size,
        has_next=end < total,
        has_prev=page > 1,
    )
