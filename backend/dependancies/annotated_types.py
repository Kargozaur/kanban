from typing import Annotated
from typing_extensions import Doc
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
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


TokenDep = Annotated[
    TokenSvc,
    Depends(get_token_svc),
    Doc("Dependancy of the Tocker Service(jwt encoding)"),
]
PasswordDep = Annotated[
    PasswordHasher,
    Depends(get_hasher),
    Doc("Dependancy of the Password hasher for the UserService"),
]
UserRepoDep = Annotated[
    UserRepository,
    Depends(get_user_repository),
    Doc(
        "Dependancy of the User repository for the UserService. Depends on DBDep"
    ),
]
SettingsDep = Annotated[
    AppSettings,
    Depends(get_settings),
    Doc(
        "Global dependancy of the AppSettings. Managed inside the FastAPI lifespan"
    ),
]
PaginationDep = Annotated[
    Pagination,
    Depends(),
    Doc(
        "Dependancy of the Pagination. Sets limit and offset for both the request and SQL queries"
    ),
]
BoardRepoDep = Annotated[
    BoardRepository,
    Depends(get_board_repository),
    Doc(
        "Dependancy of the Board repository for the BoardService. Depends on DBDep"
    ),
]
FormData = Annotated[
    OAuth2PasswordRequestForm,
    Depends(),
    Doc("Dependayc for the SwaggerUI login"),
]
