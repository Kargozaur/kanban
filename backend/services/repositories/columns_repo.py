from sqlalchemy import select, Select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.models import Columns
from backend.schemas.columns_schema import ColumnCreate, ColumnUpdate
from decimal import Decimal


class ColumnsRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _query_builder(
        self, column_id: int, board_id: int
    ) -> Select[Columns]:
        return select(Columns).where(
            Columns.id == column_id, Columns.board_id == board_id
        )

    async def _new_column_position(self, board_id: int):
        query = select(func.max(Columns.position)).where(
            Columns.board_id == board_id
        )
        result = await self.session.execute(query)
        max_position = result.scalar()
        if not max_position:
            return Decimal("1.0")
        return max_position + Decimal("1.0")

    async def _get_column(
        self, column_id: int, board_id: int
    ) -> Columns | None:
        query = self._query_builder(
            column_id=column_id, board_id=board_id
        )
        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def get_column_with_tasks(
        self, column_id: int, board_id: int
    ) -> Columns | None:
        """Get full info about the column(tasks and column info)"""
        query = self._query_builder(
            column_id=column_id, board_id=board_id
        )
        query = query.options(selectinload(Columns.tasks))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def add_column(
        self, board_id: int, column_data: ColumnCreate
    ) -> Columns:
        """Creates a new column. If position is not set, sets max position + 1"""
        if not column_data.position:
            column_data.position = await self._new_column_position(
                board_id=board_id
            )
        new_column = Columns(
            board_id=board_id,
            name=column_data.name,
            position=column_data.position,
            wip_limit=column_data.wip_limit,
        )

        self.session.add(new_column)
        await self.session.flush()
        return new_column

    async def update_column(
        self, column_id: int, board_id: int, new_data: ColumnUpdate
    ) -> None | Columns:
        """
        Tries to update column. If columnt not found, returns None
        """
        if not (
            column := await self._get_column(
                column_id=column_id, board_id=board_id
            )
        ):
            return None

        data_to_update = new_data.model_dump(exclude_unset=True)
        if not data_to_update:
            return column

        for k, v in data_to_update.items():
            setattr(column, k, v)
        await self.session.flush()
        return column

    async def drop_column(
        self, column_id: int, board_id: int
    ) -> None | True:
        """Tries to delete the column. If column not found, returns None"""
        if not (
            column := await self._get_column(
                column_id=column_id, board_id=board_id
            )
        ):
            return None
        await self.session.delete(column)
        await self.session.flush()

        return True
