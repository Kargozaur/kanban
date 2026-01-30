import pytest


@pytest.mark.parametrize(
    "board_name, description, status_code",
    [
        ("Test_board", "Description", 201),
        ("Mobile app board", "", 201),
    ],
)
async def test_board_creation(
    board_name, description, status_code, auth_client
):
    result = await auth_client.post(
        "/api/v1/board/",
        json={
            "name": board_name,
            "description": description,
        },
    )
    data = result.json()
    assert result.status_code == status_code
    assert "id" in data
    assert data["name"] == board_name


@pytest.mark.parametrize(
    "board_name, description, status_code",
    [
        ("", "", 422),
        (None, None, 422),
        ("", None, 422),
        (None, "", 422),
    ],
)
async def test_board_creation_fail(
    board_name, description, status_code, auth_client
):
    result = await auth_client.post(
        "/api/v1/board/",
        json={
            "name": board_name,
            "description": description,
        },
    )

    assert result.status_code == status_code


async def test_get_board(auth_client):
    await auth_client.post(
        "/api/v1/board/",
        json={
            "name": "Test board",
            "description": "Some description in here",
        },
    )
    result = await auth_client.get("/api/v1/board/all")
    data = result.json()
    assert result.status_code == 200
    assert len(data) > 0


async def test_unathoreized_get(unathorized_client, auth_client):
    await auth_client.post(
        "/api/v1/board/",
        json={
            "name": "Test board",
            "description": "Some description in here",
        },
    )
    result = await auth_client.get("/api/v1/board/all")
    data = result.json()
    id = data[0]["id"]
    response = await unathorized_client.get(f"/api/v1/board/{id}")
    assert response.status_code == 401


async def test_board_without_creation(auth_client):
    result = await auth_client.get("/api/v1/board/all")
    data = result.json()
    assert result.status_code == 200
    assert len(data) == 0


async def test_get_single_board(auth_client):
    await auth_client.post(
        "/api/v1/board/",
        json={
            "name": "Test board",
            "description": "Some description in here",
        },
    )
    result = await auth_client.get("/api/v1/board/all")
    data = result.json()
    id = data[0]["id"]
    single_record = await auth_client.get(f"/api/v1/board/{id}")
    data = single_record.json()
    assert single_record.status_code == 200
    assert len(data) > 0


async def test_update_board(auth_client):
    await auth_client.post(
        "/api/v1/board/",
        json={
            "name": "Test board",
            "description": "Some description in here",
        },
    )
    result = await auth_client.get("/api/v1/board/all")
    data = result.json()
    board_id = data[0]["id"]
    update = await auth_client.patch(
        f"/api/v1/board/{board_id}", json={"name": " New name"}
    )
    data = update.json()
    assert update.status_code == 200
    assert data["id"] == board_id


async def test_update_board_fail(auth_client):
    update = await auth_client.patch(
        "/api/v1/board/10000", json={"name": " New name"}
    )
    assert update.status_code == 404


async def test_delete_board(auth_client):
    await auth_client.post(
        "/api/v1/board/",
        json={
            "name": "Test board",
            "description": "Some description in here",
        },
    )
    result = await auth_client.get("/api/v1/board/all")
    data = result.json()
    board_id = data[0]["id"]
    delete = await auth_client.delete(f"/api/v1/board/{board_id}")
    assert delete.status_code == 204


async def test_board_delete_fail(auth_client):
    delete = await auth_client.delete("/api/v1/board/10000")
    assert delete.status_code == 404
