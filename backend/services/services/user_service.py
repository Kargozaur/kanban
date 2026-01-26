from backend.schemas.user_schema import UserCredentials, UserGet
from backend.core.security.password_hasher import PasswordHasher
from backend.core.security.token_svc import TokenSvc
from backend.services.repositories.user_repo import UserRepository
from backend.core.exceptions.base_exception import (
    InvalidCredentialsError,
    NotFoundError,
    AppBaseException,
)


class UserService:
    def __init__(
        self,
        user_repo: UserRepository,
        password_hasher: PasswordHasher,
        token_service: TokenSvc,
    ) -> None:
        self.user_repo = user_repo
        self.password_hasher = password_hasher
        self.token_service = token_service

    async def create_user(self, user_credential: UserCredentials):
        hashed_password = self.password_hasher.hash_password(
            user_credential.password
        )
        user_credential.password = hashed_password
        result = await self.user_repo.create_user(user_credential)
        if result["result"] != "succesfully added user":
            raise AppBaseException()
        get_user = await self.user_repo.get_user_by_email(
            user_credential.email
        )
        return UserGet.model_validate(get_user)

    async def login_user(self, user_credential: UserCredentials):
        check_if_exists = await self.user_repo.get_user_data(
            user_credential.email
        )
        if check_if_exists is None:
            raise NotFoundError()
        if not self.password_hasher.verify_password(
            user_credential.password, check_if_exists.password
        ):
            raise InvalidCredentialsError()

        access_token = self.token_service.create_token(
            check_if_exists
        )
        return {"access_token": access_token, "token_type": "Bearer"}
