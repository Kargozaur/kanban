from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import APIKeyCookie, OAuth2PasswordBearer
from typing_extensions import Doc

from backend.core.exceptions.exceptions import InvalidCredentialsError
from backend.core.security.user_auth import AuthService
from backend.dependancies.annotated_types import SettingsDep
from backend.dependancies.db_dep import DBDep
from backend.models.models import User


cookie_scheme = APIKeyCookie(name="access_token", auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def get_auth_service(settings: SettingsDep, session: DBDep) -> AuthService:
    return AuthService(settings, session)


async def current_user_dep(
    request: Request,
    token_from_header: str = Depends(oauth2_scheme),
    token_from_cookie: str = Depends(cookie_scheme),
    auth_svc: AuthService = Depends(get_auth_service),
) -> User:
    token = request.cookies.get("access_token")
    if not token:
        token = token_from_header
    if not token:
        raise InvalidCredentialsError()
    return await auth_svc.get_user(token)


CurrentUserDep = Annotated[
    User,
    Depends(current_user_dep),
    Doc(
        "Dependancy of the AuthService to verify the current user."
        "Depends on SettingsDep, DBDep"
    ),
]
