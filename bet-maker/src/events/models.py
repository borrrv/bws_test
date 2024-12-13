from decimal import Decimal

from pydantic import BaseModel

from .enum import EventState


class EventGetDTO(BaseModel):
    event_id: str
    coefficient: Decimal
    deadline: Decimal
    state: EventState

    class Config:
        from_attributes = True


def convert_events(response) -> dict[str, EventGetDTO]:
    events_dict = {
        event.event_id: {
            "event_id": event.event_id,
            "coefficient": event.coefficient,
            "deadline": event.deadline,
            "state": EventState[event.state],
        }
        for event in response.events
    }

    return {key: EventGetDTO(**event) for key, event in events_dict.items()}
