from collections.abc import Callable

from backend.kanban.core.exceptions.columns_exceptions import ColumnNotFound
from backend.kanban.core.utility.exception_map_keys import ColumnErrorKeys


ERROR_MAP: dict[ColumnErrorKeys, Callable[[], Exception]] = {
    ColumnErrorKeys.NOT_FOUND: lambda: ColumnNotFound(
        "Column with this id is not found"
    )
}
