"""Structured error responses and exception handlers."""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import uuid

logger = logging.getLogger(__name__)


def error_response(status: int, code: str, message: str, request_id: str = None) -> dict:
    return {
        "error": {
            "code": code,
            "message": message,
            "request_id": request_id or str(uuid.uuid4()),
        }
    }


def register_error_handlers(app: FastAPI) -> None:
    """Register structured error handlers on a FastAPI app."""

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        request_id = str(uuid.uuid4())
        logger.warning("http_error", extra={"status": exc.status_code, "detail": exc.detail, "request_id": request_id})
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(exc.status_code, f"HTTP_{exc.status_code}", str(exc.detail), request_id),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        request_id = str(uuid.uuid4())
        errors = [{"field": ".".join(str(l) for l in e["loc"]), "msg": e["msg"]} for e in exc.errors()]
        logger.warning("validation_error", extra={"errors": errors, "request_id": request_id})
        return JSONResponse(
            status_code=422,
            content={"error": {"code": "VALIDATION_ERROR", "message": "Invalid request data", "details": errors, "request_id": request_id}},
        )
