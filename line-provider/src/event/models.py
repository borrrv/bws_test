import decimal
from decimal import Decimal, InvalidOperation

from pydantic import BaseModel, field_validator

from .enum import EventState


class EventCreateDTO(BaseModel):
    event_id: str
    coefficient: decimal.Decimal
    deadline: decimal.Decimal
    state: EventState

    @field_validator("coefficient", mode="before")
    def validate_coefficient(cls, values):
        try:
            coefficient = Decimal(values).quantize(
                Decimal("0.01"), rounding="ROUND_HALF_UP"
            )
        except (InvalidOperation, ValueError):
            raise ValueError("Invalid coefficient format. Must be a decimal number.")
        values = coefficient
        return values


class EventUpdateDTO(BaseModel):
    coefficient: decimal.Decimal | None = None
    deadline: decimal.Decimal | None = None
    state: EventState | None = None


class EventPatchDTO(BaseModel):
    state: EventState


class EventGetDTO(EventCreateDTO):

    class Config:
        from_attributes = True
