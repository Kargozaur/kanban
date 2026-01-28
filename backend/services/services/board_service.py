from backend.services.repositories.board_repo import BoardRepository
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
import logging

logger = logging.getLogger(__name__)


class BoardService:
    def __init__(self, board_repo: BoardRepository) -> None:
        self.board_repo = board_repo

    async def create_board(
        self, owner_id: UUID, board_data: BoardCreate
    ):
        try:
            result = await self.board_repo.create_board(
                owner_id=owner_id, board_data=board_data
            )
            logging.info(f"DEBIG - result = {result}")
            return BoardGet.model_validate(result)
        except Exception as exc:
            raise BoardBaseException(f"Failed to create board: {exc}")

    async def get_boards(
        self, owner_id: UUID, pagination: Pagination
    ):
        result = await self.board_repo.get_boards(
            owner_id=owner_id, pagination=pagination
        )
        logging.info(f"DEBUG - result = {result}")
        return [BoardGet.model_validate(values) for values in result]

    async def get_board(self, owner_id: UUID, id: int):
        result = await self.board_repo.get_board(
            owner_id=owner_id, id=id
        )
        logging.info(f"DEBUG - result = {result}")
        if result is None:
            raise BoardNotFound(
                f"Board with the id {id} is not found"
            )
        return BoardFullView.model_validate(result)

    async def update_board(
        self, id: int, data_to_update: BoardUpdate
    ):
        try:
            result = await self.board_repo.update_board(
                id=id,
                data_to_update=data_to_update,
            )
            logging.info(f"DEBUG - result = {result}")
            if result is None:
                raise BoardNotFound(
                    f"Coudn't find a board with the id: {id}"
                )

            return BoardGet.model_validate(result)
        except Exception as exc:
            raise BoardBaseException(f"{exc}")

    async def delete_board(self, id: int):
        result = await self.board_repo.delete_board(id)
        logging.info(f"DEBUG - result = {result}")
        if result["result"] is False:
            raise BoardPermissionDenied(result["detail"])
        return result["detail"]
