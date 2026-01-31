from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.models import BoardMembers
from backend.schemas.member_schema import (
    AddBoardMemberUUID,
    UpdateBoardMember,
)
from uuid import UUID


class MemberRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _query_builder(self, board_id: int, user_id: UUID):
        return select(BoardMembers).where(
            BoardMembers.user_id == user_id,
            BoardMembers.board_id == board_id,
        )

    async def _get_membership_record(
        self, board_id: int, user_id: UUID
    ):
        """Method for general use inside the repository.
        Checks if member exists inside the requested board

        Args:
            board_id (int)
            user_id (UUID)

        Returns:
            scalar result | None
        """
        query = self._query_builder(
            board_id=board_id, user_id=user_id
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def add_member(self, new_user_data: AddBoardMemberUUID):
        check_if_user_exists = await self._get_membership_record(
            board_id=new_user_data.board_id,
            user_id=new_user_data.user_id,
        )
        if check_if_user_exists:
            return False
        new_member = BoardMembers(
            board_id=new_user_data.board_id,
            user_id=new_user_data.user_id,
            role=new_user_data.role,
        )
        self.session.add(new_member)
        return True

    async def update_member_role(
        self,
        board_id: int,
        user_id: UUID,
        new_role: UpdateBoardMember,
    ):
        existing_user = await self._get_membership_record(
            board_id=board_id, user_id=user_id
        )
        if not existing_user:
            return False
        users_new_role = new_role.model_dump()
        for k, v in users_new_role.items():
            setattr(existing_user, k, v)
        await self.session.flush()
        return True

    async def delete_member_from_the_board(
        self, board_id: int, user_id: UUID
    ):
        existing_user = await self._get_membership_record(
            board_id=board_id, user_id=user_id
        )
        if not existing_user:
            return False
        await self.session.delete(existing_user)
        await self.session.flush()
        return True
