from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from typing import AsyncGenerator
from backend.core.settings.settings import AppSettings

engine: AsyncEngine | None = None
async_session: async_sessionmaker[AsyncSession] | None = None


def create_engine(settings: AppSettings) -> AsyncEngine:
    return create_async_engine(
        url=settings.postgres.dsn,
        echo=settings.sqlalchemy.echo,
        echo_pool=settings.sqlalchemy.echo_pool,
        pool_size=settings.sqlalchemy.pool_size,
        max_overflow=settings.sqlalchemy.max_overflow,
        connect_args={"server_settings": {"client_encoding": "utf8"}},
    )


def init_db(settings: AppSettings) -> None:
    global engine, async_session
    engine = create_engine(settings)
    async_session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    assert async_session, "DB not initialized"
    async with async_session() as session:
        yield session
