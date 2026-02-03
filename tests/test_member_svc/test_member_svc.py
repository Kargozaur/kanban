from typing import Any

import pytest
from httpx import AsyncClient


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


async def test_adding_user(
    auth_client: AsyncClient, second_auth_client: AsyncClient
) -> None:
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


async def test_adding_user_as_admin(
    auth_client: AsyncClient, second_auth_client: AsyncClient
) -> None:
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
        json={"email": user_email, "role": "admin"},
    )
    assert result.status_code == 409


async def test_updating_user(two_members: dict[str, Any]) -> None:
    client = two_members["owner_client"]
    result = await client.patch(
        f"/api/v1/board/{two_members['board_id']}/members/update",
        json={"email": two_members["member_email"], "role": "member"},
    )
    assert result.status_code == 200


async def test_updating_unknown_user(two_members: dict[str, Any]) -> None:
    client = two_members["owner_client"]
    result = await client.patch(
        f"/api/v1/board/{two_members['board_id']}/members/update",
        json={"email": "new@example.com", "role": "member"},
    )
    assert result.status_code == 404


async def test_updating_user_to_admin(two_members: dict[str, Any]) -> None:
    client = two_members["owner_client"]
    result = await client.patch(
        f"/api/v1/board/{two_members['board_id']}/members/update",
        json={"email": two_members["member_email"], "role": "admin"},
    )
    assert result.status_code == 409


async def test_delete_user(two_members: dict[str, Any]) -> None:
    client = two_members["owner_client"]
    email = two_members["member_email"]
    result = await client.delete(
        f"/api/v1/board/{two_members['board_id']}/members/delete_member/{email}",
    )
    assert result.status_code == 204


async def test_unknown_user(two_members: dict[str, Any]) -> None:
    client = two_members["owner_client"]
    result = await client.delete(
        f"/api/v1/board/{two_members['board_id']}/members/delete_member/unknown@example.com",
    )
    assert result.status_code == 404
