from decimal import Decimal
from uuid import UUID

from backend.kanban.core.decorators.read_only import read_only
from backend.kanban.core.decorators.transactional import transactional
from backend.kanban.core.exception_mappers.task_mapper import ERROR_MAP
from backend.kanban.core.utility.exception_map_keys import TaskErrorKeys
from backend.kanban.database.unit_of_work import UnitOfWork
from backend.kanban.event_manager.tasks_event_manager import ConnectionManager
from backend.kanban.models.models import User
from backend.kanban.schemas.columns_schema import ColumnGetFull
from backend.kanban.schemas.tasks_schema import (
    CreateTask,
    CreateTaskBase,
    MoveTask,
    TaskView,
    UpdateTask,
    UpdateTaskBase,
)


class TasksService:
    def __init__(self, uow: UnitOfWork, sse: ConnectionManager) -> None:
        self.uow = uow
        self.sse = sse

    async def _get_user_id(self, email: str) -> UUID:
        result: User | None = await self.uow.users.get_user_by_email(email=email)
        if result is None:
            raise ERROR_MAP[TaskErrorKeys.USER_NOT_FOUND]()
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
            raise ERROR_MAP[TaskErrorKeys.COLUMT_NOT_FOUND]()
        if (
            columns_limit_checker.wip_limit is not None
            and len(columns_limit_checker.tasks) >= columns_limit_checker.wip_limit
        ):
            raise ERROR_MAP[TaskErrorKeys.CONFLICT]()
        user_id: UUID | None = await self._get_user_id(email=email) if email else None
        full_task_data = CreateTask(**task_data.model_dump(), assignee_id=user_id)
        if not (
            result := await self.uow.tasks.create_task(
                board_id=board_id,
                column_id=column_id,
                new_task=full_task_data,
            )
        ):
            raise ERROR_MAP[TaskErrorKeys.CREATION_FAIL]()
        return TaskView.model_validate(result)

    @read_only
    async def get_column_with_tasks(
        self, board_id: int, column_id: int
    ) -> ColumnGetFull:
        if not (
            result := await self.uow.tasks.get_tasks_for_the_board(
                board_id=board_id, column_id=column_id
            )
        ):
            raise ERROR_MAP[TaskErrorKeys.BOARD_NOT_FOUND]()
        return ColumnGetFull.model_validate(result)

    @read_only
    async def get_task(self, board_id: int, column_id: int, task_id: int) -> TaskView:
        if not (
            result := await self.uow.tasks.get_task(
                board_id=board_id, column_id=column_id, task_id=task_id
            )
        ):
            raise ERROR_MAP[TaskErrorKeys.NOT_FOUND]()

        return TaskView.model_validate(result)

    @transactional
    async def update_task(
        self,
        board_id: int,
        column_id: int,
        task_id: int,
        new_data: UpdateTaskBase,
        email: str | None = None,
    ) -> TaskView:
        user_id: UUID | None = None
        if email is not None:
            user_id: UUID = await self._get_user_id(email=email)
        updated_data = UpdateTask(
            **new_data.model_dump(exclude_unset=True), assignee_id=user_id
        )
        if not (
            result := await self.uow.tasks.update_task(
                board_id=board_id,
                column_id=column_id,
                task_id=task_id,
                data_to_update=updated_data,
            )
        ):
            raise ERROR_MAP[TaskErrorKeys.NOT_FOUND]()
        return TaskView.model_validate(result)

    @transactional
    async def delete_task(self, board_id: int, column_id: int, task_id: int) -> None:
        if not await self.uow.tasks.delete_task(
            board_id=board_id, column_id=column_id, task_id=task_id
        ):
            raise ERROR_MAP[TaskErrorKeys.NOT_FOUND]()

    @transactional
    async def move_task(
        self, board_id: int, task_id: int, move_data: MoveTask
    ) -> TaskView:
        task = await self.uow.tasks._get_task_by_id(task_id)
        target_col = await self.uow.columns.get_column_with_tasks(
            board_id=board_id, column_id=move_data.target_column_id
        )
        if not task or target_col:
            raise ERROR_MAP[TaskErrorKeys.NOT_FOUND]()
        if task.column_id != move_data.target_column_id:
            if (
                target_col.wip_limit is not None  # ty:ignore[possibly-missing-attribute]
                and len(target_col.task) >= task.wip_limit  # ty:ignore[possibly-missing-attribute]
            ):
                raise ERROR_MAP[TaskErrorKeys.CONFLICT]()
        new_position = await self._calculate_new_position(move_data)
        task.column_id = move_data.target_column_id
        task.position = new_position
        await self.sse.broadcast(
            board_id,
            {
                "event": "task_moved",
                "data": {
                    "task_id": str(task.id),
                    "new_column_id": task.column_id,
                    "new_position": float(task.position),
                },
            },
        )
        return TaskView.model_validate(task)

    async def _calculate_new_position(self, move_data: MoveTask) -> Decimal:
        neighbor_ids = [
            id
            for id in [move_data.above_task_id, move_data.below_task_id]
            if id is not None
        ]

        positions = await self.uow.tasks._position_map(neighbor_ids)

        pos_above = (
            positions.get(move_data.above_task_id) if move_data.above_task_id else None
        )
        pos_below = (
            positions.get(move_data.below_task_id) if move_data.below_task_id else None
        )
        if pos_below is not None and pos_above is None:
            return pos_below / 2

        if pos_above is not None and pos_below is None:
            return pos_above + Decimal("1.0")

        if pos_above is not None and pos_below is not None:
            return (pos_above + pos_below) / 2

        return Decimal("1.0")
