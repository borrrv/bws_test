from decimal import ROUND_HALF_UP, Decimal

from pydantic import BaseModel, field_validator

from .enums import StatusBetEnum


class CreateOneDTO(BaseModel):
    event_id: str
    bet_amount: Decimal


class GetOneDTO(BaseModel):
    id: int
    event_id: str
    bet_amount: Decimal
    status: StatusBetEnum

    class Config:
        from_attributes = True

    @field_validator("bet_amount")
    def bet_amount(cls, v):
        if v <= 0:
            raise ValueError("Only positive numbers allowed")
        v = v.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return v
