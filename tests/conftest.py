import uuid
from collections.abc import AsyncGenerator, Callable

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.kanban.core.security.password_hasher import get_hasher
from backend.kanban.core.security.token_svc import get_token_svc
from backend.kanban.core.settings.settings import get_settings
from backend.kanban.database.session_provider import get_db
from backend.kanban.database.unit_of_work import UnitOfWork
from backend.kanban.database.uow_provider import get_uow
from backend.kanban.main import create_app
from backend.kanban.models.models import Base
from tests.db import AsyncSessionTest, test_engine


@pytest.fixture(scope="session", autouse=True)
async def create_tables() -> AsyncGenerator:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def session() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionTest() as session:
        yield session
        async with test_engine.begin() as conn:
            for table in reversed(Base.metadata.sorted_tables):
                await conn.execute(table.delete())


@pytest.fixture
def app_factory(session: AsyncSession) -> Callable[[], FastAPI]:
    def create_conf_app() -> FastAPI:
        app = create_app()
        settings = get_settings()
        hasher = get_hasher()
        app.state.settings = settings
        app.state.hasher = hasher
        app.state.token = get_token_svc(settings)
        app.dependency_overrides[get_db] = lambda: session
        app.dependency_overrides[get_uow] = lambda: UnitOfWork(session)
        return app

    return create_conf_app


@pytest.fixture
async def client(app_factory: Callable[[], FastAPI]) -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app_factory()),
        base_url="http://test",
        follow_redirects=True,
    ) as client:
        yield client


async def register_and_login(client_instance: AsyncClient) -> AsyncClient:
    email = f"user_{uuid.uuid4().hex}@example.com"
    password = "SuperPassword!23"
    resp = await client_instance.post(
        "/api/v1/auth/sign_up",
        json={
            "email": email,
            "password": password,
        },
    )

    assert resp.status_code in (200, 201)
    login = await client_instance.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )
    token = login.json()["access_token"]
    client_instance.headers.update({"Authorization": f"Bearer {token}"})
    assert login.status_code == 201
    return client_instance


@pytest.fixture
async def auth_client(
    app_factory: Callable[[], FastAPI],
) -> AsyncGenerator[Callable[[], FastAPI]]:
    async with AsyncClient(
        transport=ASGITransport(app_factory()),
        base_url="http://test",
        follow_redirects=True,
    ) as client:
        yield await register_and_login(client)


@pytest.fixture
async def second_auth_client(
    app_factory: Callable[[], FastAPI],
) -> AsyncGenerator[Callable[[], FastAPI]]:
    async with AsyncClient(
        transport=ASGITransport(app_factory()),
        base_url="http://test",
        follow_redirects=True,
    ) as client:
        yield await register_and_login(client)
