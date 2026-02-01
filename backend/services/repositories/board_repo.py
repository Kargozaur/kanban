from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, Select
from backend.models.models import Boards, BoardMembers, Columns
from backend.schemas.pagination_schema import Pagination
from backend.core.utility.role_enum import RoleEnum
from backend.schemas.board_schema import (
    BoardCreate,
    BoardUpdate,
)
from uuid import UUID
import logging
from typing import Sequence

logger = logging.getLogger(__name__)


class BoardRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _select_query_builder(
        self, user_id: UUID, id: int | None = None
    ) -> Select[tuple[Boards]]:
        query = select(Boards).where(Boards.owner_id == user_id)
        if id is not None:
            query = query.where(Boards.id == id)
        return query

    async def create_board(
        self, owner_id: UUID, board_data: BoardCreate
    ) -> Boards:
        """
        Creates a new entity within a Boards table and BoardMembers. \n
        Sets owner as admin

        Args:
            owner_id (UUID)
            board_data (BoardCreate)

        Returns:
            orm_board | Exception
        """
        orm_board = Boards(
            owner_id=owner_id,
            name=board_data.name,
            description=board_data.description,
        )

        self.session.add(orm_board)
        await self.session.flush()
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
        query = query.limit(pagination.limit).offset(
            pagination.offset
        )
        result = await self.session.execute(query)
        rows = result.scalars().all()
        return rows

    async def get_board(
        self, user_id: UUID, id: int
    ) -> Sequence[Boards, BoardMembers]:
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
            selectinload(Boards.board_members).joinedload(
                BoardMembers.user
            ),
            selectinload(Boards.columns).selectinload(Columns.tasks),
        )
        logging.info(f"DEBUG - pre-result query = {query}")
        result = await self.session.execute(query)
        logging.info(f"DEBUG - result = {result}")
        row = result.scalar_one_or_none()

        return row

    async def update_board(
        self, board_id: int, data_to_update: BoardUpdate
    ) -> Boards:
        """
        Updates Boards table. User has to have Admin role. Role is managed inside the endpoint
        Args:
            id (int): id of the table
            data_to_update (BoardUpdate): Pydantic BoardUpdate schema

        Returns:
           None | updated_board
        """
        if not (board := await self.session.get(Boards, board_id)):
            return None
        to_update = data_to_update.model_dump(
            exclude_unset=True, exclude_none=True
        )
        logging.info(f"DEBUG - pre-update to_update = {to_update}")
        if not to_update:
            return board
        for k, v in to_update.items():
            setattr(board, k, v)

        await self.session.flush()
        return board

    async def delete_board(self, id: int) -> bool:
        """
        Deletes board. To delete the board, user has to have Admin role. \n
        Role is managed inside the router
        Args:
            id (int): id of the table
            user_id (UUID):

        Returns:
            bool
        """

        if not (board := await self.session.get(Boards, id)):
            return False

        logging.info(f"DEBUG - board = {board}")

        await self.session.delete(board)
        await self.session.flush()
        return True
