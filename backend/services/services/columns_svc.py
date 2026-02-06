from backend.core.decorators.read_only import read_only
from backend.core.decorators.transactional import transactional
from backend.core.exception_mappers.column_mapper import ERROR_MAP
from backend.core.utility.exception_map_keys import ColumnErrorKeys
from backend.database.unit_of_work import UnitOfWork
from backend.models.models import Columns
from backend.schemas.columns_schema import (
    ColumnCreate,
    ColumnGet,
    ColumnGetFull,
    ColumnUpdate,
)


class ColumnService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    @transactional
    async def add_column(self, board_id: int, column_data: ColumnCreate) -> ColumnGet:
        result: Columns = await self.uow.columns.add_column(
            board_id=board_id, column_data=column_data
        )
        return ColumnGet.model_validate(result)

    @read_only
    async def get_column_with_task(
        self, column_id: int, board_id: int
    ) -> ColumnGetFull:
        result: Columns | None = await self.uow.columns.get_column_with_tasks(
            column_id=column_id, board_id=board_id
        )
        return ColumnGetFull.model_validate(result)

    @transactional
    async def update_column(
        self, column_id: int, board_id: int, new_data: ColumnUpdate
    ) -> ColumnGet:
        if not (
            result := await self.uow.columns.update_column(
                column_id=column_id,
                board_id=board_id,
                new_data=new_data,
            )
        ):
            raise ERROR_MAP[ColumnErrorKeys.NOT_FOUND]()
        return ColumnGet.model_validate(result)

    @transactional
    async def drop_column(self, column_id: int, board_id: int) -> None:
        if not await self.uow.columns.drop_column(
            column_id=column_id, board_id=board_id
        ):
            raise ERROR_MAP[ColumnErrorKeys.NOT_FOUND]()
