from fastapi import Depends, Request, HTTPException

from .router import router
import logging

logger = logging.getLogger(__name__)

@router.delete("/{_id}", status_code=204)
def delete_one(request: Request, _id: str):
    try:
        request.app.state.delete_one(_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Not Found")