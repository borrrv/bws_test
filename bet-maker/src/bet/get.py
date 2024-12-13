from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_session

from .models import GetOneDTO
from .router import router
from .service import BetGetListService


@router.get("/", response_model=list[GetOneDTO], status_code=200)
async def get_list(
    request: Request, session: AsyncSession = Depends(get_session)
) -> GetOneDTO:
    return await BetGetListService.get_list(session=session)
