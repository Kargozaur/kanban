from typing import Annotated

from fastapi import Depends

from backend.dependancies.uow_dep import UOWDep
from backend.services.services.tasks_service import TasksService


def get_task_svc(uow: UOWDep) -> TasksService:
    return TasksService(uow)


TaskSvcDep = Annotated[TasksService, Depends(get_task_svc)]
