from fastapi import APIRouter, Depends, Response
from backend.core.utility.role_enum import RoleEnum
from backend.services.services.board_service import BoardService
from backend.dependancies.board_svc_dep import get_board_svc
from backend.dependancies.permission_dep import CurrentUserDep
from backend.dependancies.annotated_types import PaginationDep
from backend.dependancies.permission_dep import PermissionDep
from backend.schemas.board_schema import (
    BoardCreate,
    BoardGet,
    BoardFullView,
    BoardUpdate,
)
from typing import Annotated

BoardSvcDep = Annotated[BoardService, Depends(get_board_svc)]

board_router = APIRouter(prefix="/board", tags=["Board"])


@board_router.post("/", status_code=201, response_model=BoardGet)
async def create_board(
    board_svc: BoardSvcDep,
    current_user: CurrentUserDep,
    board_data: BoardCreate,
):
    return await board_svc.create_board(
        owner_id=current_user.id, board_data=board_data
    )


@board_router.get(
    "/all", status_code=200, response_model=list[BoardGet]
)
async def get_all_boards(
    board_svc: BoardSvcDep,
    current_user: CurrentUserDep,
    pagination: PaginationDep,
):
    return await board_svc.get_boards(
        owner_id=current_user.id, pagination=pagination
    )


@board_router.get("/{id}", response_model=BoardFullView)
async def get_full_board(
    id: int, board_svc: BoardSvcDep, current_user: CurrentUserDep
):
    return await board_svc.get_board(owner_id=current_user.id, id=id)


@board_router.patch(
    "/{id}",
    response_model=BoardGet,
    status_code=200,
    dependencies=[PermissionDep([RoleEnum.ADMIN])],
)
async def update_board(
    id: int, board_svc: BoardSvcDep, new_data: BoardUpdate
):
    return await board_svc.update_board(
        id=id, data_to_update=new_data
    )


@board_router.delete(
    "/{id}", dependencies=[PermissionDep([RoleEnum.ADMIN])]
)
async def delete_board(id: int, board_svc: BoardSvcDep):
    result = await board_svc.delete_board(id)
    return Response(status_code=204, content={"detail": result})
