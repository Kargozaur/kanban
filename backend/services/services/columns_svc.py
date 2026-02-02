from backend.core.decorators.read_only import read_only
from backend.core.decorators.transactional import transactional
from backend.database.unit_of_work import UnitOfWork
from backend.schemas.columns_schema import (
    ColumnCreate,
    ColumnGet,
    ColumnUpdate,
    ColumnGetFull,
)
from backend.core.exceptions.columns_exceptions import ColumnNotFound


class ColumnService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    @transactional
    async def add_column(
        self, board_id: int, column_data: ColumnCreate
    ):
        result = await self.uow.columns.add_column(
            board_id=board_id, column_data=column_data
        )
        return ColumnGet.model_validate(result)

    @read_only
    async def get_column_with_task(
        self, column_id: int, board_id: int
    ) -> ColumnGet:
        result = await self.uow.columns.get_column_with_tasks(
            column_id=column_id, board_id=board_id
        )
        return ColumnGetFull.model_validate(result)

    @transactional
    async def update_column(
        self, column_id: int, board_id: int, new_data: ColumnUpdate
    ):
        if not (
            result := await self.uow.columns.update_column(
                column_id=column_id,
                board_id=board_id,
                new_data=new_data,
            )
        ):
            raise ColumnNotFound(
                f"Column with the id {column_id} not found"
            )
        return ColumnGet.model_validate(result)

    @transactional
    async def drop_column(self, column_id: int, board_id: int):
        if not await self.uow.columns.drop_column(
            column_id=column_id, board_id=board_id
        ):
            raise ColumnNotFound(
                f"Column with the id {column_id} not found"
            )
