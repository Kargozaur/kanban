from backend.schemas.user_schema import (
    UserCredentials,
    UserGet,
    UserLogin,
)
from backend.schemas.token_schema import TokenResponse
from backend.core.security.password_hasher import PasswordHasher
from backend.core.security.token_svc import TokenSvc
from backend.database.unit_of_work import UnitOfWork
from backend.core.exceptions.exceptions import (
    NotFoundError,
    UserAlreadyExists,
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
        uow: UnitOfWork,
        password_hasher: PasswordHasher,
        token_service: TokenSvc,
    ) -> None:
        self.uow = uow
        self.password_hasher = password_hasher
        self.token_service = token_service

    async def create_user(self, user_credential: UserCredentials):
        async with self.uow:
            hashed_password = self.password_hasher.hash_password(
                user_credential.password
            )
            updated_model = user_credential.model_copy(
                update={"password": hashed_password}
            )
            logging.info(
                f"DEBUG - Creating user with the email: {updated_model.email}"
            )
            logging.info(
                f"DEBUG - user name is: {updated_model.name}"
            )
            user_orm = await self.uow.users.create_user(updated_model)
            logger.info(f"DEBUG - result= {user_orm}")
            if not user_orm:
                raise UserAlreadyExists()
            result = UserGet.model_validate(user_orm)

            logging.info(
                f"DEBUG - type of get_user: {type(user_orm)}"
            )
            logging.info(f"DEBUG - get_user values: {user_orm}")
            logger.info(
                f"DEBUG - get_user.__dict__ if available: {getattr(user_orm, '__dict__', 'no __dict__')}"
            )
            await self.uow.commit()
            return result

    async def login_user(self, user_credential: UserLogin):
        async with self.uow:
            check_if_exists = await self.uow.users.get_user_data(
                user_credential.email
            )
            if (
                check_if_exists is None
                or not self.password_hasher.verify_password(
                    user_credential.password, check_if_exists.password
                )
            ):
                raise NotFoundError()

            access_token = self.token_service.create_token(
                check_if_exists
            )
            token = {
                "access_token": access_token,
                "token_type": "Bearer",
            }
            return TokenResponse.model_validate(token)
