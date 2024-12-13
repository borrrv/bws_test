import logging

from fastapi import HTTPException, Request

from .router import router

logger = logging.getLogger(__name__)


@router.delete("/{_id}", status_code=204)
def delete_one(request: Request, _id: str):
    """
    Удалить событие.
    """
    try:
        request.app.state.delete_one(_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Not Found")
