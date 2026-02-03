from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.core.settings.db_settings import DbSettings, SQLAlchemy
from backend.core.settings.log_settings import LoggingSettings
from backend.core.settings.token_settings import TokenSettings


class AppSettings(BaseSettings):
    postgres: DbSettings
    sqlalchemy: SQLAlchemy
    token: TokenSettings
    logging: LoggingSettings

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[3] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        env_nested_delimiter="__",
    )


def get_settings() -> AppSettings:
    return AppSettings()  # ty:ignore[missing-argument]
