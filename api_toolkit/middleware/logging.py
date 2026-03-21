"""Request and response logging middleware with structured JSON output."""
import time
import uuid
import logging
from fastapi import Request

logger = logging.getLogger("api.access")


class RequestLoggingMiddleware:
    """Logs every request with method, path, status, duration, and request ID.

    Adds X-Request-ID header to every response for tracing.

    Usage::

        app.add_middleware(RequestLoggingMiddleware)
    """

    def __init__(self, app, log_request_body: bool = False):
        self.app = app
        self.log_request_body = log_request_body

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        request_id = str(uuid.uuid4())
        start = time.perf_counter()
        status_code = 500

        async def send_with_logging(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
                headers = dict(message.get("headers", []))
                headers[b"x-request-id"] = request_id.encode()
                message = {**message, "headers": list(headers.items())}
            await send(message)

        try:
            await self.app(scope, receive, send_with_logging)
        finally:
            duration_ms = round((time.perf_counter() - start) * 1000, 2)
            logger.info(
                "request",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status": status_code,
                    "duration_ms": duration_ms,
                    "client": request.client.host if request.client else "unknown",
                },
            )
