from uuid import UUID

from backend.core.decorators.read_only import read_only
from backend.core.decorators.transactional import transactional
from backend.core.exceptions.board_exceptions import BoardNotFound
from backend.core.exceptions.columns_exceptions import ColumnNotFound
from backend.core.exceptions.exceptions import NotFoundError
from backend.core.exceptions.tasks_exception import (
    TaskConflict,
    TaskCreationFail,
    TaskNotFound,
)
from backend.database.unit_of_work import UnitOfWork
from backend.schemas.board_schema import BoardTaskView
from backend.schemas.tasks_schema import (
    CreateTask,
    CreateTaskBase,
    TaskView,
    UpdateTask,
)


class TasksService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def _get_user_id(self, email: str) -> UUID:
        result = await self.uow.users.get_user_by_email(email=email)
        if result is None:
            raise NotFoundError()
        return result.id

    @transactional
    async def create_task(
        self,
        board_id: int,
        column_id: int,
        task_data: CreateTaskBase,
        email: str | None = None,
    ) -> TaskView:
        if not (
            columns_limit_checker := await self.uow.columns.get_column_with_tasks(
                column_id=column_id, board_id=board_id
            )
        ):
            raise ColumnNotFound(f"Column with the id {column_id} is not found")
        if (
            columns_limit_checker.wip_limit is not None
            and len(columns_limit_checker.tasks) >= columns_limit_checker.wip_limit
        ):
            raise TaskConflict("You can not add more tasks to the column")
        user_id: UUID | None = await self._get_user_id(email=email) if email else None
        full_task_data = CreateTask(**task_data.model_dump(), assignee_id=user_id)
        if not (
            result := await self.uow.tasks.create_task(
                board_id=board_id,
                column_id=column_id,
                new_task=full_task_data,
            )
        ):
            raise TaskCreationFail("Failed to create a task")
        return TaskView.model_validate(result)

    @read_only
    async def get_board_with_tasks(
        self, board_id: int, column_id: int
    ) -> BoardTaskView:
        if not (
            result := await self.uow.tasks.get_tasks_for_the_board(
                board_id=board_id, column_id=column_id
            )
        ):
            raise BoardNotFound(f"Board with the id {board_id} not found")
        return BoardTaskView.model_validate(result)

    @read_only
    async def get_task(self, board_id: int, column_id: int, task_id: int) -> TaskView:
        if not (
            result := await self.uow.tasks.get_task(
                board_id=board_id, column_id=column_id, task_id=task_id
            )
        ):
            raise TaskNotFound(f"Task with the id {task_id} is not found")

        return TaskView.model_validate(result)

    @transactional
    async def update_task(
        self, board_id: int, column_id: int, task_id: int, new_data: UpdateTask
    ) -> TaskView:
        if not (
            result := await self.uow.tasks.update_task(
                board_id=board_id,
                column_id=column_id,
                task_id=task_id,
                data_to_update=new_data,
            )
        ):
            raise TaskNotFound(f"Task with the id {task_id} is not found")
        return TaskView.model_validate(result)

    @transactional
    async def delete_task(self, board_id: int, column_id: int, task_id: int) -> None:
        if not await self.uow.tasks.delete_task(
            board_id=board_id, column_id=column_id, task_id=task_id
        ):
            raise TaskNotFound(f"Task with the {task_id} is not found")
