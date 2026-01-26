from backend.core.settings.settings import AppSettings
from datetime import datetime, timedelta, timezone
from backend.models.models import User
import jwt


class TokenSvc:
    def __init__(self, settings: AppSettings) -> None:
        self.secret = settings.token.secret
        self.algo = settings.token.algorithm
        self.access_ttl = settings.token.token_ttl

    def create_token(self, user: User) -> str:
        to_encode: dict[str, str] = {"sub": str(user.id)}
        expire: datetime = datetime.now(tz=timezone.utc) + timedelta(
            minutes=self.access_ttl
        )
        to_encode.update({"exp": expire})
        encoded: str = jwt.encode(
            payload=to_encode, key=self.secret, algorithm=self.algo
        )
        return encoded


def get_token_svc(settings) -> TokenSvc:
    return TokenSvc(settings)
