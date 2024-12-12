from multiprocessing.managers import Value

from fastapi import Depends, HTTPException, Request
from sqlalchemy.exc import IntegrityError


from .models import EventCreateDTO, EventGetDTO
from .router import router
import logging


@router.post("/", response_model=EventGetDTO, status_code=201)
def create_one(request: Request, params: EventCreateDTO) -> EventGetDTO:
    try:
        result = request.app.state.storage.add_one(params)
    except ValueError as e:
        raise HTTPException(404, detail=f"Event with ID {params.event_id} already exists.")
    return result
