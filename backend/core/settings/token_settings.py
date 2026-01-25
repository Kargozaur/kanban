from pydantic import BaseModel


class TokenSettings(BaseModel):
    secret: str
    algorithm: str
    token_ttl: int
