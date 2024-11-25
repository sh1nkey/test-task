from enum import StrEnum, Enum

from typing_extensions import TypedDict


class UserDict(TypedDict):
    email: str
    id: str


class PaymentStatuses(StrEnum):
    SENT = "send"
    RECIEVED = "receive"


