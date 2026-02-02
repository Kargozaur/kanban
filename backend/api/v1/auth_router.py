from fastapi import APIRouter, Depends, Response, Request
from typing import Annotated
from backend.dependancies.user_dep import get_user_service
from backend.dependancies.auth_dep import CurrentUserDep
from backend.dependancies.annotated_types import FormData
from backend.services.services.user_service import UserService
from backend.schemas.user_schema import (
    UserCredentials,
    UserGet,
    UserLogin,
)


def create_auth_router():
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
        description="Compares user credentials. If credentials right, returns a JWT token. \n"
        "Username field expects users email.",
    )
    async def login(
        request: Request,
        response: Response,
        user_svc: UserSvcDep,
        form_data: FormData,
    ):
        existing_token = request.cookies.get("access_token")
        if existing_token:
            return {"message": "You are already logged in"}
        user_credentials = UserLogin(
            email=form_data.username, password=form_data.password
        )
        token = await user_svc.login_user(user_credentials)
        response.set_cookie(
            key="access_token",
            value=token.access_token,
            httponly=True,
            max_age=3600,
            samesite="lax",
        )
        return token

    @user_auth_router.post("/logout")
    async def logout(
        response: Response, current_user: CurrentUserDep
    ):
        response.delete_cookie(
            key="access_token", httponly=True, samesite="lax"
        )
        return {"message": "Succesfully logged out"}

    @user_auth_router.get("/me", response_model=UserGet)
    async def get_me(current_user: CurrentUserDep):
        return current_user

    return user_auth_router
