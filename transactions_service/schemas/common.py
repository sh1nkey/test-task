import datetime
from typing import Literal
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel, Field

from utils_types import PaymentStatuses


class MessageErrorSchema(BaseModel):
    error: str


class PaymentListSchema(BaseModel):
    sender_id: UUID
    receiver_id: UUID
    quantity_money: int
    created_at: datetime.datetime


class StatusSchema(BaseModel):
    status: Literal["sent"] | Literal["received"] = Query(description="query x")


