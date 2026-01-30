from backend.dependancies.uow_dep import UOWDep
from backend.services.services.board_service import BoardService


def get_board_svc(uow: UOWDep) -> BoardService:
    return BoardService(uow)
