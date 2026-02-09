from collections.abc import Sequence
from uuid import UUID

from backend.kanban.core.decorators.read_only import read_only
from backend.kanban.core.decorators.transactional import transactional
from backend.kanban.core.exception_mappers.board_mapper import ERROR_MAP
from backend.kanban.core.utility.exception_map_keys import BoardErrorKeys
from backend.kanban.database.unit_of_work import UnitOfWork
from backend.kanban.models.models import Boards
from backend.kanban.schemas.board_schema import (
    BoardCreate,
    BoardFullView,
    BoardGet,
    BoardUpdate,
)
from backend.kanban.schemas.pagination_schema import Pagination


class BoardService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    @transactional
    async def create_board(self, owner_id: UUID, board_data: BoardCreate) -> BoardGet:
        if not (
            result := await self.uow.boards.create_board(
                owner_id=owner_id, board_data=board_data
            )
        ):
            raise ERROR_MAP[BoardErrorKeys.BASE]()
        return BoardGet.model_validate(result)

    @read_only
    async def get_boards(self, user_id: UUID, pagination: Pagination) -> list[BoardGet]:
        result: Sequence[Boards] = await self.uow.boards.get_boards(
            user_id=user_id, pagination=pagination
        )
        return [BoardGet.model_validate(values) for values in result]

    @read_only
    async def get_board(self, user_id: UUID, id: int) -> BoardFullView:
        if not (result := await self.uow.boards.get_board(user_id=user_id, id=id)):
            raise ERROR_MAP[BoardErrorKeys.NOT_FOUND]()
        return BoardFullView.model_validate(result)

    @transactional
    async def update_board(
        self, board_id: int, data_to_update: BoardUpdate
    ) -> BoardGet:
        if not (
            result := await self.uow.boards.update_board(
                board_id=board_id,
                data_to_update=data_to_update,
            )
        ):
            raise ERROR_MAP[BoardErrorKeys.NOT_FOUND]()
        return BoardGet.model_validate(result)

    @transactional
    async def delete_board(self, id: int) -> str:
        result: None | bool = await self.uow.boards.delete_board(id)
        if not result:
            raise ERROR_MAP[BoardErrorKeys.PERMISSION_DENIED]()
        return f"Board {id} was succesfully deleted"
