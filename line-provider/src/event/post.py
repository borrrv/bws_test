from fastapi import HTTPException, Request

from .models import EventCreateDTO, EventGetDTO
from .router import router


@router.post("/", response_model=EventGetDTO, status_code=201)
def create_one(request: Request, params: EventCreateDTO) -> EventGetDTO:
    """
    Создать событие.
    """
    try:
        result = request.app.state.storage.add_one(params)
    except ValueError:
        raise HTTPException(
            404, detail=f"Event with ID {params.event_id} already exists."
        )
    return result
