from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from backend.core.settings.settings import AppSettings


def create_engine(settings: AppSettings) -> AsyncEngine:
    return create_async_engine(
        url=settings.postgres.dsn,
        echo=settings.sqlalchemy.echo,
        echo_pool=settings.sqlalchemy.echo_pool,
        pool_size=settings.sqlalchemy.pool_size,
        max_overflow=settings.sqlalchemy.max_overflow,
        connect_args={"server_settings": {"client_encoding": "utf8"}},
    )


def init_db(
    settings: AppSettings,
) -> tuple[AsyncEngine, async_sessionmaker]:
    engine = create_engine(settings)
    async_session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
    return engine, async_session
