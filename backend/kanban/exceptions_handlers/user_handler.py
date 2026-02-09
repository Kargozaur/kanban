import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.kanban.core.exceptions.exceptions import (
    AppBaseException,
    InvalidCredentialsError,
    NotFoundError,
    PermissionError,
    TokenError,
    UserAlreadyExists,
)


logger = logging.getLogger(__name__)


def user_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(AppBaseException)
    async def base_exception(request: Request, exc: AppBaseException) -> JSONResponse:
        logging.exception("Application base exception")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=getattr(exc, "headers", None),
        )

    @app.exception_handler(InvalidCredentialsError)
    async def invalid_credentials_error(
        request: Request, exc: InvalidCredentialsError
    ) -> JSONResponse:
        logging.exception("Invalid credentials exception")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers,
        )

    @app.exception_handler(NotFoundError)
    async def not_found_exception(request: Request, exc: NotFoundError) -> JSONResponse:
        logging.exception("Not found exception")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=getattr(exc, "headers", None),
        )

    @app.exception_handler(TokenError)
    async def token_exception(request: Request, exc: TokenError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers,
        )

    @app.exception_handler(PermissionError)
    async def permission_exception(
        request: Request, exc: PermissionError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers,
        )

    @app.exception_handler(UserAlreadyExists)
    async def already_exists(request: Request, exc: UserAlreadyExists) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers,
        )
