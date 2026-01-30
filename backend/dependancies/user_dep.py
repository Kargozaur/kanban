from backend.dependancies.annotated_types import (
    TokenDep,
    PasswordDep,
)
from backend.dependancies.uow_dep import UOWDep
from backend.services.services.user_service import UserService


def get_user_service(
    uow: UOWDep,
    password_hasher: PasswordDep,
    token_svc: TokenDep,
) -> UserService:
    return UserService(uow, password_hasher, token_svc)
