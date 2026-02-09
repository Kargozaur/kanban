from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class DatabaseProvider:
    """Database provider for the lifespan"""

    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        self.sessionmaker = sessionmaker

    async def session_generator(
        self,
    ) -> AsyncGenerator[AsyncSession]:
        async with self.sessionmaker() as session:
            yield session
