from typing import Any

import pytest
from httpx import AsyncClient


@pytest.fixture
async def columns(auth_client: AsyncClient) -> dict[str, Any]:
    data = await auth_client.post(
        "/api/v1/board/",
        json={
            "name": "Test board",
            "description": "Some description in here",
        },
    )
    assert data.status_code in (200, 201)
    board_id = data.json()["id"]
    columns = await auth_client.post(
        f"/api/v1/board/{board_id}/columns/add",
        json={
            "name": "my amazing zzz",
            "position": 2.5,
            "wip_limit": 1,
        },
    )
    assert columns.status_code in (200, 201)
    column_id = columns.json()["id"]
    return {
        "owner_client": auth_client,
        "board_id": board_id,
        "column_id": column_id,
    }


async def test_creation_column(auth_client: AsyncClient) -> None:
    data = await auth_client.post(
        "/api/v1/board/",
        json={
            "name": "Test board",
            "description": "Some description in here",
        },
    )
    assert data.status_code in (200, 201)
    board_id = data.json()["id"]
    columns = await auth_client.post(
        f"/api/v1/board/{board_id}/columns/add",
        json={
            "name": "my amazing zzz",
            "position": 2.5,
            "wip_limit": 1,
        },
    )
    data = columns.json()["name"]
    assert columns.status_code in (200, 201)
    assert data == "my amazing zzz"


async def test_creation_column_violation(auth_client: AsyncClient) -> None:
    data = await auth_client.post(
        "/api/v1/board/",
        json={
            "name": "Test board",
            "description": "Some description in here",
        },
    )
    assert data.status_code in (200, 201)
    board_id = data.json()["id"]
    await auth_client.post(
        f"/api/v1/board/{board_id}/columns/add",
        json={
            "name": "my amazing zzz",
            "position": 2.5,
            "wip_limit": 1,
        },
    )
    result = await auth_client.post(
        f"/api/v1/board/{board_id}/columns/add",
        json={
            "name": "my amazing zzz",
            "position": 2.5,
            "wip_limit": 1,
        },
    )
    assert result.status_code == 409


async def test_update_column(columns: dict[str, Any]) -> None:
    auth_client = columns["owner_client"]
    new_name = "my new amazing name"
    result = await auth_client.patch(
        f"/api/v1/board/{columns['board_id']}/columns/{columns['column_id']}",
        json={"name": new_name},
    )
    data = result.json()
    assert result.status_code == 200
    assert data["name"] == new_name


async def test_update_column_violation(columns: dict[str, Any]) -> None:
    auth_client = columns["owner_client"]
    await auth_client.post(
        f"/api/v1/board/{columns['board_id']}/columns/add",
        json={
            "name": "very new column",
            "position": 3,
            "wip_limit": 1,
        },
    )
    result = await auth_client.patch(
        f"/api/v1/board/{columns['board_id']}/columns/{columns['column_id']}",
        json={"name": "very new column"},
    )
    assert result.status_code == 409


async def test_delete_column(columns: dict[str, Any]) -> None:
    auth_client = columns["owner_client"]
    result = await auth_client.delete(
        f"/api/v1/board/{columns['board_id']}/columns/{columns['column_id']}"
    )
    assert result.status_code == 204
