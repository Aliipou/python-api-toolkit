"""Typed settings from environment variables."""
import os
from dataclasses import dataclass, field


@dataclass
class Settings:
    jwt_secret: str = field(default_factory=lambda: os.environ.get("JWT_SECRET", ""))
    jwt_algorithm: str = field(default_factory=lambda: os.environ.get("JWT_ALGORITHM", "HS256"))
    jwt_expire_minutes: int = field(default_factory=lambda: int(os.environ.get("JWT_EXPIRE_MINUTES", "30")))
    redis_url: str = field(default_factory=lambda: os.environ.get("REDIS_URL", "redis://localhost:6379"))
    rate_limit_requests: int = field(default_factory=lambda: int(os.environ.get("RATE_LIMIT_REQUESTS", "60")))
    log_level: str = field(default_factory=lambda: os.environ.get("LOG_LEVEL", "INFO").upper())
    debug: bool = field(default_factory=lambda: os.environ.get("DEBUG", "false").lower() == "true")

    def validate(self) -> None:
        if not self.jwt_secret:
            raise ValueError("JWT_SECRET must be set")
        if len(self.jwt_secret) < 32:
            raise ValueError("JWT_SECRET must be at least 32 characters")


_settings = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
        _settings.validate()
    return _settings
