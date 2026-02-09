from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from backend.kanban.core.settings.settings import AppSettings
from backend.kanban.models.models import User


class TokenSvc:
    def __init__(self, settings: AppSettings) -> None:
        self.secret = settings.token.secret
        self.algo = settings.token.algorithm
        self.access_ttl = settings.token.token_ttl

    async def create_token(self, user: User) -> str:
        to_encode: dict[str, Any] = {"sub": str(user.id)}
        expire: datetime = datetime.now(tz=UTC) + timedelta(minutes=self.access_ttl)
        to_encode.update({"exp": expire})
        encoded: str = jwt.encode(
            payload=to_encode, key=self.secret, algorithm=self.algo
        )
        return encoded


def get_token_svc(settings: AppSettings) -> TokenSvc:
    return TokenSvc(settings)
