from fastapi import APIRouter

router = APIRouter(tags=["Bets"], prefix="/bets")


from .get import *  # noqa F401
from .post import *  # noqa F401
