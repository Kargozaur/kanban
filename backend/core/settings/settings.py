from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from backend.core.settings.db_settings import DbSettings, SQLAlchemy
from backend.core.settings.log_settings import LoggingSettings
from backend.core.settings.token_settings import TokenSettings


class AppSettings(BaseSettings):
    postgres: DbSettings = Field(default_factory=DbSettings)
    sqlalchemy: SQLAlchemy = Field(default_factory=SQLAlchemy)
    token: TokenSettings = Field(default_factory=TokenSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        env_nested_delimiter="_",
    )


def get_settings() -> AppSettings:
    return AppSettings()
