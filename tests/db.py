from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from sqlalchemy.pool import NullPool

test_db_url = "sqlite+aiosqlite:///./test.db"
test_engine = create_async_engine(url=test_db_url, poolclass=NullPool)
AsyncSessionTest = async_sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)
