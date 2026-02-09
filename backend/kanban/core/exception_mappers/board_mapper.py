from collections.abc import Callable

from backend.kanban.core.exceptions.board_exceptions import (
    BoardBaseException,
    BoardNotFound,
    BoardPermissionDenied,
)
from backend.kanban.core.utility.exception_map_keys import BoardErrorKeys


ERROR_MAP: dict[BoardErrorKeys, Callable[[], Exception]] = {
    BoardErrorKeys.BASE: lambda: BoardBaseException("Could not create a board"),
    BoardErrorKeys.NOT_FOUND: lambda: BoardNotFound("Board with this id is not found"),
    BoardErrorKeys.PERMISSION_DENIED: lambda: BoardPermissionDenied(
        "You can not perform this action on this board"
    ),
}
