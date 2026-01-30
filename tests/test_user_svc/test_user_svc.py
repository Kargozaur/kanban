import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("user@example.com", "SuperPassword!23", 201),
        ("use__123@example.com", "2###2SS3", 201),
        ("use2r@example.com", "CoolPoaa11@@", 201),
    ],
)
def test_user_creation(email, password, status_code, client):
    result = client.post(
        "/api/v1/auth/sign_up",
        json={
            "email": email,
            "password": password,
        },
    )
    data = result.json()

    assert data["email"] == email
    assert result.status_code == status_code


@pytest.mark.parametrize(
    "email,password, status_code",
    [
        ("bad_em.com", "passwr", 422),
        ("goog@example.com", "bas_ps", 422),
        ("be", "Go0DPassw#d", 422),
    ],
)
def test_registration_fail(email, password, status_code, client):
    result = client.post(
        "/api/v1/auth/sign_up",
        json={
            "email": email,
            "password": password,
        },
    )
    assert result.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("good@example.com", "SupperPassw0rd!23", 201),
        ("user22@example.com", "Par@at#332", 201),
    ],
)
def test_user_login(email, password, status_code, client):
    client.post(
        "/api/v1/auth/sign_up",
        json={
            "email": email,
            "password": password,
        },
    )
    result = client.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )
    data = result.json()
    assert result.status_code == status_code
    assert "access_token" in data
    assert data["token_type"] == "Bearer"


@pytest.mark.parametrize(
    "email, password, bad_password, status_code",
    [
        ("user@example.com", "SuperPassword!23", "bad_password", 401),
        ("user22@example.com", "Myc)0lPass", "not_cool_pass", 401),
    ],
)
def test_password(email, password, bad_password, status_code, client):
    client.post(
        "/api/v1/auth/sign_up",
        json={
            "email": email,
            "password": password,
        },
    )
    result = client.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": bad_password,
        },
    )
    assert result.status_code == status_code


@pytest.mark.parametrize(
    "email, wrong_email, password, status_code",
    [
        (
            "user@example.com",
            "user2@example.com",
            "SuperPassword!23",
            404,
        ),
        (
            "user3@example.com",
            "notexistingemail@example.com",
            "SuperPassword!23",
            404,
        ),
    ],
)
def test_email(email, wrong_email, password, status_code, client):
    client.post(
        "/api/v1/auth/sign_up",
        json={
            "email": email,
            "password": password,
        },
    )
    result = client.post(
        "/api/v1/auth/login",
        data={
            "username": wrong_email,
            "password": password,
        },
    )
    assert result.status_code == status_code


def test_user_logout(client):
    client.post(
        "/api/v1/auth/sign_up",
        json={
            "username": "user@example.com",
            "password": "SuperPassword!23",
        },
    )
    client.post(
        "/api/v1/auth/login",
        data={
            "username": "user@example.com",
            "password": "SuperPassword!23",
        },
    )
    result = client.post("/api/v1/auth/logout")
    data = result.json()
    assert result.status_code == 200
    assert "message" in data


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("good@example.com", "SupperPassw0rd!23", 200),
        ("user22@example.com", "Par@at#332", 200),
    ],
)
def test_me(email, password, status_code, client):
    client.post(
        "/api/v1/auth/sign_up",
        json={
            "email": email,
            "password": password,
        },
    )
    client.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )
    result = client.get("/api/v1/auth/me")
    data = result.json()
    assert result.status_code == status_code
    assert "id" in data
    assert data["email"] == email


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
