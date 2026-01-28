from fastapi import Depends, Request
from typing import Annotated
from typing_extensions import Doc
from backend.core.security.user_auth import AuthService
from backend.dependancies.db_dep import DBDep
from backend.dependancies.annotated_types import SettingsDep
from backend.models.models import User
from backend.core.exceptions.exceptions import InvalidCredentialsError


def get_auth_service(
    settings: SettingsDep, session: DBDep
) -> AuthService:
    return AuthService(settings, session)


async def current_user_dep(
    request: Request,
    auth_svc: AuthService = Depends(get_auth_service),
) -> User:
    token = request.cookies.get("access_token")
    if not token:
        raise InvalidCredentialsError()
    return await auth_svc.get_user(token)


CurrentUserDep = Annotated[
    User,
    Depends(current_user_dep),
    Doc(
        "Dependancy of the AuthService to verify the current user. Depends on SettingsDep, DBDep"
    ),
]
