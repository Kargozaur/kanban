from backend.schemas.user_schema import (
    UserCredentials,
    UserGet,
    UserLogin,
)
from backend.schemas.token_schema import TokenResponse
from backend.core.security.password_hasher import PasswordHasher
from backend.core.security.token_svc import TokenSvc
from backend.services.repositories.user_repo import UserRepository
from backend.core.exceptions.exceptions import (
    InvalidCredentialsError,
    NotFoundError,
    AppBaseException,
)
import logging

logger = logging.getLogger(__name__)


class UserService:
    """
    User service \n
    methods: \n
    create_user(user_credential) \n
    login_user(user_credential) \n
    """

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
        updated_model = user_credential.model_copy(
            update={"password": hashed_password}
        )
        logging.info(
            f"DEBUG - Creating user with the email: {updated_model.email}"
        )
        logging.info(f"DEBUG - user name is: {updated_model.name}")
        result = await self.user_repo.create_user(updated_model)
        logger.info(f"DEBUG - result= {result}")
        if result["result"] is False:
            raise AppBaseException()
        get_user = await self.user_repo.get_user_by_email(
            updated_model.email
        )
        logging.info(f"DEBUG - type of get_user: {type(get_user)}")
        logging.info(f"DEBUG - get_user values: {get_user}")
        logger.info(
            f"DEBUG - get_user.__dict__ if available: {getattr(get_user, '__dict__', 'no __dict__')}"
        )
        return UserGet.model_validate(get_user)

    async def login_user(self, user_credential: UserLogin):
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
        token = {"access_token": access_token, "token_type": "Bearer"}
        return TokenResponse.model_validate(token)
