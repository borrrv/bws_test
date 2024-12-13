from decimal import Decimal
from logging import getLogger
from time import time

import event_pb2
from pydantic import BaseModel
from src.core.singleton import singleton

logger = getLogger(__name__)


@singleton
class Storage:

    def __init__(self):
        self.__storage: dict[str, BaseModel] = {}

    def get_one(self, _id: str) -> BaseModel:
        return self.__storage.get(_id)

    def set_one(self, _id: str, data: BaseModel) -> None:
        self.__storage[_id] = data
        logger.warning(f"Update competed for {_id}")

    def add_one(self, data: BaseModel) -> BaseModel:
        if data.event_id in self.__storage:
            logger.error(f"Duplicate event ID: {data.event_id}")
            raise ValueError("Duplicate event ID")
        current_time = Decimal(time())
        data.deadline += current_time
        self.__storage[data.event_id] = data
        logger.warning(f"Add completed for event ID: {data.event_id}")
        return data

    def delete_one(self, _id: str) -> None:
        if _id in self.__storage:
            del self.__storage[_id]
            logger.warning(f"Delete competed for {_id}")
        else:
            logger.error(f"Event with id {_id} not found")
            raise ValueError(f"Event with id {_id} not found")

    @property
    def get_storage(self) -> dict[str, BaseModel]:
        return self.__storage

    def get_convert_storage(
        self, events: dict[str, BaseModel], event_pb: event_pb2
    ) -> event_pb2.Response:
        if events is None:
            return event_pb2.Response(events=events)
        try:
            events = [
                event_pb.Event(
                    event_id=event.event_id,
                    coefficient=str(event.coefficient),
                    deadline=str(event.deadline),
                    state=event.state.name,
                )
                for key, event in events.items()
            ]
        except AttributeError:
            events = [
                event_pb.Event(
                    event_id=events.event_id,
                    coefficient=str(events.coefficient),
                    deadline=str(events.deadline),
                    state=events.state.name,
                )
            ]

        return event_pb.Response(events=events)

    def get_valid_event(self) -> dict[str, BaseModel]:
        result = {}
        for key in self.__storage:
            if time() < self.__storage[key].deadline:
                result[key] = self.__storage[key]
            continue
        return result

    def get_valid_one_event(self, _id: str) -> bool:
        if self.__storage[_id].deadline > time():
            return True
        return False
