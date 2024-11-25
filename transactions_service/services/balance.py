import logging
from asyncio import TaskGroup
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from config.uow_conf import IUnitOfWork
from protos.client import get_user, check_recipient_exists

logger = logging.getLogger("uvicorn.error")


class BalanceService:

    @classmethod
    async def send_money(self, uow: IUnitOfWork, *, money: int, sender_id: UUID, receiver_id: UUID) -> None:
        await self._check_receiver_exist(receiver_id)  # check existence

        async with uow:
            try:
                await uow.balance.increase_balance(id=receiver_id, quantity_money=money)
                await uow.balance.decrease_balance(id=sender_id, quantity_money=money)
            except IntegrityError as e:
                await uow.rollback()
                logger.error(f"При переводе случилась ошибка. Текст: {str(e)}")
                raise HTTPException(status_code=400, detail="Ошибка при переводе средств")

            await uow.payment.create_payment(
                sender_id=sender_id,
                receiver_id=receiver_id,
                quantity_money=money
            )
            await uow.commit()
            logger.info(f"Перевод в {round(money / 100, 2)} руб был успешно завершён")


    @staticmethod
    async def _check_receiver_exist(receiver_id: UUID | str) -> None:
        await check_recipient_exists(receiver_id)





