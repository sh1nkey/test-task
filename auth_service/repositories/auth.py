import uuid
from typing import Optional
from urllib.request import Request

from fastapi import Depends
from fastapi_users import BaseUserManager, UUIDIDMixin

from models.user import User, get_user_db
from config.password_hash_conf import password_helper

SECRET = "SECRET"


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db, password_helper)


async def get_user_manager_f(user_db=Depends(get_user_db)):
    return UserManager(user_db, password_helper)
