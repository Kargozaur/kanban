from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError


def pydantic_exceptions_handler(app: FastAPI) -> None:
    @app.exception_handler(ValidationError)
    async def validation_error(request: Request, exc: ValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "detail": "Pydantic validation error",
                "errors": exc.errors(include_input=False, include_url=False),
            },
        )
