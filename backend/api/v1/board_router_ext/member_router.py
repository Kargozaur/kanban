from fastapi import APIRouter, Depends
from backend.core.utility.role_enum import RoleEnum
from backend.services.services.member_service import MemberService
from backend.dependancies.member_svc_dep import get_member_svc
from backend.dependancies.permission_dep import PermissionDep
from backend.schemas.member_schema import (
    AddBoardMemberEmail,
    UpdateBoardMember,
)
from typing import Annotated


def create_member_router():
    MemberSvcDep = Annotated[MemberService, Depends(get_member_svc)]
    member_router = APIRouter(
        prefix="/{board_id}", tags=["Board", "BoardMembers"]
    )

    @member_router.post(
        "/members/add",
        dependencies=[PermissionDep([RoleEnum.ADMIN])],
        status_code=201,
        description="Post method for the router. board_id is a path parameter, \n "
        "and user_data is a body",
    )
    async def add_member(
        board_id: int,
        user_data: AddBoardMemberEmail,
        member_svc: MemberSvcDep,
    ):
        return await member_svc.add_member_to_the_board(
            board_id=board_id, user_data=user_data
        )

    @member_router.patch(
        "/members/update",
        dependencies=[PermissionDep([RoleEnum.ADMIN])],
        status_code=200,
        description="Update method for the router. board_id is a path parameter, \n"
        "update_member is a body",
    )
    async def update_role(
        board_id: int,
        update_member: UpdateBoardMember,
        member_svc: MemberSvcDep,
    ):
        return await member_svc.update_user_role(
            board_id=board_id, user_data=update_member
        )

    @member_router.delete(
        "/members/delete_member/{email}",
        dependencies=[PermissionDep([RoleEnum.ADMIN])],
        status_code=204,
        description="Delete method for the router. Email and board_id \n"
        "are both Path parameters.",
    )
    async def delete_user(
        board_id: int,
        email: str,
        member_svc: MemberSvcDep,
    ):
        await member_svc.delete_user_from_the_board(
            board_id=board_id, user_email=email
        )

    return member_router
