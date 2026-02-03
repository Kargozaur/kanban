import logging
from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.core.utility.role_enum import RoleEnum
from backend.models.models import BoardMembers, Boards, Columns
from backend.schemas.board_schema import (
    BoardCreate,
    BoardUpdate,
)
from backend.schemas.pagination_schema import Pagination
from backend.services.repositories.generic_repo import BaseRepository


logger = logging.getLogger(__name__)


class BoardRepository(BaseRepository[Boards, BoardCreate, BoardUpdate]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Boards)

    def _select_query_builder(
        self, user_id: UUID, id: int | None = None
    ) -> Select[tuple[Boards]]:
        query = (
            select(Boards)
            .join(
                Boards.board_members,
            )
            .where(BoardMembers.user_id == user_id)
        ).distinct()
        if id is not None:
            query = query.where(Boards.id == id)
        return query

    async def create_board(self, owner_id: UUID, board_data: BoardCreate) -> Boards:
        """
        Creates a new entity within a Boards table and BoardMembers. \n
        Sets owner as admin

        Args:
            owner_id (UUID)
            board_data (BoardCreate)

        Returns:
            orm_board
        """
        orm_board = await super().create(
            data=board_data,
            owner_id=owner_id,
        )

        owner_membership = BoardMembers(
            board_id=orm_board.id,
            user_id=owner_id,
            role=RoleEnum.ADMIN,
        )
        self.session.add(owner_membership)
        return orm_board

    async def get_boards(
        self, user_id: UUID, pagination: Pagination
    ) -> Sequence[Boards]:
        """
        Get all boards, where current user represented
        Args:
            user_id (UUID)
            pagination (Pagination): Pydantic Pagination schema

        Returns:
            Sequence[Boards] or []
        """
        query = self._select_query_builder(user_id=user_id)
        query = query.limit(pagination.limit).offset(pagination.offset)
        result = await self.session.execute(query)
        rows: Sequence[Boards] = result.scalars().all()
        return rows

    async def get_board(self, user_id: UUID, id: int) -> Boards | None:
        """
        Get full info about the board
        Args:
            owner_id (UUID):
            id (int): id of the board inside the Boards table

        Returns:
            full info about a board
        """
        query = self._select_query_builder(user_id=user_id, id=id)
        query = query.options(
            selectinload(Boards.board_members).joinedload(BoardMembers.user),
            selectinload(Boards.columns).selectinload(Columns.tasks),
        )
        logging.info(f"DEBUG - pre-result query = {query}")
        result = await self.session.execute(query)
        logging.info(f"DEBUG - result = {result}")
        row: Boards | None = result.scalar_one_or_none()

        return row

    async def update_board(
        self, board_id: int, data_to_update: BoardUpdate
    ) -> Boards | None:
        """
        Updates Boards table. User has to have Admin role. Role is managed inside
        the endpoint
        Args:
            id (int): id of the table
            data_to_update (BoardUpdate): Pydantic BoardUpdate schema

        Returns:
           None | updated_board
        """
        if not (
            board := await super().update(data_to_update=data_to_update, id=board_id)
        ):
            return None
        return board

    async def delete_board(self, id: int) -> None | bool:
        """
        Deletes board. To delete the board, user has to have Admin role. \n
        Role is managed inside the router
        Args:
            id (int): id of the table

        Returns:
            bool
        """

        if not (board := await super().delete(id=id)):
            return None

        logging.info(f"DEBUG - board = {board}")

        return True
