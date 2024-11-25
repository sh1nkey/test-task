import datetime
from uuid import UUID

from db.main_db import Base


from sqlalchemy import  ForeignKey, text, CheckConstraint

from sqlalchemy.orm import Mapped, mapped_column






class UserBalance(Base):

    __tablename__ = "user_balance"

    user_id: Mapped[UUID] = mapped_column(unique=True)
    balance: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    )

    __table_args__ = (
        CheckConstraint('balance >= 0', name='check_balance_positive'),
    )




class Payment(Base):
    __tablename__ = "payment"

    sender_id: Mapped[UUID] = mapped_column(ForeignKey("user_balance.user_id"))
    receiver_id: Mapped[UUID] = mapped_column(ForeignKey("user_balance.user_id"))

    quantity_money: Mapped[int]

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE ('utc', now())"))

    __table_args__ = (
        CheckConstraint('quantity_money >= 0', name='check_quantity_money_positive'),
    )




