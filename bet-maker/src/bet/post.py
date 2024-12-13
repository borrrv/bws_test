from fastapi import Depends, HTTPException, Request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session

from .models import CreateOneDTO, GetOneDTO
from .router import router
from .service import BetCreateService


@router.post("/", response_model=GetOneDTO, status_code=201)
async def create_one(
    request: Request, params: CreateOneDTO, session: AsyncSession = Depends(get_session)
) -> GetOneDTO:
    """
    Совершает ставку на событие.
        Проверяет на наличие события и попадание в дедлайны.
    """
    try:

        result = await BetCreateService.create_one(session=session, params=params)
    except IntegrityError as e:
        raise HTTPException(404, detail=str(e))
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    return result
