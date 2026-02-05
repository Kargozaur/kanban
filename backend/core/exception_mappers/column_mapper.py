from collections.abc import Callable

from backend.core.exceptions.columns_exceptions import ColumnNotFound
from backend.core.utility.exception_map_keys import ColumnErrorKeys


ERROR_MAP: dict[ColumnErrorKeys, Callable[[], Exception]] = {
    ColumnErrorKeys.NOT_FOUND: lambda: ColumnNotFound(
        "Column with this id is not found"
    )
}
