from fastapi import HTTPException, Request

from .models import EventPatchDTO
from .router import router


@router.patch("/{_id}", status_code=204)
async def patch_one(request: Request, _id: str, data: EventPatchDTO):
    """
    Обновить статус события.
    """
    existing_event = request.app.state.storage.get_one(_id)
    if not existing_event:
        raise HTTPException(status_code=404, detail=f"Event with id {_id} not found")
    updated_data = existing_event.copy(update=data.model_dump(exclude_unset=True))
    request.app.state.storage.set_one(_id, updated_data)
    await request.app.state.rabbitmq.publish_message(
        {"status": data.state.value, "event_id": _id}
    )
    return
