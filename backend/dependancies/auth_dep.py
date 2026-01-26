from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from backend.core.security.user_auth import AuthService
from backend.dependancies.db_dep import DBDep
from backend.dependancies.annotated_types import SettingsDep
from backend.models.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_auth_service(
    settings: SettingsDep, session: DBDep
) -> AuthService:
    return AuthService(settings, session)


async def current_user_dep(
    auth_svc: AuthService = Depends(get_auth_service),
    token: str = Depends(oauth2_scheme),
) -> User:
    return await auth_svc.get_user(token)


CurrentUserDep = Annotated[User, Depends(current_user_dep)]
