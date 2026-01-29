import pytest_asyncio
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from tests.db import AsyncSessionTest
from backend.main import create_app
from backend.database.session_provider import get_db
from backend.models.models import Base
from tests.db import test_engine
import uuid
from typing import Generator


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
def client() -> Generator[FastAPI]:
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client


@pytest.fixture
def unathorized_client() -> Generator[FastAPI]:
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client


@pytest.fixture
def auth_client(client):
    email = f"user_{uuid.uuid4().hex}@example.com"
    password = "SuperPassword!23"
    resp = client.post(
        "/api/v1/auth/sign_up",
        json={
            "email": email,
            "password": password,
        },
    )

    assert resp.status_code in (200, 201)
    login = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert login.status_code == 201

    return client
