from decimal import Decimal
from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models.models import Boards, Tasks
from backend.schemas.tasks_schema import CreateTask, UpdateTask
from backend.services.repositories.generic_repo import BaseRepository


class TasksRepo(BaseRepository[Tasks, CreateTask, UpdateTask]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Tasks)

    def _query_builder(
        self,
        board_id: int,
        column_id: int,
        task_id: int | None = None,
        assignee_id: UUID | None = None,
    ) -> Select:
        query = select(Tasks).filter_by(board_id=board_id, column_id=column_id)
        if assignee_id:
            query = query.filter_by(assignee_id=assignee_id)
        if task_id:
            query = query.filter_by(id=task_id)
        return query

    async def create_task(
        self,
        board_id: int,
        column_id: int,
        new_task: CreateTask,
    ) -> Tasks:
        """Tries to create a task for the column
        Args:
            board_id (int)
            column_id (int)
            new_task (CreateTask)
            assignee_id (UUID | None, optional) Defaults to None.

        Returns:
            Tasks | None
        """
        if new_task.position is None:
            query = select(func.max(Tasks.position)).filter_by(column_id=column_id)
            current_max = await self.session.scalar(query) or Decimal("1.0")
            new_task.position = current_max
        result: Tasks = await super().create(
            new_task,
            board_id=board_id,
            column_id=column_id,
        )
        return result

    async def get_tasks_for_the_board(
        self, board_id: int, column_id: int
    ) -> Boards | None:
        """Gets board with the tasks
        Args:
            board_id (int)
            column_id (int)
        Returns:
            Boards | None
        """
        query = (
            select(Boards)
            .where(Boards.id == board_id)
            .options(selectinload(Boards.tasks.and_(Tasks.column_id == column_id)))
        )
        result = await self.session.execute(query)
        rows: Boards | None = result.scalar_one_or_none()
        return rows

    async def get_task(
        self, board_id: int, column_id: int, task_id: int
    ) -> Tasks | None:
        """Retrieves full information about the task

        Args:
            board_id (int)
            column_id (int)
            task_id (int)

        Returns:
            Tasks | None
        """
        query = self._query_builder(
            board_id=board_id, column_id=column_id, task_id=task_id
        )
        result = await self.session.execute(query)
        row: Tasks | None = result.scalar_one_or_none()
        return row

    async def update_task(
        self, board_id: int, column_id: int, task_id: int, data_to_update: UpdateTask
    ) -> Tasks | None:
        """Tries to update the task. Returns None if failed
        Args:
            board_id (int)
            column_id (int)
            task_id (int)
            data_to_update (UpdateTask)

        Returns:
            Tasks | None
        """
        result: Tasks | None = await super().update(
            data_to_update, board_id=board_id, column_id=column_id, id=task_id
        )
        return result

    async def delete_task(
        self, board_id: int, column_id: int, task_id: int
    ) -> bool | None:
        """Tries to delete a task from the column. If fails, returns None

        Args:
            board_id (int)
            column_id (int)
            task_id (int)

        Returns:
            bool | None
        """
        result = await super().delete(
            board_id=board_id, column_id=column_id, id=task_id
        )
        return result
