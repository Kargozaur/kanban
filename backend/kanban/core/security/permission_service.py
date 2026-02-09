from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.kanban.core.exceptions.board_exceptions import (
    BoardNotFound,
    BoardPermissionDenied,
)
from backend.kanban.core.utility.role_enum import RoleEnum
from backend.kanban.models.models import BoardMembers, Boards


class PermissionService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def check_user_board_role(
        self,
        user_id: UUID,
        board_id: int,
        required_roles: list[RoleEnum],
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
        if row is None:
            raise BoardNotFound("Board with this id is not found")
        owner_id, role = row
        if owner_id == user_id:
            return True
        if role in required_roles:
            return True
        raise BoardPermissionDenied("You dont have required permission")
