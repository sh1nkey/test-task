from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from db.main_db import Base, get_async_session
from schemas.users import UserReadSchema

from sqlalchemy import Boolean, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


class User(Base):

    __tablename__ = "user"

    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def to_read_model(self) -> UserReadSchema:
        return UserReadSchema(id=self.id, email=self.email)
