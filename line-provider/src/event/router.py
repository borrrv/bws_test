from fastapi import APIRouter

router = APIRouter(tags=["Events"], prefix="/event")

from .post import *
from .delete import *
from .get import *
from .update import *
