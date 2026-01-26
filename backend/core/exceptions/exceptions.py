class AppBaseException(Exception):
    status_code: int = 500
    detail: str = "Internal server error"
    headers: dict[str, str] | None = None


class NotFoundError(AppBaseException):
    status_code = 404
    detail = "Resource not found"


class InvalidCredentialsError(AppBaseException):
    status_code = 401
    detail = "Could not validate credentials"
    headers = {"WWW-Authenticate": "Bearer"}


class TokenError(AppBaseException):
    status_code = 401
    detail = "Could not validate your token"
    headers = {"WWW-Authenticate": "Bearer"}
