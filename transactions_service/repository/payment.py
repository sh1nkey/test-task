import datetime

from sqlalchemy import UUID, select, and_

from config.repo_conf import SQLAlchemyRepository
from db.models import Payment
from utils_types import PaymentStatuses

from fastapi_pagination.ext.sqlalchemy import paginate

class PaymentRepository(SQLAlchemyRepository):
    model = Payment

    async def create_payment(
            self,
            *,
            sender_id: UUID,
            receiver_id: UUID,
            quantity_money: int,
    ) -> None:
        new_payment = self.model(
            sender_id=sender_id,
            receiver_id=receiver_id,
            quantity_money=quantity_money
        )
        self.session.add(new_payment)

    async def get_filtered_payments(
            self,
            id: UUID,
            *,
            status: PaymentStatuses | None = None,
            filtration_date: datetime.datetime | None = None
    ):
        stmt = select(self.model)

        conditions = []

        if status:
            if status.value == PaymentStatuses.SENT.value:
                conditions.append(self.model.sender_id == id)

            elif status.value == PaymentStatuses.RECIEVED.value:
                conditions.append(self.model.receiver_id == id)

        if filtration_date is not None:
            conditions.append(self.model.created_at >= filtration_date)


        if conditions:
            stmt = stmt.where(and_(*conditions))


        return await paginate(
            self.session,
            stmt
        )
