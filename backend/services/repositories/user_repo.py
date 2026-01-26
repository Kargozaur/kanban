from sqlalchemy import select
from sqlalchemy.orm import load_only
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.user_schema import UserCredentials
from backend.models.models import User
import logging

logger = logging.getLogger(__name__)


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
            self._get_user_by_email_helper(email)
        )
        return result.scalar() is not None

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Get's user. If user exists, returns User object, if not returns None
        """
        query = self._get_user_by_email_helper(email)
        query = query.options(
            load_only(User.id, User.email, User.name)
        )
        result = await self.session.execute(query)
        row = result.scalar_one_or_none()
        return row

    async def create_user(self, user_data: UserCredentials) -> dict:
        """
        Creates user if check_user is False
        """

        check_user: bool = await self._check_if_email_exists(
            user_data.email
        )
        logger.info(f"DEBUG - check_user = {check_user}")
        if check_user is True:
            return {
                "result": False,
                "reason": "email already exists",
            }
        logging.info(f"Email received in the repo: {user_data.email}")
        from_orm_user = User(
            email=user_data.email,
            name=user_data.name,
            password=user_data.password,
        )
        try:
            self.session.add(from_orm_user)
            await self.session.flush()
            await self.session.commit()
            return {"result": True}
        except Exception as exc:
            await self.session.rollback()
            logging.exception(
                f"Exception occured for the {user_data.email}"
            )
            return {"result": False, "reason": str(exc)}

    async def get_user_data(self, email: str):
        query = self._get_user_by_email_helper(email)
        result = await self.session.execute(query)
        row = result.scalar_one_or_none()
        if row is None:
            return None
        return row
