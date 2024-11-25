import uuid
from typing import Annotated, Optional

import jwt

from fastapi import Depends, HTTPException
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    JWTStrategy,
    AuthenticationBackend,
    BearerTransport,
)
from fastapi_users.jwt import decode_jwt
from fastapi.security import OAuth2PasswordBearer

from jwt import InvalidTokenError
from pydantic import BaseModel
from starlette import status

from models.user import User
from repositories.auth import get_user_manager
from services.user import UserService

from config.uow_conf import IUnitOfWork, UnitOfWork
from utils_typing import UserDict

SECRET = "SECRET"

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


class JWTStrategyCustom(JWTStrategy):
    def id_from_token(self, token: Optional[str]) -> Optional[uuid.UUID]:
        if token is None:
            return None

        data = decode_jwt(
            token, self.decode_key, self.token_audience, algorithms=[self.algorithm]
        )

        user_id = data.get("sub")
        if user_id is None:
            return None

        return user_id


def get_jwt_strategy() -> JWTStrategyCustom:
    return JWTStrategyCustom(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)


class Token(BaseModel):
    access_token: str
    token_type: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/jwt/login")


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        uow: IUnitOfWork = Depends(UnitOfWork),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return await user_ex_token(token, uow, credentials_exception)


async def user_ex_token(token: str, uow: IUnitOfWork, exception: Exception) -> UserDict | None:
    id = get_jwt_strategy().id_from_token(token)


    return await UserService.find_user(uow, id)
