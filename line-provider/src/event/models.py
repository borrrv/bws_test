from pydantic import BaseModel
import decimal
from .enum import EventState

class EventCreateDTO(BaseModel):
    event_id: str
    coefficient: decimal.Decimal
    deadline: decimal.Decimal
    state: EventState

class EventUpdateDTO(BaseModel):
    coefficient: decimal.Decimal | None = None
    deadline: decimal.Decimal | None = None
    state: EventState | None = None

class EventPatchDTO(BaseModel):
    state: EventState

class EventGetDTO(EventCreateDTO):

    class Config:
        from_attributes = True