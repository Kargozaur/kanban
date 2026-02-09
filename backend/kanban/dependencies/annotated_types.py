from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Doc

from backend.kanban.core.security.password_hasher import PasswordHasher
from backend.kanban.core.security.token_svc import TokenSvc
from backend.kanban.core.settings.settings import AppSettings
from backend.kanban.dependencies.db_dep import DBDep
from backend.kanban.dependencies.states import (
    get_hasher,
    get_settings,
    get_token_svc,
)
from backend.kanban.schemas.pagination_schema import Pagination
from backend.kanban.services.repositories.board_repo import BoardRepository
from backend.kanban.services.repositories.user_repo import UserRepository


def get_user_repository(db: DBDep) -> UserRepository:
    return UserRepository(db)


def get_board_repository(db: DBDep) -> BoardRepository:
    return BoardRepository(db)


TokenDep = Annotated[
    TokenSvc,
    Depends(get_token_svc),
    Doc("dependency of the Tocker Service(jwt encoding)"),
]
PasswordDep = Annotated[
    PasswordHasher,
    Depends(get_hasher),
    Doc("dependency of the Password hasher for the UserService"),
]
UserRepoDep = Annotated[
    UserRepository,
    Depends(get_user_repository),
    Doc("dependency of the User repository for the UserService. Depends on DBDep"),
]
SettingsDep = Annotated[
    AppSettings,
    Depends(get_settings),
    Doc("Global dependency of the AppSettings. Managed inside the FastAPI lifespan"),
]
PaginationDep = Annotated[
    Pagination,
    Depends(),
    Doc(
        "dependency of the Pagination. Sets limit and offset for both the request"
        "and SQL queries"
    ),
]
BoardRepoDep = Annotated[
    BoardRepository,
    Depends(get_board_repository),
    Doc("dependency of the Board repository for the BoardService. Depends on DBDep"),
]
FormData = Annotated[
    OAuth2PasswordRequestForm,
    Depends(),
    Doc("dependency for the SwaggerUI login"),
]
