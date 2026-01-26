from pydantic import BaseModel
from uuid import UUID


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class Token(BaseModel):
    sub: UUID
    exp: int
