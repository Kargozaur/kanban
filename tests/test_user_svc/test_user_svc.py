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
    assert result.status_code == 200
    assert data["email"] == "user@example.com"


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
    assert len(data["access_token"]) >= 8
    assert data["token_type"] == "Bearer"
