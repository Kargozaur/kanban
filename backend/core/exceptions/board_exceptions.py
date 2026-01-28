class BoardBaseException(Exception):
    status_code = 500
    detail = "Board Exception"

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__()

    def __str__(self) -> str:
        return f"{self.message}"


class BoardNotFound(BoardBaseException):
    status_code = 404
    detail = "Board not found"

    def __init__(self, message: str) -> None:
        super().__init__(message)


class BoardPermissionDenied(BoardBaseException):
    status_code = 403
    detail = "Permission denied"

    def __init__(self, message: str) -> None:
        super().__init__(message)
