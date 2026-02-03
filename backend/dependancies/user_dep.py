from typing import Annotated

from fastapi import Depends
from typing_extensions import Doc

from backend.dependancies.annotated_types import (
    PasswordDep,
    TokenDep,
)
from backend.dependancies.uow_dep import UOWDep
from backend.services.services.user_service import UserService


def get_user_service(
    uow: UOWDep,
    password_hasher: PasswordDep,
    token_svc: TokenDep,
) -> UserService:
    return UserService(uow, password_hasher, token_svc)


UserSvcDep = Annotated[
    UserService,
    Depends(get_user_service),
    Doc("Dependancy for the user service inside the auth router"),
]
