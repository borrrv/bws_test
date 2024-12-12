from pydantic import BaseModel
from src.core.singleton import singleton
from logging import getLogger
from time import time
from decimal import Decimal

logger = getLogger(__name__)

@singleton
class Storage:

    def __init__(self):
        self.storage: dict[str, BaseModel] = {}

    def get_one(self, _id: str) -> BaseModel:
        return self.storage.get(_id)

    def set_one(self, _id: str, data: BaseModel) -> None:
        self.storage[_id] = data
        logger.warning(f"Update competed for {_id}")

    def add_one(self, data: BaseModel) -> None:
        if data.event_id not in self.storage:
            data.deadline += Decimal(time())
            self.storage[data.event_id] = data
            logger.warning(f"Add competed for {data.event_id}")
            return self.storage[data.event_id]
        else:
            logger.error('Duplicate event id')
            raise ValueError('Duplicate event id')

    def delete_one(self, _id: str) -> None:
        if _id in self.storage:
            del self.storage[_id]
            logger.warning(f"Delete competed for {_id}")
            return True
        else:
            logger.error(f"Event with id {_id} not found")
            raise ValueError(f"Event with id {_id} not found")

    def get_storage(self):
        return self.storage
