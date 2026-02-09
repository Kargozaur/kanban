class TaskBaseException(Exception):
    status_code = 500
    detail = "Task base exception"

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__()

    def __str__(self) -> str:
        return f"{self.message}"


class TaskNotFound(TaskBaseException):
    status_code = 404
    detail = "Could not validate the task"

    def __init__(self, message: str) -> None:
        super().__init__(message)


class TaskConflict(TaskBaseException):
    status_code = 409
    detail = "Could not add the task"

    def __init__(self, message: str) -> None:
        super().__init__(message)


class TaskCreationFail(TaskBaseException):
    status_code = 400
    detail = "Failed to create a task"

    def __init__(self, message: str) -> None:
        super().__init__(message)
