from typing import Annotated

from fastapi import Depends
from typing_extensions import Doc

from backend.kanban.dependencies.uow_dep import UOWDep
from backend.kanban.event_manager.tasks_event_manager import connection_manager
from backend.kanban.services.services.tasks_service import TasksService


def get_task_svc(uow: UOWDep) -> TasksService:
    return TasksService(uow, connection_manager)


TaskSvcDep = Annotated[
    TasksService,
    Depends(get_task_svc),
    Doc("Task service dependency for the tasks router"),
]
