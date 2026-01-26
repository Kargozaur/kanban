from sqlalchemy import select
from sqlalchemy.orm import load_only
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.user_schema import UserCredentials
from backend.models.models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _get_user_by_email_helper(self, email: str) -> select:
        return select(User).where(User.email == email)

    async def _check_if_email_exists(self, email: str) -> bool:
        """method to check if email is taken or not \n
        True if exists, False if not
        """
        result = await self.session.execute(
            self._get_user_helper(email)
        )
        return result.scalar() is not None

    async def get_user_by_email(self, email: str):
        """
        Get's user. If user doesn't exists
        """
        query = self._get_user_by_email_helper(email)
        query = query.options(
            load_only(User.id, User.email, User.name)
        )
        result = await self.session.execute(query)
        row = result.scalar_one_or_none()
        if row is None:
            return {"message": "user with this email doesn't exists"}
        return row

    async def create_user(self, user_data: UserCredentials) -> dict:
        """
        Creates user if check_user is False
        """
        try:
            check_user: (
                User | None
            ) = await self._check_if_email_exists(user_data.email)
            if check_user is True:
                raise
            from_orm_user = User(
                email=user_data.email,
                name=user_data.name,
                password=user_data.password,
            )
            self.session.add(from_orm_user)
            await self.session.flush(from_orm_user)
            await self.session.commit()
            return {"result": "succesfully added user"}
        except Exception:
            self.session.rollback()
            return {"result": "an error occured"}

    async def get_user_data(self, email: str):
        query = self._get_user_by_email_helper(email)
        result = await self.session.execute(query)
        row = result.scalar_one_or_none()
        if row is None:
            return None
        return row
