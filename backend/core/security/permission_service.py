from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from uuid import UUID
from backend.core.utility.role_enum import RoleEnum
from backend.models.models import BoardMembers, Boards
from backend.core.exceptions.board_exceptions import (
    BoardPermissionDenied,
)


class PermissionService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def chech_user_board_role(
        self,
        user_id: UUID,
        board_id: int,
        requires_roles: list[RoleEnum],
    ) -> bool:
        query = (
            select(Boards.owner_id, BoardMembers.role)
            .outerjoin(
                BoardMembers,
                and_(
                    BoardMembers.board_id == Boards.id,
                    BoardMembers.user_id == user_id,
                ),
            )
            .where(Boards.id == board_id)
        )
        result = await self.session.execute(query)
        row = result.fetchone()
        owner_id, role = row
        if owner_id == user_id:
            return True
        if role in requires_roles:
            return True
        raise BoardPermissionDenied(
            "You dont have required permission"
        )
