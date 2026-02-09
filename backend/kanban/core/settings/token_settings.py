from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TokenSettings(BaseSettings):
    secret: str
    algorithm: str
    token_ttl: int = Field(default=60)

    model_config = SettingsConfigDict(env_prefix="TOKEN__")
