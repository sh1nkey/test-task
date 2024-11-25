from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import uuid

from config.base import base_config
from sqlalchemy import UUID as sql_UUID

load_dotenv()

DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{base_config.POSTGRES_USER}"
    f":{base_config.POSTGRES_PASSWORD}"
    f"@{base_config.POSTGRES_HOST}"
    f":{base_config.POSTGRES_PORT}"
    f"/{base_config.POSTGRES_DB}"
)
print(DATABASE_URL)

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4, primary_key=True, index=True
    )


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
