from fastapi import APIRouter

router = APIRouter(tags=["Events"], prefix="/event")

from .delete import *  # noqa F401
from .get import *  # noqa F401
from .post import *  # noqa F401
from .update import *  # noqa F401
