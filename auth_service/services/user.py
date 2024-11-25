from uuid import UUID

from fastapi import HTTPException
from starlette import status

from config.uow_conf import IUnitOfWork

from utils_typing import UserDict


class UserService:
    @staticmethod
    async def find_user(uow: IUnitOfWork, id: str) -> UserDict:
        user_data = {}
        async with uow:
            user_query = await uow.users.find_one(UUID(id))
            if user_query:
                user_data["id"] = user_query.id
                user_data["email"] = user_query.email

        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователя с таким id нет в базе данных",
            )

        return user_data

    @staticmethod
    async def check_exist(uow: IUnitOfWork, id: str) -> bool:
        async with uow:
            user_exists: bool = await uow.users.check_exists(id)

        return user_exists
