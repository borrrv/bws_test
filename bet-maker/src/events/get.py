from fastapi import HTTPException, Request

from src.events.router import router
from src.grpc_event import grpc_client

from .models import EventGetDTO


@router.get("/all", response_model=dict[str, EventGetDTO], status_code=200)
async def get_list_all(request: Request) -> dict[str, EventGetDTO]:
    """
    Возвращает список всех событий.
    """
    try:
        message = await grpc_client.get_event_all()
        return message
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=dict[str, EventGetDTO], status_code=200)
async def get_list(request: Request) -> dict[str, EventGetDTO]:
    """
    Возвращает список событий, на которые можно совершить ставку.
        Таковыми считаются все события, для которых ещё не наступил дедлайн для ставок
    """
    try:
        message = await grpc_client.get_event()
        return message
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
