"""Tests for the retry decorator."""
import pytest
from api_toolkit.retry import retry


def test_succeeds_first_attempt():
    calls = []
    @retry(max_attempts=3)
    def fn():
        calls.append(1)
        return "ok"
    assert fn() == "ok"
    assert len(calls) == 1


def test_retries_on_failure():
    calls = []
    @retry(exceptions=(ValueError,), max_attempts=3, base_delay=0)
    def fn():
        calls.append(1)
        if len(calls) < 3:
            raise ValueError("fail")
        return "ok"
    assert fn() == "ok"
    assert len(calls) == 3


def test_raises_after_max_attempts():
    @retry(exceptions=(RuntimeError,), max_attempts=2, base_delay=0)
    def fn():
        raise RuntimeError("always fails")
    with pytest.raises(RuntimeError):
        fn()


def test_does_not_retry_unexpected_exception():
    @retry(exceptions=(ValueError,), max_attempts=3, base_delay=0)
    def fn():
        raise TypeError("not retried")
    with pytest.raises(TypeError):
        fn()
