import datetime
from enum import StrEnum
from typing import Literal, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Header, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_pagination import Page, LimitOffsetPage
from starlette import status

from api.dependencies import UOWDep
from protos.client import get_user, get_current_user
from schemas.common import MessageErrorSchema, StatusSchema, PaymentListSchema
from services.balance import BalanceService
from services.payment import PaymentService
from utils_types import UserDict, PaymentStatuses

router = APIRouter(prefix="/profile", tags=["Профиль"])

auth_scheme = HTTPBearer()


# POST перевод с проверкой баланса перед завершением транзакции
# GET просмотр c пагинацией и фильтрами



@router.post(
    "/transfer",
    summary="Эндпоинт перевода денег для другого пользователя",
    response_description="Описание пользователя",
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": MessageErrorSchema, "description": "Возникшая ошибка"},
    },
)
async def send_money(
        uow: UOWDep,
        money: int,
        receiver_id: str,
        user: UserDict = Depends(get_current_user),
):

    await BalanceService.send_money(
        uow,
        money=money,
        sender_id=str(user["id"]),
        receiver_id=str(receiver_id)
    )









@router.get(
    "/my-transactions",
    summary="Показывает данные о транзакциях вошедшего пользователя",
    response_description="Описание пользователя",
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": MessageErrorSchema, "description": "Возникшая ошибка"},
    },
    response_model=LimitOffsetPage[PaymentListSchema]
)
async def get_transaction_data(
        uow: UOWDep,
        status: Optional[PaymentStatuses] = None,
        date: datetime.datetime | None = Query(None),
        user: UserDict = Depends(get_current_user),
):
    return await PaymentService.get_current_user_payments(
        uow,
        id=UUID(user["id"]),
        status=status,
        filtration_date=date
    )
