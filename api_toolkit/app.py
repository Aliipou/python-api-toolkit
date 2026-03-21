"""App factory — wires middleware and error handlers into a FastAPI app."""
from fastapi import FastAPI
from api_toolkit.middleware.security import SecurityHeadersMiddleware
from api_toolkit.errors import register_error_handlers
from api_toolkit.observability import get_structured_logger

logger = get_structured_logger(__name__)


def create_app(title: str = "API", version: str = "0.1.0", debug: bool = False) -> FastAPI:
    app = FastAPI(title=title, version=version, debug=debug)
    app.add_middleware(SecurityHeadersMiddleware)
    register_error_handlers(app)

    @app.get("/health", tags=["system"])
    async def health():
        return {"status": "ok", "version": version}

    logger.info("App created", extra={"title": title})
    return app
