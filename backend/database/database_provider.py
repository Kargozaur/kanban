from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from typing import AsyncGenerator


class DatabaseProvider:
    """Database adapter for the lifespan"""

    def __init__(
        self, sessionmaker: async_sessionmaker[AsyncSession]
    ) -> None:
        self.sessionmaker = sessionmaker

    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.sessionmaker() as session:
            yield session
