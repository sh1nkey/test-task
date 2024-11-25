import datetime
from uuid import UUID

from api.dependencies import UOWDep
from db.models import Payment
from schemas.common import PaymentListSchema
from utils_types import PaymentStatuses


class PaymentService:

    @classmethod
    async def get_current_user_payments(
            cls,
            uow: UOWDep,
            *,
            id: UUID,
            status: PaymentStatuses | None = None,
            filtration_date: datetime.datetime | None = None
    ) -> list[PaymentListSchema]:
        async with uow:
            payments: list[Payment] = await uow.payment.get_filtered_payments(
                id,
                status=status,
                filtration_date=filtration_date
            )
        return payments
