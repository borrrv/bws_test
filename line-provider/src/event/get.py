from fastapi import HTTPException, Request

from .models import EventGetDTO
from .router import router


@router.get("/{_id}", response_model=EventGetDTO, status_code=200)
def get_one(request: Request, _id: str) -> EventGetDTO:
    """
    Получение события по его id.
    """
    event = request.app.state.storage.get_one(_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return event


@router.get("/all/", response_model=dict[str, EventGetDTO], status_code=200)
def get_list_all(request: Request) -> dict[str, EventGetDTO]:
    """
    Получение всех событий.
    """
    return request.app.state.storage.get_storage


@router.get("/", response_model=dict[str, EventGetDTO], status_code=200)
def get_list(request: Request) -> dict[str, EventGetDTO]:
    """
    Возвращает список событий, на которые можно совершить ставку.
    """
    return request.app.state.storage.get_valid_event()
