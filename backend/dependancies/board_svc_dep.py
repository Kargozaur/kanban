from fastapi import Depends
from backend.dependancies.uow_dep import UOWDep
from backend.services.services.board_service import BoardService
from typing import Annotated


def get_board_svc(uow: UOWDep) -> BoardService:
    return BoardService(uow)


BoardSvcDep = Annotated[BoardService, Depends(get_board_svc)]
