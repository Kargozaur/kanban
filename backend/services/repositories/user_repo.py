import logging

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from backend.models.models import User
from backend.schemas.user_schema import UserCredentials
from backend.services.repositories.generic_repo import BaseRepository


logger = logging.getLogger(__name__)


class UserRepository(BaseRepository[User, UserCredentials]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    def _get_user_by_email_helper(self, email: str) -> Select[tuple[User]]:
        return select(User).where(User.email == email)

    async def _check_if_email_exists(self, email: str) -> bool:
        """method to check if email is taken or not \n
        True if exists, False if not
        """
        result = await self.session.execute(self._get_user_by_email_helper(email))
        return result.scalar() is not None

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Get's user. If user exists, returns User object, if not returns None
        """
        query = self._get_user_by_email_helper(email)
        query = query.options(load_only(User.id, User.email, User.name))
        result = await self.session.execute(query)
        row: User | None = result.scalar_one_or_none()
        return row

    async def create_user(self, user_data: UserCredentials) -> User | None:
        """
        Creates user if check_user is False
        """

        if await self._check_if_email_exists(user_data.email):
            return None

        logging.info(f"Email received in the repo: {user_data.email}")
        from_orm_user = await super().create(user_data)

        return from_orm_user

    async def get_user_data(self, email: str) -> User | None:
        query = self._get_user_by_email_helper(email)
        result = await self.session.execute(query)
        if not (row := result.scalar_one_or_none()):
            return None
        return row
