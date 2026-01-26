from typing import Annotated
from fastapi import Depends
from backend.dependancies.states import get_hasher, get_token_svc
from backend.core.security.password_hasher import PasswordHasher
from backend.core.security.token_svc import TokenSvc
from backend.dependancies.db_dep import DBDep
from backend.services.repositories.user_repo import UserRepository


def get_user_repository(db: DBDep) -> UserRepository:
    return UserRepository(db)


TokenDep = Annotated[TokenSvc, Depends(get_token_svc)]
PasswordDep = Annotated[PasswordHasher, Depends(get_hasher)]
UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]
