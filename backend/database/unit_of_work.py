from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from backend.services.repositories.board_repo import BoardRepository
from backend.services.repositories.columns_repo import ColumnsRepo
from backend.services.repositories.member_repo import MemberRepo
from backend.services.repositories.user_repo import UserRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepository(self.session)
        self.boards = BoardRepository(self.session)
        self.member = MemberRepo(self.session)
        self.columns = ColumnsRepo(self.session)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: BaseException | None,
    ) -> None:
        if exc_type:
            await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
