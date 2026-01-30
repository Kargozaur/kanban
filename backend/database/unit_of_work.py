from sqlalchemy.ext.asyncio import AsyncSession
from backend.services.repositories.board_repo import BoardRepository
from backend.services.repositories.user_repo import UserRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepository(self.session)
        self.boards = BoardRepository(self.session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
