from pydantic import BaseModel, BeforeValidator, EmailStr, ConfigDict
from typing import Annotated
from backend.core.utility.password_verifier import verify_password
from backend.core.utility.validate_name import set_name
from uuid import UUID

PasswordField = Annotated[str, BeforeValidator(verify_password)]
NameField = Annotated[str, BeforeValidator(set_name)]


class UserCredentials(BaseModel):
    email: EmailStr
    password: PasswordField
    name: NameField = None


class UserLogin(BaseModel):
    email: str
    password: str


class UserGet(BaseModel):
    id: UUID
    email: str
    name: str

    model_config = ConfigDict(from_attributes=True)
