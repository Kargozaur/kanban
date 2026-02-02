class ColumnBaseException(Exception):
    status_code = 500
    detail = "Column base exception"

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__()

    def __str__(self) -> str:
        return f"{self.message}"


class ColumnNotFound(ColumnBaseException):
    status_code = 404
    detail = "Column with this id is not found"

    def __init__(self, message: str) -> None:
        super().__init__(message)
