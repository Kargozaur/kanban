from pydantic import (
    BaseModel,
    BeforeValidator,
    EmailStr,
    ConfigDict,
    model_validator,
)
from typing import Annotated, Optional
from backend.core.utility.password_verifier import verify_password
from uuid import UUID

PasswordField = Annotated[str, BeforeValidator(verify_password)]


class UserCredentials(BaseModel):
    email: EmailStr
    password: PasswordField
    name: Optional[str] = None

    """validator in case if user """

    @model_validator(mode="after")
    def set_name_from_email(self):
        if not self.name or not self.name.strip():
            self.name = (
                self.email.split("@")[0]
                .replace("_", " ")
                .replace(".", " ")
            )
        return self


class UserLogin(BaseModel):
    email: str
    password: str


class UserGet(BaseModel):
    id: UUID
    email: str
    name: str

    model_config = ConfigDict(from_attributes=True)
