from functools import lru_cache

from pydantic import AliasChoices, Field
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
        extra="ignore",
    )

    project_name: str = Field(
        default="EV Optimization",
        description="Application name",
        validation_alias=AliasChoices("APP_NAME", "PROJECT_NAME"),
    )

    app_version: str = Field(
        default="0.1.0",
        description="Application version",
    )

    environment: str = Field(
        default="development",
        description="Application environment",
        validation_alias=AliasChoices("ENV", "ENVIRONMENT"),
    )

    database_url: str = Field(
        default="postgresql+psycopg2:///ev_truck",
        validation_alias="DATABASE_URL",
        description="SQLAlchemy PostgreSQL connection URL",
    )

    google_sheet_id: str | None = Field(
        default=None,
        validation_alias="GOOGLE_SHEET_ID",
    )

    google_sheet_range: str = Field(
        default="vehicle_readings!A:Z",
        validation_alias="GOOGLE_SHEET_RANGE",
    )

    google_application_credentials: str | None = Field(
        default=None,
        validation_alias="GOOGLE_APPLICATION_CREDENTIALS",
    )


@lru_cache
def get_settings() -> Settings:
    """Return application settings."""
    return Settings()
