"""Application settings, populated from environment variables.

The .env file is consulted in local development for convenience; in Docker
and in production the variables come from the runtime environment directly.
Unknown env vars are ignored so the same .env can serve multiple tools.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = (
        "postgresql+psycopg://getrawfoods:getrawfoods@localhost:5432/getrawfoods"
    )
    debug: bool = False


settings = Settings()
