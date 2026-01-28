from backend.dependancies.annotated_types import BoardRepoDep
from backend.services.services.board_service import BoardService


def get_board_svc(board_repo: BoardRepoDep) -> BoardService:
    return BoardService(board_repo)
