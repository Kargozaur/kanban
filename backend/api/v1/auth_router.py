from fastapi import APIRouter, Depends
from typing import Annotated
from backend.dependancies.user_dep import get_user_service
from backend.services.services.user_service import UserService
from backend.schemas.user_schema import (
    UserCredentials,
    UserGet,
    UserLogin,
)
from backend.schemas.token_schema import TokenResponse

UserSvcDep = Annotated[UserService, Depends(get_user_service)]

user_auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@user_auth_router.post(
    "/sign_up",
    status_code=201,
    response_model=UserGet,
    description="Creates a new user. Name field is optional. \n "
    "If empty, name would be set based on regex and provided email. ",
    response_description="Returns user id, email, name. ",
)
async def sign_up(
    user_credentials: UserCredentials, user_svc: UserSvcDep
):
    return await user_svc.create_user(user_credentials)


@user_auth_router.post(
    "/login",
    status_code=201,
    response_model=TokenResponse,
    description="Compares user credentials. If credentials right, returns a JWT token",
)
async def login(user_credentials: UserLogin, user_svc: UserSvcDep):
    return await user_svc.login_user(user_credentials)
