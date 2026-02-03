from typing import Annotated

from fastapi import Depends
from typing_extensions import Doc

from backend.dependancies.uow_dep import UOWDep
from backend.services.services.board_service import BoardService


def get_board_svc(uow: UOWDep) -> BoardService:
    return BoardService(uow)


BoardSvcDep = Annotated[
    BoardService,
    Depends(get_board_svc),
    Doc("Dependancy for the general board router"),
]
