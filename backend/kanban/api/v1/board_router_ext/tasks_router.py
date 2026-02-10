import json
from collections.abc import AsyncGenerator

from fastapi import APIRouter, Body, Request
from fastapi.responses import StreamingResponse

from backend.kanban.core.utility.role_enum import RoleEnum
from backend.kanban.dependencies.permission_dep import PermissionDep
from backend.kanban.dependencies.service_dependencies.tasks_dep import TaskSvcDep
from backend.kanban.event_manager.tasks_event_manager import connection_manager
from backend.kanban.schemas.columns_schema import ColumnGetFull
from backend.kanban.schemas.tasks_schema import (
    CreateTaskBase,
    MoveTask,
    TaskView,
    UpdateTaskBase,
)


def create_tasks_router() -> APIRouter:
    tasks_router = APIRouter(
        prefix="/{board_id}/columns/{column_id}/tasks",
        tags=["Board", "Columns", "Tasks"],
    )

    @tasks_router.post(
        "/add_task",
        dependencies=[PermissionDep([RoleEnum.ADMIN, RoleEnum.MEMBER])],
        status_code=201,
        description="Add task to the column",
    )
    async def add_task(
        board_id: int,
        column_id: int,
        task_svc: TaskSvcDep,
        task_data: CreateTaskBase,
        email: str | None = Body(default=None),
    ) -> TaskView:
        return await task_svc.create_task(
            board_id=board_id, column_id=column_id, task_data=task_data, email=email
        )

    @tasks_router.get(
        "/",
        dependencies=[
            PermissionDep([RoleEnum.ADMIN, RoleEnum.MEMBER, RoleEnum.VIEWER])
        ],
        status_code=200,
        description="Get full info about the column",
    )
    async def get_tasks_for_the_column(
        board_id: int, column_id: int, task_svc: TaskSvcDep
    ) -> ColumnGetFull:
        return await task_svc.get_column_with_tasks(
            board_id=board_id, column_id=column_id
        )

    @tasks_router.get(
        "/events/stream",
        dependencies=[
            PermissionDep([RoleEnum.ADMIN, RoleEnum.MEMBER, RoleEnum.VIEWER])
        ],
    )
    async def stream_board_updates(
        board_id: int, request: Request
    ) -> StreamingResponse:
        async def event_generator() -> AsyncGenerator:
            queue = await connection_manager.subscribe(board_id)
            try:
                while True:
                    if await request.is_disconnected():
                        break
                    data = await queue.get()
                    json_data = json.dumps(data)
                    yield f"data: {json_data}\n\n"
            finally:
                connection_manager.unsubscribe(board_id, queue)

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            },
        )

    @tasks_router.get(
        "/{task_id}",
        dependencies=[
            PermissionDep([RoleEnum.ADMIN, RoleEnum.MEMBER, RoleEnum.VIEWER])
        ],
        status_code=200,
        description="Get full info about the single task",
    )
    async def get_single_task(
        board_id: int,
        column_id: int,
        task_id: int,
        task_svc: TaskSvcDep,
    ) -> TaskView:
        return await task_svc.get_task(
            board_id=board_id, column_id=column_id, task_id=task_id
        )

    @tasks_router.put(
        "/{task_id}",
        dependencies=[PermissionDep([RoleEnum.ADMIN, RoleEnum.MEMBER])],
        status_code=200,
        description="Update task by either updating it data or setting a new assignee",
    )
    async def update_task(
        board_id: int,
        column_id: int,
        task_id: int,
        new_data: UpdateTaskBase,
        task_svc: TaskSvcDep,
        email: str | None = Body(default=None),
    ) -> TaskView:
        return await task_svc.update_task(
            board_id=board_id,
            column_id=column_id,
            task_id=task_id,
            new_data=new_data,
            email=email,
        )

    @tasks_router.delete(
        "/{task_id}",
        dependencies=[PermissionDep([RoleEnum.ADMIN, RoleEnum.MEMBER])],
        status_code=204,
        description="Delete task",
    )
    async def delete_task(
        board_id: int, column_id: int, task_id: int, task_svc: TaskSvcDep
    ) -> None:
        await task_svc.delete_task(
            board_id=board_id, column_id=column_id, task_id=task_id
        )

    @tasks_router.patch("/{task_id}/move")
    async def move_task(
        board_id: int,
        column_id: int,
        task_id: int,
        move_data: MoveTask,
        task_svc: TaskSvcDep,
    ) -> TaskView:
        return await task_svc.move_task(
            board_id=board_id, task_id=task_id, move_data=move_data
        )

    return tasks_router
