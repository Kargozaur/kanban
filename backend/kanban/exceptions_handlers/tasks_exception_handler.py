from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.kanban.core.exceptions.tasks_exception import (
    TaskBaseException,
    TaskConflict,
    TaskCreationFail,
    TaskNotFound,
)


def tasks_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(TaskBaseException)
    async def task_base_handler(
        request: Request, exc: TaskBaseException
    ) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(TaskConflict)
    async def task_conflict_handler(
        request: Request, exc: TaskConflict
    ) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(TaskCreationFail)
    async def task_creation_fail_handler(
        request: Request, exc: TaskCreationFail
    ) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(TaskNotFound)
    async def task_not_found_handler(
        request: Request, exc: TaskNotFound
    ) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
