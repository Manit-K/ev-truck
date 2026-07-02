from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration.

    This class loads configuration from environment variables
    or the local .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    project_name: str = Field(
        default="EV Optimization",
        description="Application name",
    )

    app_version: str = Field(
        default="0.1.0",
        description="Application version",
    )

    environment: str = Field(
        default="development",
        description="Application environment",
    )


@lru_cache
def get_settings() -> Settings:
    """Return application settings."""
    return Settings()