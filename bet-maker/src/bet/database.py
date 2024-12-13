from decimal import Decimal

from sqlalchemy import BigInteger, Enum, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from src.core.database import AbstractBase

from .enums import StatusBetEnum


class Bet(AbstractBase):
    __tablename__ = "bet"
    id: Mapped[str] = mapped_column(
        BigInteger, unique=True, primary_key=True, auto_increment=True
    )
    event_id: Mapped[str] = mapped_column(String)
    bet_amount: Mapped[Decimal] = mapped_column(Numeric)
    status: Mapped[str] = mapped_column(
        Enum(StatusBetEnum), default=StatusBetEnum.NOT_PLAYED
    )
