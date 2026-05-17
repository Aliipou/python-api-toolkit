"""Async HTTP client with retry, timeout, and structured error handling."""
from __future__ import annotations
import logging
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)


class HttpClientError(Exception):
    """Raised when an HTTP request fails after all retries."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class AsyncHttpClient:
    """Async HTTP client with retry, exponential backoff, and structured logging.

    Designed for service-to-service calls where reliability matters.
    All requests are logged with method, URL, status, and duration.

    Example::

        async with AsyncHttpClient(base_url="https://api.example.com") as client:
            data = await client.get("/users/123")
            result = await client.post("/orders", json={"item_id": 42})
    """

    def __init__(
        self,
        base_url: str = "",
        timeout: float = 10.0,
        max_retries: int = 3,
        backoff: float = 0.5,
        headers: Optional[dict] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff = backoff
        self.default_headers = headers or {}

    async def __aenter__(self) -> "AsyncHttpClient":
        return self

    async def __aexit__(self, *args: Any) -> None:
        pass  # Future: close connection pool

    async def request(
        self,
        method: str,
        path: str,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> dict:
        """Execute an HTTP request with retry logic.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH).
            path: URL path (appended to base_url).
            json: Request body as dict (serialized to JSON).
            headers: Additional headers (merged with defaults).
            params: Query string parameters.

        Returns:
            Parsed JSON response body.

        Raises:
            HttpClientError: After all retries are exhausted.
        """
        url = f"{self.base_url}{path}"
        if params:
            qs = "&".join(f"{k}={v}" for k, v in params.items())
            url = f"{url}?{qs}"

        req_headers = {**self.default_headers, **(headers or {})}
        body = None
        if json is not None:
            body = __import__("json").dumps(json).encode()
            req_headers["Content-Type"] = "application/json"

        delay = self.backoff
        for attempt in range(1, self.max_retries + 1):
            start = time.perf_counter()
            try:
                # Run blocking urlopen in thread pool to not block event loop
                result = await asyncio.get_event_loop().run_in_executor(
                    None, self._execute, method, url, body, req_headers
                )
                duration_ms = round((time.perf_counter() - start) * 1000, 2)
                logger.info("http_request", extra={
                    "method": method, "url": url,
                    "status": result.get("_status", 200),
                    "duration_ms": duration_ms, "attempt": attempt,
                })
                return result
            except HttpClientError as e:
                if e.status_code and e.status_code < 500:
                    raise  # 4xx errors are not retried
                if attempt == self.max_retries:
                    raise
                logger.warning("http_retry", extra={"attempt": attempt, "url": url, "wait": delay})
                await asyncio.sleep(delay)
                delay = min(delay * 2, 30.0)

        raise HttpClientError(f"Failed after {self.max_retries} attempts: {url}")

    def _execute(self, method: str, url: str, body: Optional[bytes], headers: dict) -> dict:
        """Blocking HTTP call (runs in thread pool)."""
        req = Request(url, data=body, headers=headers, method=method)
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                content = resp.read()
                return json.loads(content) if content else {}
        except HTTPError as e:
            raise HttpClientError(str(e), status_code=e.code)
        except URLError as e:
            raise HttpClientError(f"Connection error: {e}")

    async def get(self, path: str, **kwargs: Any) -> dict:
        return await self.request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs: Any) -> dict:
        return await self.request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs: Any) -> dict:
        return await self.request("PUT", path, **kwargs)

    async def delete(self, path: str, **kwargs: Any) -> dict:
        return await self.request("DELETE", path, **kwargs)

    async def patch(self, path: str, **kwargs: Any) -> dict:
        return await self.request("PATCH", path, **kwargs)
