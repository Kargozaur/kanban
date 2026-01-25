from pydantic import Field, PostgresDsn, BaseModel
from typing import Annotated

Port = Annotated[int, Field(..., ge=1, le=65535)]
Driver = Annotated[str, Field(..., default="asyncpg")]


class DbSettings(BaseModel):
    user: str
    password: str
    host: str
    db: str
    port: Port
    driver: Driver

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


class SQLAlchemy(BaseModel):
    echo: bool = Field(default=False)
    echo_pool: bool = Field(default=False)
    pool_size: int = Field(default=5, ge=1)
    max_overflow: int = Field(default=10, ge=0)
