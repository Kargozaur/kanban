import jwt
from jwt import PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.token_schema import Token
from backend.core.settings.settings import AppSettings
from backend.models.models import User
from backend.core.exceptions.exceptions import InvalidCredentialsError


class AuthService:
    def __init__(
        self, settings: AppSettings, session: AsyncSession
    ) -> None:
        self.key = settings.token.secret
        self.algo = settings.token.algorithm
        self.session = session

    def verify_access_token(
        self, token: str, credential_exception: Exception
    ) -> Token:
        try:
            payload = jwt.decode(
                jwt=token, key=self.key, algorithms=[self.algo]
            )
            return Token.model_validate(payload)
        except PyJWTError:
            raise credential_exception

    async def get_user(self, token: str) -> User:
        credential_exception = InvalidCredentialsError()
        token_data = self.verify_access_token(
            token, credential_exception
        )
        if token_data.sub is None:
            raise credential_exception
        user_id = token_data.sub
        user = await self.session.get(User, user_id)
        if not user:
            raise credential_exception
        return user
