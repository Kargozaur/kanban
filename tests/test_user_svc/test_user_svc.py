import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("user@example.com", "SuperPassword!23", 201),
        ("use__123@example.com", "2###2SS3", 201),
        ("use2r@example.com", "CoolPoaa11@@", 201),
    ],
)
async def test_user_creation(
    email: str, password: str, status_code: int, client: AsyncClient
) -> None:
    result = await client.post(
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
async def test_registration_fail(
    email: str, password: str, status_code: int, client: AsyncClient
) -> None:
    result = await client.post(
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
async def test_user_login(
    email: str, password: str, status_code: int, client: AsyncClient
) -> None:
    await client.post(
        "/api/v1/auth/sign_up",
        json={
            "email": email,
            "password": password,
        },
    )
    result = await client.post(
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
        ("user@example.com", "SuperPassword!23", "bad_password", 404),
        ("user22@example.com", "Myc)0lPass", "not_cool_pass", 404),
    ],
)
async def test_password(
    email: str, password: str, bad_password: str, status_code: int, client: AsyncClient
) -> None:
    await client.post(
        "/api/v1/auth/sign_up",
        json={
            "email": email,
            "password": password,
        },
    )
    result = await client.post(
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
async def test_email(
    email: str, wrong_email: str, password: str, status_code: int, client: AsyncClient
) -> None:
    await client.post(
        "/api/v1/auth/sign_up",
        json={
            "email": email,
            "password": password,
        },
    )
    result = await client.post(
        "/api/v1/auth/login",
        data={
            "username": wrong_email,
            "password": password,
        },
    )
    assert result.status_code == status_code


async def test_user_logout(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/auth/sign_up",
        json={
            "email": "user@example.com",
            "password": "SuperPassword!23",
        },
    )
    login_res = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "user@example.com",
            "password": "SuperPassword!23",
        },
    )
    token = login_res.json()["access_token"]
    result = await client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )
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
async def test_me(
    email: str, password: str, status_code: int, client: AsyncClient
) -> None:
    await client.post(
        "/api/v1/auth/sign_up",
        json={
            "email": email,
            "password": password,
        },
    )
    await client.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )
    result = await client.get("/api/v1/auth/me")
    data = result.json()
    assert result.status_code == status_code
    assert "id" in data
    assert data["email"] == email


async def test_me_blank(client: AsyncClient) -> None:
    result = await client.get("/api/v1/auth/me")
    assert result.status_code == 401


async def test_me_without_login(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/auth/sign_up",
        json={
            "email": "user@example.com",
            "password": "SuperPassword!23",
        },
    )
    result = await client.get("/api/v1/auth/me")
    assert result.status_code == 401
