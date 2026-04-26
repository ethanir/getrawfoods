"""Application configuration loaded from environment variables.

All config goes through this module so we have a single source of truth.
Pydantic-settings validates types at startup — fail loud, fail early.
"""

from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Database
    database_url: str = Field(
        default="postgresql+psycopg://getrawfoods:devpassword@localhost:5432/getrawfoods",
        description="SQLAlchemy database URL",
    )

    # Environment
    environment: str = Field(default="development")

    # CORS — comma-separated list of allowed origins
    cors_origins: str = Field(default="http://localhost:3000")

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    # Auth (used in Phase 3+)
    jwt_secret: str = Field(default="dev-only-not-secure-change-me")
    jwt_algorithm: str = Field(default="HS256")
    jwt_access_token_minutes: int = Field(default=15)
    jwt_refresh_token_days: int = Field(default=30)

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        allowed = {"development", "staging", "production"}
        if v not in allowed:
            raise ValueError(f"environment must be one of {allowed}, got {v!r}")
        return v


settings = Settings()
