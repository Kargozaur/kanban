from typing import Any

import pytest
from httpx import AsyncClient


@pytest.fixture
async def task_fixture(auth_client: AsyncClient) -> dict[str, Any]:
    data_board = await auth_client.post(
        "/api/v1/board/",
        json={
            "name": "Test board",
            "description": "Some description in here",
        },
    )
    board_id: int = data_board.json()["id"]
    assert data_board.status_code in (200, 201)
    assert board_id == data_board.json()["id"]
    create_column = await auth_client.post(
        f"/api/v1/board/{board_id}/columns/add",
        json={"name": "my amazing column", "position": 1, "wip_limit": 3},
    )
    column_id: int = create_column.json()["id"]
    assert create_column.status_code in (200, 201)
    assert column_id == create_column.json()["id"]
    return {"client": auth_client, "board_id": board_id, "column_id": column_id}


@pytest.fixture
async def two_members(
    auth_client: AsyncClient, second_auth_client: AsyncClient
) -> dict[str, Any]:
    data = await auth_client.post(
        "/api/v1/board/",
        json={
            "name": "Test board",
            "description": "Some description in here",
        },
    )
    assert data.status_code in (201, 200)
    board_id = data.json()["id"]
    user_data = await second_auth_client.get("/api/v1/auth/me")
    user_email = user_data.json()["email"]
    result = await auth_client.post(
        f"/api/v1/board/{board_id}/members/add",
        json={"email": user_email, "role": "viewer"},
    )
    assert result.status_code == 201
    return {
        "board_id": board_id,
        "member_email": user_email,
        "owner_client": auth_client,
        "member_client": second_auth_client,
    }


async def test_task_creation(task_fixture: dict[str, Any]) -> None:
    client: AsyncClient = task_fixture["client"]
    task_creation = await client.post(
        f"/api/v1/board/{task_fixture['board_id']}/columns/{task_fixture['column_id']}/tasks/add_task",
        json={
            "task_data": {
                "title": "Add test",
                "description": "Description to the test",
                "position": 1,
            }
        },
    )

    task_data = task_creation.json()
    assert task_creation.status_code == 201
    assert task_data["title"] == "Add test"


@pytest.fixture
async def bulk_creation(task_fixture: dict[str, Any]) -> AsyncClient:
    client: AsyncClient = task_fixture["client"]
    await client.post(
        f"/api/v1/board/{task_fixture['board_id']}/columns/{task_fixture['column_id']}/tasks/add_task",
        json={
            "task_data": {
                "title": "Add test",
                "description": "Description to the test",
                "position": 1,
            }
        },
    )
    await client.post(
        f"/api/v1/board/{task_fixture['board_id']}/columns/{task_fixture['column_id']}/tasks/add_task",
        json={
            "task_data": {
                "title": "Add test2",
                "description": "Description to the test",
                "position": 2,
            }
        },
    )
    await client.post(
        f"/api/v1/board/{task_fixture['board_id']}/columns/{task_fixture['column_id']}/tasks/add_task",
        json={
            "task_data": {
                "title": "Add test2",
                "description": "Description to the test",
                "position": 3,
            }
        },
    )
    return client


async def test_task_creation_fail(
    task_fixture: dict[str, Any], bulk_creation: None
) -> None:
    client: AsyncClient = task_fixture["client"]
    result = await client.post(
        f"/api/v1/board/{task_fixture['board_id']}/columns/{task_fixture['column_id']}/tasks/add_task",
        json={
            "task_data": {
                "title": "Add test2",
                "description": "Description to the test",
                "position": 4,
            }
        },
    )
    assert result.status_code == 409


async def test_delete_task(
    bulk_creation: AsyncClient, task_fixture: dict[str, Any]
) -> None:
    client = bulk_creation
    existing_task = await client.get(
        f"/api/v1/board/{task_fixture['board_id']}/columns/{task_fixture['column_id']}/tasks/{2}"
    )
    assert existing_task.status_code == 200
    task_id: int = existing_task.json()["id"]
    result = await client.delete(
        f"/api/v1/board/{task_fixture['board_id']}/columns/{task_fixture['column_id']}/tasks/{task_id}"
    )
    assert result.status_code == 204


async def test_put_task(
    bulk_creation: AsyncClient, task_fixture: dict[str, Any]
) -> None:
    client = bulk_creation
    existing_task = await client.get(
        f"/api/v1/board/{task_fixture['board_id']}/columns/{task_fixture['column_id']}/tasks/{2}"
    )
    assert existing_task.status_code == 200
    task_id: int = existing_task.json()["id"]
    result = await client.put(
        f"/api/v1/board/{task_fixture['board_id']}/columns/{task_fixture['column_id']}/tasks/{task_id}",
        json={
            "new_data": {
                "title": "Super new test name",
                "description": "Very new name of the test",
                "position": 5,
            }
        },
    )
    assert result.status_code == 200
    assert task_id == result.json()["id"]


async def test_assign_user_to_the_task(
    two_members: dict[str, Any],
    bulk_creation: AsyncClient,
    task_fixture: dict[str, Any],
) -> None:
    client = bulk_creation
    member_email: str = two_members["member_email"]
    existing_task = await client.get(
        f"/api/v1/board/{task_fixture['board_id']}/columns/{task_fixture['column_id']}/tasks/{2}"
    )
    assert existing_task.status_code == 200
    task_id: int = existing_task.json()["id"]
    result = await client.put(
        f"/api/v1/board/{task_fixture['board_id']}/columns/{task_fixture['column_id']}/tasks/{task_id}",
        json={"new_data": {}, "email": member_email},
    )
    assert result.status_code == 200
