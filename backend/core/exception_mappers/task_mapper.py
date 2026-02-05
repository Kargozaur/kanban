from collections.abc import Callable

from backend.core.exceptions.board_exceptions import BoardNotFound
from backend.core.exceptions.columns_exceptions import ColumnNotFound
from backend.core.exceptions.exceptions import NotFoundError
from backend.core.exceptions.tasks_exception import (
    TaskConflict,
    TaskCreationFail,
    TaskNotFound,
)
from backend.core.utility.exception_map_keys import TaskErrorKeys


ERROR_MAP: dict[TaskErrorKeys, Callable[[], Exception]] = {
    TaskErrorKeys.CONFLICT: lambda: TaskConflict(
        "You can not add more tasks to the column"
    ),
    TaskErrorKeys.CREATION_FAIL: lambda: TaskCreationFail("Failed to create a task"),
    TaskErrorKeys.NOT_FOUND: lambda: TaskNotFound("Task with this id is not found"),
    TaskErrorKeys.COLUMT_NOT_FOUND: lambda: ColumnNotFound(
        "Column with this id is not found"
    ),
    TaskErrorKeys.BOARD_NOT_FOUND: lambda: BoardNotFound(
        "Board with this id is not found"
    ),
    TaskErrorKeys.USER_NOT_FOUND: lambda: NotFoundError(),
}
