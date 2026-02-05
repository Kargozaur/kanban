from fastapi import Request

from backend.core.security.password_hasher import PasswordHasher
from backend.core.security.token_svc import TokenSvc
from backend.core.settings.settings import AppSettings


def get_settings(request: Request) -> AppSettings:
    return request.app.state.settings


def get_hasher(request: Request) -> PasswordHasher:
    return request.app.state.hasher


def get_token_svc(request: Request) -> TokenSvc:
    return request.app.state.token
