from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)


def base_exception_handler(app: FastAPI):
    @app.exception_handler(Exception)
    async def other_exceptions(request: Request, exc: Exception):
        logger.exception(msg="Python base exception")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": exc.__class__.__name__},
            headers=getattr(exc, "headers", None),
        )
