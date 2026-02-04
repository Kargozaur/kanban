from typing import Any

from anyio.to_thread import run_sync

from backend.core.decorators.transactional import transactional
from backend.core.exceptions.exceptions import (
    NotFoundError,
    UserAlreadyExists,
)
from backend.core.security.password_hasher import PasswordHasher
from backend.core.security.token_svc import TokenSvc
from backend.database.unit_of_work import UnitOfWork
from backend.schemas.token_schema import TokenResponse
from backend.schemas.user_schema import (
    UserCredentials,
    UserGet,
    UserLogin,
)


class UserService:
    """
    User service \n
    methods: \n
    create_user(user_credential) \n
    login_user(user_credential) \n
    """

    def __init__(
        self,
        uow: UnitOfWork,
        password_hasher: PasswordHasher,
        token_service: TokenSvc,
    ) -> None:
        self.uow = uow
        self.password_hasher = password_hasher
        self.token_service = token_service

    @transactional
    async def create_user(self, user_credential: UserCredentials) -> UserGet:
        hashed_password = await run_sync(
            self.password_hasher.hash_password, user_credential.password
        )
        updated_model = user_credential.model_copy(update={"password": hashed_password})

        user_orm = await self.uow.users.create_user(updated_model)

        if not user_orm:
            raise UserAlreadyExists()
        result = UserGet.model_validate(user_orm)

        return result

    @transactional
    async def login_user(self, user_credential: UserLogin) -> TokenResponse:
        if not (
            check_if_exists := await self.uow.users.get_user_data(user_credential.email)
        ):
            raise NotFoundError()
        is_password_correct: bool = await run_sync(
            self.password_hasher.verify_password,
            user_credential.password,
            check_if_exists.password,
        )
        if not is_password_correct:
            raise NotFoundError()
        access_token = await self.token_service.create_token(check_if_exists)
        token: dict[str, Any] = {
            "access_token": access_token,
            "token_type": "Bearer",
        }
        return TokenResponse.model_validate(token)
