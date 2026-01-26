from pydantic import BaseModel, BeforeValidator, EmailStr
from typing import Annotated
from backend.core.utility.password_verifier import verify_password
from uuid import UUID

PasswordField = Annotated[str, BeforeValidator(verify_password)]


class UserCredentials(BaseModel):
    email: EmailStr
    password: PasswordField


class UserGet(BaseModel):
    id: UUID
    email: str
