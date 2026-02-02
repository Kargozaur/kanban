from fastapi import APIRouter, Depends, Response
from backend.core.utility.role_enum import RoleEnum
from backend.services.services.board_service import BoardService
from backend.dependancies.board_svc_dep import get_board_svc
from backend.dependancies.permission_dep import CurrentUserDep
from backend.dependancies.annotated_types import PaginationDep
from backend.dependancies.permission_dep import PermissionDep
from backend.api.v1.board_router_ext.member_router import (
    create_member_router,
)
from backend.schemas.board_schema import (
    BoardCreate,
    BoardGet,
    BoardUpdate,
)

from typing import Annotated


def create_board_router():
    BoardSvcDep = Annotated[BoardService, Depends(get_board_svc)]
    board_router = APIRouter(prefix="/board", tags=["Board"])
    board_router.include_router(create_member_router())

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
        return await board_svc.get_board(
            user_id=current_user.id, id=id
        )

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

    return board_router
