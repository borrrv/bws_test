from pydantic import BaseModel
from src.core.database import AbstractBase

__all__ = ("AbstractTable", "AbstractResponseModel")


class AbstractTable:
    table: AbstractBase


class AbstractResponseModel:
    response_model: BaseModel
