from uuid import UUID

from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class Token(BaseModel):
    sub: UUID
    exp: int
