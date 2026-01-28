from typing import Annotated
from fastapi import Depends
from backend.dependancies.states import (
    get_hasher,
    get_token_svc,
    get_settings,
)
from backend.core.security.password_hasher import PasswordHasher
from backend.core.security.token_svc import TokenSvc
from backend.dependancies.db_dep import DBDep
from backend.services.repositories.user_repo import UserRepository
from backend.core.settings.settings import AppSettings
from backend.schemas.pagination_schema import Pagination
from backend.services.repositories.board_repo import BoardRepository


def get_user_repository(db: DBDep) -> UserRepository:
    return UserRepository(db)


def get_board_repository(db: DBDep) -> BoardRepository:
    return BoardRepository(db)


TokenDep = Annotated[TokenSvc, Depends(get_token_svc)]
PasswordDep = Annotated[PasswordHasher, Depends(get_hasher)]
UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]
SettingsDep = Annotated[AppSettings, Depends(get_settings)]
PaginationDep = Annotated[Pagination, Depends()]
BoardRepoDep = Annotated[
    BoardRepository, Depends(get_board_repository)
]
