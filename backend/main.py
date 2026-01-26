from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from pydantic import ValidationError
from backend.core.settings.settings import get_settings
from backend.core.settings.log_settings import configure_logging
from backend.database.db_config import init_db
from backend.database.database_provider import DatabaseProvider
from backend.core.security.password_hasher import get_hasher
from backend.core.security.token_svc import get_token_svc
from backend.api.routers import api_router
from backend.core.exceptions.exceptions import (
    AppBaseException,
    InvalidCredentialsError,
    NotFoundError,
    TokenError,
)
import logging

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """FastAPI app factory"""
    app = FastAPI(
        lifespan=lifespan, default_response_class=JSONResponse
    )
    app.include_router(api_router)

    @app.exception_handler(ValidationError)
    async def validation_error(
        request: Request, exc: ValidationError
    ):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "detail": "Pydantic validation error",
                "errors": exc.errors(
                    include_input=False, include_url=False
                ),
            },
        )

    @app.exception_handler(AppBaseException)
    async def base_exception(request: Request, exc: AppBaseException):
        logging.exception("Application base exception")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=getattr(exc, "headers", None),
        )

    @app.exception_handler(InvalidCredentialsError)
    async def invalid_credentials_error(
        request: Request, exc: InvalidCredentialsError
    ):
        logging.exception("Invalid credentials exception")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers,
        )

    @app.exception_handler(NotFoundError)
    async def not_found_exception(
        request: Request, exc: NotFoundError
    ):
        logging.exception("Not found exception")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=getattr(exc, "headers", None),
        )

    @app.exception_handler(TokenError)
    async def token_exception(request: Request, exc: TokenError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers,
        )

    @app.exception_handler(Exception)
    async def other_exceptions(request: Request, exc: Exception):
        logging.exception(msg="Python base exception")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": exc.__class__.__name__},
            headers=getattr(exc, "headers", None),
        )

    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    pass_hasher = get_hasher()
    token_svc = get_token_svc(settings)
    configure_logging(level=settings.logging.level)
    engine, async_session_maker = init_db(settings)
    app.state.db = DatabaseProvider(async_session_maker)
    app.state.settings = settings
    app.state.hasher = pass_hasher
    app.state.token = token_svc
    yield

    await engine.dispose()
