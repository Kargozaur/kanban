from typing import Annotated
from fastapi import Depends
from backend.dependancies.states import get_hasher, get_token_svc
from backend.core.security.password_hasher import PasswordHasher
from backend.core.security.token_svc import TokenSvc

TokenDep = Annotated[TokenSvc, Depends(get_token_svc)]
PasswordDep = Annotated[PasswordHasher, Depends(get_hasher)]
