from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.core.exceptions.board_exceptions import (
    BoardBaseException,
    BoardNotFound,
    BoardPermissionDenied,
)


def board_exceptions_handler(app: FastAPI) -> None:
    @app.exception_handler(BoardBaseException)
    async def board_base_exception(
        request: Request, exc: BoardBaseException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(BoardPermissionDenied)
    async def board_permission_denied(
        request: Request, exc: BoardPermissionDenied
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(BoardNotFound)
    async def board_not_found(request: Request, exc: BoardNotFound) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
