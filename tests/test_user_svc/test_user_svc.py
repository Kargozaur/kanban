import pytest


def test_user_creation(client):
    result = client.post(
        "/api/v1/auth/sign_up",
        json={
            "email": "user@example.com",
            "password": "SuperPassword!23",
        },
    )
    data = result.json()
    assert result.status_code == 201
    assert data["email"] == "user@example.com"


def test_user_creation_fail(client):
    result = client.post(
        "/api/v1/auth/sign_up",
        json={
            "email": "userexample.com",
            "password": "SuperPassword!23",
        },
    )
    data = result.json()
    assert result.status_code == 422
    assert "detail" in data


def test_user_login(client):
    client.post(
        "/api/v1/auth/sign_up",
        json={
            "email": "user@example.com",
            "password": "SuperPassword!23",
        },
    )
    result = client.post(
        "/api/v1/auth/login",
        json={
            "email": "user@example.com",
            "password": "SuperPassword!23",
        },
    )
    data = result.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"


def test_user_logout(client):
    client.post(
        "/api/v1/auth/sign_up",
        json={
            "email": "user@example.com",
            "password": "SuperPassword!23",
        },
    )
    client.post(
        "/api/v1/auth/login",
        json={
            "email": "user@example.com",
            "password": "SuperPassword!23",
        },
    )
    result = client.post("/api/v1/auth/logout")
    data = result.json()
    assert result.status_code == 200
    assert "message" in data


def test_me(client):
    client.post(
        "/api/v1/auth/sign_up",
        json={
            "email": "user@example.com",
            "password": "SuperPassword!23",
        },
    )
    client.post(
        "/api/v1/auth/login",
        json={
            "email": "user@example.com",
            "password": "SuperPassword!23",
        },
    )
    result = client.get("/api/v1/auth/me")
    data = result.json()
    assert result.status_code == 200
    assert "id" in data


def test_me_blank(client):
    result = client.get("/api/v1/auth/me")
    assert result.status_code == 401


def test_me_without_login(client):
    client.post(
        "/api/v1/auth/sign_up",
        json={
            "email": "user@example.com",
            "password": "SuperPassword!23",
        },
    )
    result = client.get("/api/v1/auth/me")
    assert result.status_code == 401
