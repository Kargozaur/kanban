from fastapi import APIRouter

from backend.core.utility.role_enum import RoleEnum
from backend.dependencies.auth_dep import CurrentUserDep
from backend.dependencies.permission_dep import PermissionDep
from backend.dependencies.service_dependencies.member_svc_dep import MemberSvcDep
from backend.schemas.member_schema import (
    AddBoardMemberEmail,
    MemberResponse,
    UpdateBoardMember,
)


def create_member_router() -> APIRouter:
    member_router = APIRouter(
        prefix="/{board_id}/members", tags=["Board", "BoardMembers"]
    )

    @member_router.post(
        "/add",
        dependencies=[PermissionDep([RoleEnum.ADMIN])],
        status_code=201,
        description="Post method for the router. board_id is a path parameter, \n "
        "and user_data is a body",
    )
    async def add_member(
        board_id: int,
        user_data: AddBoardMemberEmail,
        member_svc: MemberSvcDep,
    ) -> MemberResponse:
        return await member_svc.add_member_to_the_board(
            board_id=board_id, user_data=user_data
        )

    @member_router.patch(
        "/update",
        dependencies=[PermissionDep([RoleEnum.ADMIN])],
        status_code=200,
        description="Update method for the router. board_id is a path parameter, \n"
        "update_member is a body",
    )
    async def update_role(
        board_id: int,
        update_member: UpdateBoardMember,
        member_svc: MemberSvcDep,
        current_user: CurrentUserDep,
    ) -> MemberResponse:
        return await member_svc.update_user_role(
            board_id=board_id, user_data=update_member, current_user=current_user.id
        )

    @member_router.delete(
        "/delete_member/{email}",
        dependencies=[PermissionDep([RoleEnum.ADMIN])],
        status_code=204,
        description="Delete method for the router. Email and board_id \n"
        "are both Path parameters.",
    )
    async def delete_user(
        board_id: int,
        email: str,
        member_svc: MemberSvcDep,
        current_user: CurrentUserDep,
    ) -> None:
        await member_svc.delete_user_from_the_board(
            board_id=board_id, user_email=email, current_user=current_user.id
        )

    return member_router
