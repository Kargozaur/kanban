from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.kanban.core.exceptions.columns_exceptions import (
    ColumnBaseException,
    ColumnNotFound,
)


def columns_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(ColumnBaseException)
    async def columns_base_exception(
        request: Request, exc: ColumnBaseException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(ColumnNotFound)
    async def board_permission_denied(
        request: Request, exc: ColumnNotFound
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
