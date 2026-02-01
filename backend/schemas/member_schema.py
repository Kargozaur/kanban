from pydantic import BaseModel, Field
from backend.core.utility.role_enum import RoleEnum
from typing import Annotated
from uuid import UUID


class AddBoardMemberBase(BaseModel):
    role: Annotated[
        RoleEnum,
        Field(
            RoleEnum.VIEWER,
            examples=[
                "admin",
                "viewer",
                "member",
            ],
            description="By default ads user as a viewer. \n"
            "This behavior may be adjusted with the patch request \n"
            "by the user with role of the admin",
        ),
    ]


class AddBoardMemberEmail(AddBoardMemberBase):
    email: Annotated[
        str,
        Field(
            ...,
            description="Id of the user from the appropriate table",
        ),
    ]


class AddBoardMemberUUID(AddBoardMemberBase):
    user_id: Annotated[
        UUID, Field(..., description="User's id from the database")
    ]


class UpdateBoardMember(BaseModel):
    email: str
    role: Annotated[
        RoleEnum,
        Field(
            default=RoleEnum.VIEWER,
            description="Changes the role of the user inside the board",
        ),
    ]
