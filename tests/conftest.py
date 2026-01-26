import pytest_asyncio
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from tests.db import AsyncSessionTest
from backend.main import create_app
from backend.database.session_provider import get_db
from backend.models.models import Base
from tests.db import test_engine


async def override_get_db():
    async with AsyncSessionTest() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    import asyncio

    async def _create():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def _drop():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    asyncio.run(_create())
    yield
    asyncio.run(_drop())


@pytest.fixture
def client() -> FastAPI:
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client
