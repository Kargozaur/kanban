from fastapi import APIRouter, Depends, Response, Body
from backend.core.utility.role_enum import RoleEnum
from backend.services.services.board_service import BoardService
from backend.dependancies.board_svc_dep import get_board_svc
from backend.dependancies.member_svc_dep import get_member_svc
from backend.dependancies.permission_dep import CurrentUserDep
from backend.dependancies.annotated_types import PaginationDep
from backend.dependancies.permission_dep import PermissionDep
from backend.services.services.member_service import MemberService
from backend.schemas.board_schema import (
    BoardCreate,
    BoardGet,
    BoardUpdate,
)
from backend.schemas.member_schema import (
    AddBoardMemberEmail,
    UpdateBoardMember,
)
from typing import Annotated

BoardSvcDep = Annotated[BoardService, Depends(get_board_svc)]
MemberSvcDep = Annotated[MemberService, Depends(get_member_svc)]

board_router = APIRouter(prefix="/board", tags=["Board"])


@board_router.post(
    "/",
    status_code=201,
    response_model=BoardGet,
    description="Endpoint to create a new board",
    response_description="Returns board id, name, description, created and owner.",
)
async def create_board(
    board_svc: BoardSvcDep,
    current_user: CurrentUserDep,
    board_data: BoardCreate,
):
    return await board_svc.create_board(
        owner_id=current_user.id, board_data=board_data
    )


@board_router.get(
    "/all",
    status_code=200,
    description="Returns all boards where user presented",
    response_description="returns a list of all the boards, where user exists",
)
async def get_all_boards(
    board_svc: BoardSvcDep,
    current_user: CurrentUserDep,
    pagination: PaginationDep,
):
    return await board_svc.get_boards(
        user_id=current_user.id, pagination=pagination
    )


@board_router.get(
    "/{id}",
    description="Gets a full about the board",
    response_description="Gets a full data about the Board",
)
async def get_full_board(
    id: int, board_svc: BoardSvcDep, current_user: CurrentUserDep
):
    return await board_svc.get_board(user_id=current_user.id, id=id)


@board_router.patch(
    "/{board_id}",
    status_code=200,
    dependencies=[PermissionDep([RoleEnum.ADMIN])],
    description="Updates board based on data provided. User has to have admin role to perform this action",
)
async def update_board(
    board_id: int, board_svc: BoardSvcDep, new_data: BoardUpdate
):
    return await board_svc.update_board(
        board_id=board_id, data_to_update=new_data
    )


@board_router.delete(
    "/{board_id}",
    dependencies=[PermissionDep([RoleEnum.ADMIN])],
    description="Deletes board. User has to have an admin role to perform this action",
)
async def delete_board(board_id: int, board_svc: BoardSvcDep):
    await board_svc.delete_board(board_id)
    return Response(status_code=204)


@board_router.post(
    "/{board_id}/members/add",
    dependencies=[PermissionDep([RoleEnum.ADMIN])],
    status_code=201,
)
async def add_member(
    board_id: int,
    user_data: AddBoardMemberEmail,
    member_svc: MemberSvcDep,
):
    return await member_svc.add_member_to_the_board(
        board_id=board_id, user_data=user_data
    )


@board_router.patch(
    "/{board_id}/members/update",
    dependencies=[PermissionDep([RoleEnum.ADMIN])],
    status_code=200,
)
async def update_role(
    board_id: int,
    update_member: UpdateBoardMember,
    member_svc: MemberSvcDep,
):
    return await member_svc.update_user_role(
        board_id=board_id, user_data=update_member
    )


@board_router.delete(
    "/{board_id}/members/delete_member",
    dependencies=[PermissionDep([RoleEnum.ADMIN])],
    status_code=204,
)
async def delete_user(
    board_id: int, email: str, member_svc: MemberSvcDep
):
    await member_svc.delete_user_from_the_board(
        board_id=board_id, user_email=email
    )
