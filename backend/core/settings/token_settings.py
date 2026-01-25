from pydantic import BaseModel, Field


class TokenSettings(BaseModel):
    secret: str
    algorithm: str
    token_ttl: int = Field(default=60)
