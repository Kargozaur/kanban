from backend.core.decorators.transactional import transactional
from backend.database.unit_of_work import UnitOfWork
from backend.schemas.pagination_schema import Pagination
from backend.schemas.board_schema import (
    BoardCreate,
    BoardUpdate,
    BoardGet,
    BoardFullView,
)
from backend.core.exceptions.board_exceptions import (
    BoardBaseException,
    BoardNotFound,
    BoardPermissionDenied,
)
from uuid import UUID


class BoardService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    @transactional
    async def create_board(
        self, owner_id: UUID, board_data: BoardCreate
    ):
        result = await self.uow.boards.create_board(
            owner_id=owner_id, board_data=board_data
        )
        if not result:
            raise BoardBaseException("Could not create a board")
        return BoardGet.model_validate(result)

    @transactional
    async def get_boards(self, user_id: UUID, pagination: Pagination):
        result = await self.uow.boards.get_boards(
            user_id=user_id, pagination=pagination
        )
        return [BoardGet.model_validate(values) for values in result]

    @transactional
    async def get_board(self, user_id: UUID, id: int):
        result = await self.uow.boards.get_board(
            user_id=user_id, id=id
        )
        if not result:
            raise BoardNotFound(
                f"Board with the id {id} is not found"
            )
        return BoardFullView.model_validate(result)

    @transactional
    async def update_board(
        self, board_id: int, data_to_update: BoardUpdate
    ):
        result = await self.uow.boards.update_board(
            board_id=board_id,
            data_to_update=data_to_update,
        )
        if not result:
            raise BoardNotFound(
                f"Coudn't find a board with the id: {board_id}"
            )
        return BoardGet.model_validate(result)

    @transactional
    async def delete_board(self, id: int):
        result = await self.uow.boards.delete_board(id)
        if not result:
            raise BoardPermissionDenied(result["detail"])
        return f"Board {id} was succesfully deleted"
