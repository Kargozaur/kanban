from fastapi import APIRouter, Request, Response

from backend.dependancies.annotated_types import FormData
from backend.dependancies.auth_dep import CurrentUserDep
from backend.dependancies.user_dep import UserSvcDep
from backend.models.models import User
from backend.schemas.token_schema import TokenResponse
from backend.schemas.user_schema import (
    UserCredentials,
    UserGet,
    UserLogin,
)


def create_auth_router() -> APIRouter:
    user_auth_router = APIRouter(prefix="/auth", tags=["Auth"])

    @user_auth_router.post(
        "/sign_up",
        status_code=201,
        description="Creates a new user. Name field is optional. \n "
        "If empty, name would be set based on regex and provided email. ",
        response_description="Returns user id, email, name. ",
    )
    async def sign_up(
        user_credentials: UserCredentials, user_svc: UserSvcDep
    ) -> UserGet:
        return await user_svc.create_user(user_credentials)

    @user_auth_router.post(
        "/login",
        status_code=201,
        description="Compares user credentials. If credentials right, \n"
        "returns a JWT token."
        "Username field expects users email.",
    )
    async def login(
        request: Request,
        response: Response,
        user_svc: UserSvcDep,
        form_data: FormData,
    ) -> TokenResponse | dict[str, str]:
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
    ) -> dict[str, str]:
        response.delete_cookie(key="access_token", httponly=True, samesite="lax")
        return {"message": "Succesfully logged out"}

    @user_auth_router.get("/me", response_model=UserGet)
    async def get_me(current_user: CurrentUserDep) -> User:
        return current_user

    return user_auth_router
