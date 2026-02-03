import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from backend.api.routers import create_api_router
from backend.core.security.password_hasher import get_hasher
from backend.core.security.token_svc import get_token_svc
from backend.core.settings.log_settings import configure_logging
from backend.core.settings.settings import get_settings
from backend.database.database_provider import DatabaseProvider
from backend.database.db_config import init_db
from backend.exceptions_handlers.base_exception_handler import (
    base_exception_handler,
)
from backend.exceptions_handlers.board_handler import (
    board_exceptions_handler,
)
from backend.exceptions_handlers.columns_exception_handler import (
    columns_exception_handler,
)
from backend.exceptions_handlers.member_exception_handler import (
    member_exception_handler,
)
from backend.exceptions_handlers.pydantic_handler import (
    pydantic_exceptions_handler,
)
from backend.exceptions_handlers.sqlalchemy_exception_handler import (
    sqlalchemy_handler,
)
from backend.exceptions_handlers.user_handler import (
    user_exception_handler,
)


logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """FastAPI app factory"""
    app = FastAPI(
        lifespan=lifespan,
        default_response_class=JSONResponse,
        description="""
        FastAPI backend for the Kanban app.
        App handles JWT authentication. Role management based on the
        FastAPI dependancies,
        full CRUD operations on kanban boards.
    """,
    )
    base_exception_handler(app)
    board_exceptions_handler(app)
    pydantic_exceptions_handler(app)
    user_exception_handler(app)
    member_exception_handler(app)
    columns_exception_handler(app)
    sqlalchemy_handler(app)
    app.include_router(create_api_router())

    @app.get("/")
    async def main() -> dict[str, str]:
        return {"App": "Kanban"}

    return app


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator:
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
