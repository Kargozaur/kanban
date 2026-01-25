from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from contextlib import asynccontextmanager
from backend.core.settings.settings import get_settings
from backend.database import engine, init_db


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan, default_response_class=ORJSONResponse
    )
    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    init_db(settings)
    yield
    if engine:
        await engine.dispose()
