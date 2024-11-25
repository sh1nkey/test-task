from sqlalchemy import select, exists

from models.user import User
from config.repo_conf import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User

    async def find_one(self, id: str):
        stmt_done = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )

        return stmt_done.scalar_one_or_none()


    async def check_exists(self, id: str) -> bool:
        """
        SELECT EXISTS (
            SELECT 1
            FROM "user"
            WHERE "user".id = '7e2589e8-5dcc-49ce-8ccf-57396342dd5d'
        );
        """
        stmt_done = await self.session.execute(
            select(exists().where(self.model.id == id))
        )

        return bool(stmt_done.scalar())

