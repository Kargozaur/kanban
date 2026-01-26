from backend.dependancies.annotated_types import (
    TokenDep,
    PasswordDep,
    UserRepoDep,
)

from backend.services.services.user_service import UserService


def get_user_service(
    user_repo: UserRepoDep,
    password_hasher: PasswordDep,
    token_svc: TokenDep,
) -> UserService:
    return UserService(user_repo, password_hasher, token_svc)
