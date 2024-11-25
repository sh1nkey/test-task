import logging

from fastapi import APIRouter, Depends, Body
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_users import BaseUserManager
from pydantic import EmailStr
from starlette import status
from fastapi_users import exceptions, models
from api.dependencies import UOWDep

from config.orjson import CusomORJSONResponse

from repositories.auth import get_user_manager

from schemas.common import MessageErrorSchema

from config.jwt_conf import get_current_user
from utils_typing import UserDict

router = APIRouter(prefix="/profile", tags=["Профиль"])

auth_scheme = HTTPBearer()

logger = logging.getLogger('uvicorn.info')


@router.get(
    "/me",
    summary="Показывает данные о вошедшем пользователе",
    response_description="Описание пользователя",
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": MessageErrorSchema, "description": "Возникшая ошибка"},
    },
)
async def get_profile(
        uow: UOWDep,
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)
):
    try:
        user_data: UserDict = await get_current_user(token.credentials, uow)
        response = CusomORJSONResponse(user_data, status_code=status.HTTP_200_OK)
        logger.info(f"Пользователь {user_data['email']} успешно получил информацию о своём профиле")
        return response
    except Exception:
        logger.error("Ошибка при получении профиля")
        raise


@router.post(
    "/forgot-password",
    status_code=status.HTTP_201_CREATED,
    name="reset:forgot_password",
)
async def forgot_password(
        uow: UOWDep,
        password_new: str = Body(...),
        email: EmailStr = Body(..., embed=True),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme),
        user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
):
    try:
        user = await user_manager.get_by_email(email)
        await user_manager._update(user, {"password": password_new})
        logger.info(f"Пользователь {user.email} успешно обновил свой пароль")
    except Exception:
        logger.error("Ошибка при обновлении пароля")
        raise
