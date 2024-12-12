from fastapi import Request, HTTPException
from .models import EventUpdateDTO, EventPatchDTO
from .router import router


@router.patch("/{_id}", status_code=204)
async def patch_one(request: Request, _id: str, data: EventPatchDTO):
    existing_event = request.app.state.storage.get_one(_id)
    if not existing_event:
        raise HTTPException(status_code=404, detail=f"Event with id {_id} not found")
    updated_data = existing_event.copy(update=data.model_dump(exclude_unset=True))
    request.app.state.storage.set_one(_id, updated_data)
    return