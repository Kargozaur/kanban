from typing import Annotated, Self
from uuid import UUID

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    EmailStr,
    Field,
    model_validator,
)
from typing_extensions import Doc

from backend.kanban.core.utility.password_verifier import verify_password
from backend.kanban.schemas.generic import GenericId


PasswordField = Annotated[
    str,
    BeforeValidator(verify_password),
    Doc(
        "Password field for the User registration.\n "
        "Based on verify_password function with the regex within it."
    ),
]


class UserCredentials(BaseModel):
    email: Annotated[EmailStr, Field(..., examples=["user@example.com"])]
    password: Annotated[PasswordField, Field(examples=["SuperPassword!123"])]
    name: Annotated[str | None, Field(default=None, examples=["User Name"])]

    """validator in case if user didn't set their name"""

    @model_validator(mode="after")
    def set_name_from_email(self) -> Self:
        if not self.name or not self.name.strip():
            self.name = self.email.split("@")[0].replace("_", " ").replace(".", " ")
        return self


class UserLogin(BaseModel):
    email: Annotated[str, Field(..., examples=["user@example.com"])]
    password: Annotated[str, Field(..., examples=["SuperPassword!123"])]


class UserGetForTotal(BaseModel):
    email: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserGet(UserGetForTotal, GenericId[UUID]):
    pass
