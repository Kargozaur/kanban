from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from contextlib import asynccontextmanager
from pydantic import ValidationError
from backend.core.settings.settings import get_settings
from backend.core.settings.log_settings import configure_logging
from backend.database import engine, init_db
from backend.core.security.password_hasher import get_hasher
from backend.core.security.token_svc import get_token_svc
from backend.core.exceptions.exceptions import (
    AppBaseException,
    InvalidCredentialsError,
    NotFoundError,
)
import logging
import traceback

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan, default_response_class=ORJSONResponse
    )

    @app.exception_handler(ValidationError)
    async def validation_error(
        request: Request, exc: ValidationError
    ):
        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "detail": "App base exception",
                "errors": exc.errors(
                    include_input=False, include_url=False
                ),
            },
        )

    @app.exception_handler(AppBaseException)
    async def base_exception(request: Request, exc: AppBaseException):
        return ORJSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=getattr(exc, "headers", None),
        )

    @app.exception_handler(InvalidCredentialsError)
    async def invalid_credentials_error(
        request: Request, exc: InvalidCredentialsError
    ):
        return ORJSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers,
        )

    @app.exception_handler(NotFoundError)
    async def not_found_exception(
        request: Request, exc: NotFoundError
    ):
        return ORJSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=getattr(exc, "headers", None),
        )

    @app.exception_handler(Exception)
    async def other_exceptions(request: Request, exc: Exception):
        traceback_str = "".join(
            traceback.format_exc(type(exc), exc, exc.__traceback__)
        )
        logging.exception(msg="Base Exception Occured")
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": traceback_str},
            headers=getattr(exc, "headers", None),
        )

    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    pass_hasher = get_hasher()
    token_svc = get_token_svc(settings)
    configure_logging(level=settings.logging.level)
    init_db(settings)
    app.state.settings = settings
    app.state.hasher = pass_hasher
    app.state.token = token_svc
    yield
    if engine:
        await engine.dispose()
