from fastapi import APIRouter

router = APIRouter(tags=["Bet.Events"], prefix="/events")


from .get import *  # noqa F401
