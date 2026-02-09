from fastapi import APIRouter

from backend.kanban.api.v1.auth_router import create_auth_router
from backend.kanban.api.v1.board_router import create_board_router


def create_api_router() -> APIRouter:
    api_router = APIRouter(prefix="/api")
    v1_router = APIRouter(prefix="/v1", tags=["v1"])
    v1_router.include_router(create_auth_router())
    v1_router.include_router(create_board_router())

    api_router.include_router(v1_router)
    return api_router
