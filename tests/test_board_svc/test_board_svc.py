import pytest


def test_board_creation(auth_client):
    result = auth_client.post(
        "/api/v1/board/",
        json={
            "name": "Test board",
            "description": "Some description in here",
        },
    )
    data = result.json()
    assert result.status_code == 201
    assert "id" in data


def test_with_empty_description(auth_client):
    result = auth_client.post(
        "/api/v1/board/",
        json={"name": "Test board"},
    )
    data = result.json()
    assert result.status_code == 201
    assert "id" in data


def test_board_creation_fail(auth_client):
    result = auth_client.post(
        "/api/v1/board/",
        json={
            "name": "",
            "description": "Some description in here",
        },
    )

    assert result.status_code == 422


def test_get_board(auth_client):
    auth_client.post(
        "/api/v1/board/",
        json={
            "name": "Test board",
            "description": "Some description in here",
        },
    )
    result = auth_client.get("/api/v1/board/all")
    data = result.json()
    assert result.status_code == 200
    assert len(data) > 0


def test_get_single_board(auth_client):
    auth_client.post(
        "/api/v1/board/",
        json={
            "name": "Test board",
            "description": "Some description in here",
        },
    )
    result = auth_client.get("/api/v1/board/all")
    data = result.json()
    id = data[0]["id"]
    single_record = auth_client.get(f"/api/v1/board/{id}")
    data = single_record.json()
    assert single_record.status_code == 200
    assert len(data) > 0


def test_update_board(auth_client):
    auth_client.post(
        "/api/v1/board/",
        json={
            "name": "Test board",
            "description": "Some description in here",
        },
    )
    result = auth_client.get("/api/v1/board/all")
    data = result.json()
    board_id = data[0]["id"]
    update = auth_client.patch(
        f"/api/v1/board/{board_id}", json={"name": " New name"}
    )
    data = update.json()
    assert update.status_code == 200
    assert data["id"] == board_id


def test_update_board_fail(auth_client):
    update = auth_client.patch(
        "/api/v1/board/10000", json={"name": " New name"}
    )
    assert update.status_code == 404


def test_delete_board(auth_client):
    auth_client.post(
        "/api/v1/board/",
        json={
            "name": "Test board",
            "description": "Some description in here",
        },
    )
    result = auth_client.get("/api/v1/board/all")
    data = result.json()
    board_id = data[0]["id"]
    delete = auth_client.delete(f"/api/v1/board/{board_id}")
    assert delete.status_code == 204


def test_board_delete_fail(auth_client):
    delete = auth_client.delete("/api/v1/board/10000")
    assert delete.status_code == 404
