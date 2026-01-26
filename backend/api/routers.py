from fastapi import APIRouter
from backend.api.v1.auth_router import user_auth_router

api_router = APIRouter(prefix="/api")
v1_router = APIRouter(prefix="/v1", tags=["v1"])
v1_router.include_router(user_auth_router)


api_router.include_router(v1_router)
