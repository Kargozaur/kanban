from pydantic import (
    BaseModel,
    BeforeValidator,
    EmailStr,
    ConfigDict,
    model_validator,
    Field,
)
from typing import Annotated, Optional
from typing_extensions import Doc
from backend.core.utility.password_verifier import verify_password
from uuid import UUID

PasswordField = Annotated[
    str,
    BeforeValidator(verify_password),
    Doc(
        "Password field for the User registration.\n "
        "Based on verify_password function with the regex within it."
    ),
]


class UserCredentials(BaseModel):
    email: Annotated[
        EmailStr, Field(..., examples=["user@example.com"])
    ]
    password: Annotated[
        PasswordField, Field(examples=["SuperPassword!123"])
    ]
    name: Annotated[
        Optional[str], Field(default=None, examples=["User Name"])
    ]

    """validator in case if user didn't set their name"""

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
    email: Annotated[str, Field(..., examples=["user@example.com"])]
    password: Annotated[
        str, Field(..., examples=["SuperPassword!123"])
    ]


class UserGet(BaseModel):
    id: UUID
    email: str
    name: str

    model_config = ConfigDict(from_attributes=True)
