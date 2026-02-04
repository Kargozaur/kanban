from fastapi import APIRouter, Body

from backend.core.utility.role_enum import RoleEnum
from backend.dependancies.permission_dep import PermissionDep
from backend.dependancies.tasks_dep import TaskSvcDep
from backend.schemas.board_schema import BoardTaskView
from backend.schemas.tasks_schema import (
    CreateTaskBase,
    TaskView,
    UpdateTask,
)


def create_tasks_router() -> APIRouter:
    tasks_router = APIRouter(
        prefix="/{board_id}/columns/{column_id}/tasks",
        tags=["Board", "Columns", "Tasks"],
    )

    @tasks_router.post(
        "/add_task", dependencies=[PermissionDep([RoleEnum.ADMIN, RoleEnum.MEMBER])]
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
    )
    async def get_tasks_for_the_board(
        board_id: int, column_id: int, task_svc: TaskSvcDep
    ) -> BoardTaskView:
        return await task_svc.get_board_with_tasks(
            board_id=board_id, column_id=column_id
        )

    @tasks_router.get(
        "/{task_id}",
        dependencies=[
            PermissionDep([RoleEnum.ADMIN, RoleEnum.MEMBER, RoleEnum.VIEWER])
        ],
    )
    async def get_single_task(
        board_id: int, column_id: int, task_id: int, task_svc: TaskSvcDep
    ) -> TaskView:
        return await task_svc.get_task(
            board_id=board_id, column_id=column_id, task_id=task_id
        )

    @tasks_router.patch(
        "/{task_id}", dependencies=[PermissionDep([RoleEnum.ADMIN, RoleEnum.MEMBER])]
    )
    async def update_task(
        board_id: int,
        column_id: int,
        task_id: int,
        new_data: UpdateTask,
        task_svc: TaskSvcDep,
    ) -> TaskView:
        return await task_svc.update_task(
            board_id=board_id, column_id=column_id, task_id=task_id, new_data=new_data
        )

    @tasks_router.delete(
        "/{task_id}", dependencies=[PermissionDep([RoleEnum.ADMIN, RoleEnum.MEMBER])]
    )
    async def delete_task(
        board_id: int, column_id: int, task_id: int, task_svc: TaskSvcDep
    ) -> None:
        await task_svc.delete_task(
            board_id=board_id, column_id=column_id, task_id=task_id
        )

    return tasks_router
