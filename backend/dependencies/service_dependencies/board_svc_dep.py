from typing import Annotated

from fastapi import Depends
from typing_extensions import Doc

from backend.dependencies.uow_dep import UOWDep
from backend.services.services.board_service import BoardService


def get_board_svc(uow: UOWDep) -> BoardService:
    return BoardService(uow)


BoardSvcDep = Annotated[
    BoardService,
    Depends(get_board_svc),
    Doc("dependency for the general board router"),
]
