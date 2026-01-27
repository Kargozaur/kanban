from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from backend.core.utility.role_enum import RoleEnum
from backend.models.models import BoardMembers


class PermissionService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def chech_user_board_role(
        self,
        user_id: UUID,
        board_id: int,
        requires_roles: list[RoleEnum],
    ) -> bool:
        query = select(BoardMembers.role).where(
            BoardMembers.user_id == user_id,
            BoardMembers.board_id == board_id,
        )
        result = await self.session.execute(query)
        role = result.scalar_one_or_none()
        if not role or role not in requires_roles:
            raise
        return True
