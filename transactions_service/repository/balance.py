from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import update, func, Integer

from config.repo_conf import SQLAlchemyRepository
from db.models import UserBalance


class BalanceRepository(SQLAlchemyRepository):
    model = UserBalance

    async def increase_balance(self, *, id: UUID, quantity_money: int) -> None:
        stmt = (
            update(UserBalance)
            .where(UserBalance.user_id == id)
            .values(balance=UserBalance.balance + func.cast(quantity_money, Integer))
            .returning(UserBalance.balance)
        )

        result = await self.session.execute(stmt)
        updated_balance = result.fetchone()

        if not updated_balance:
            await self._create_if_no_balance(updated_balance)

    async def decrease_balance(self, *, id: UUID, quantity_money: int) -> None:

        stmt = (
            update(UserBalance)
            .where(UserBalance.user_id == UUID(id))
            .values(balance=UserBalance.balance - func.cast(quantity_money, Integer))
            .returning(UserBalance.balance)
        )

        result = await self.session.execute(stmt)
        updated_balance = result.fetchone()

        if not updated_balance:
            await self._create_if_no_balance()

    async def _create_if_no_balance(self):
        await self.session.rollback()

        new_balance = UserBalance(user_id=id)
        self.session.add(new_balance)
        await self.session.commit()

        raise HTTPException(
            status_code=400,
            detail="Не смогли оплатить, потому что баланс пользователя равен нулю. Попробуйте ещё раз"
        )
