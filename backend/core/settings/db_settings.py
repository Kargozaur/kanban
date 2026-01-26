from pydantic import Field, PostgresDsn, BaseModel
from typing import Annotated
from pydantic_settings import BaseSettings, SettingsConfigDict

Port = Annotated[int, Field(..., ge=1, le=65535)]
Driver = Annotated[str, Field(default="asyncpg")]


class DbSettings(BaseSettings):
    user: str
    password: str
    host: str
    db: str
    port: Port
    driver: Driver

    model_config = SettingsConfigDict(env_prefix="POSTGRES__")

    @property
    def dsn(self) -> str:
        return str(
            PostgresDsn.build(
                scheme=f"postgresql+{self.driver}",
                username=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                path=self.db,
            )
        )


class SQLAlchemy(BaseSettings):
    echo: bool = Field(default=False)
    echo_pool: bool = Field(default=False)
    pool_size: int = Field(default=5, ge=1)
    max_overflow: int = Field(default=10, ge=0)

    model_config = SettingsConfigDict(env_prefix="SQLALCHEMY__")
