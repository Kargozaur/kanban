from uuid import UUID

from sqlalchemy import Select, exists, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.utility.role_enum import RoleEnum
from backend.models.models import BoardMembers
from backend.schemas.member_schema import (
    AddBoardMemberUUID,
    UpdateMemberWithId,
)
from backend.services.repositories.generic_repo import BaseRepository


class MemberRepo(BaseRepository[BoardMembers, AddBoardMemberUUID, UpdateMemberWithId]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, BoardMembers)

    def _query_builder(
        self, board_id: int, user_id: UUID
    ) -> Select[tuple[BoardMembers]]:
        return select(BoardMembers).where(
            BoardMembers.user_id == user_id,
            BoardMembers.board_id == board_id,
        )

    def _membership_record_builder(self, board_id: int, user_id: UUID) -> Select:
        return select(
            exists().where(
                BoardMembers.board_id == board_id,
                BoardMembers.user_id == user_id,
            )
        )

    async def _existing_user(self, board_id: int, user_id: UUID) -> bool:
        result = await self.session.execute(
            self._membership_record_builder(board_id=board_id, user_id=user_id)
        )
        return bool(result.scalar())

    async def _get_membership_record(
        self, board_id: int, user_id: UUID
    ) -> BoardMembers | None:
        """Method for general use inside the repository.
        Checks if member exists inside the requested board

        Args:
            board_id (int)
            user_id (UUID)

        Returns:
            scalar result | None
        """
        query = self._query_builder(board_id=board_id, user_id=user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def _get_admin_count(self, board_id: int) -> int:
        query = select(func.count()).where(
            BoardMembers.board_id == board_id, BoardMembers.role == RoleEnum.ADMIN
        )
        result = await self.session.execute(query)
        return result.scalar() or 0

    async def add_member(
        self, board_id: int, new_user_data: AddBoardMemberUUID
    ) -> None | bool | str:
        """Method to add the member for the board.
        In cases when admin tries to assign admin role for the
        returns "conflict"
        Args:
            board_id (int)
            new_user_data (AddBoardMemberUUID):

        Returns:
            bool | str
        """
        if await self._existing_user(
            board_id=board_id,
            user_id=new_user_data.user_id,
        ):
            return None
        if new_user_data.role == RoleEnum.ADMIN:
            return "conflict"
        await super().create(new_user_data, board_id=board_id)
        return True

    async def update_member_role(
        self, member_data: UpdateMemberWithId
    ) -> None | str | BoardMembers:
        """
        Updates user role by the admin. If admin tries to assign another admin \n
        returns "conflict"
        Args:
            board_id (int)
            user_id (UUID)
            new_role (UpdateBoardMember):

        Returns:
            bool | str | str
        """
        current_member = await self.get_entity(
            board_id=member_data.id, user_id=member_data.user_id
        )
        if not current_member:
            return None
        if current_member.role == RoleEnum.ADMIN and member_data.role != RoleEnum.ADMIN:
            return "conflict"
        if member_data.role == RoleEnum.ADMIN and current_member.role != RoleEnum.ADMIN:
            return "conflict"
        new_value = await super().update(
            data_to_update=member_data,
            user_id=member_data.user_id,
            board_id=member_data.id,
        )
        if await self._get_admin_count(board_id=member_data.id) < 1:
            return None
        return new_value

    async def delete_member_from_the_board(
        self, board_id: int, user_id: UUID, current_user: UUID
    ) -> None | bool | str:
        """
        Method to delete member from the board. Action may be \n
        done only by the admin.
        Args:
            board_id (int)
            user_id (UUID)

        Returns:
            bool
        """
        member: BoardMembers | None = await self.get_entity(
            board_id=board_id, user_id=user_id
        )
        if not member:
            return None
        if current_user == user_id:
            return "conflict"
        if member.role == RoleEnum.ADMIN:
            admin_count = await self._get_admin_count(board_id=board_id)
            if admin_count <= 1:
                return "last admin"
        if not (await super().delete(board_id=board_id, user_id=user_id)):
            return None
        return True
