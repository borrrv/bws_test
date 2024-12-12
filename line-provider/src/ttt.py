# import asyncio
#
# from pydantic import BaseModel
# from enum import Enum
# import time
# from pydantic import BaseModel
# import decimal
#
# class EventState(Enum):
#     NEW = 1
#     FINISHED_WIN = 2
#     FINISHED_LOSE = 3
#
#
# class Event(BaseModel):
#     event_id: str
#     coefficient: decimal.Decimal | None = None
#     deadline: int | None = None
#     state: EventState | None = None
#
#
# class Storage:
#     def __init__(self):
#         self.storage: dict[str, BaseModel] = {}
#
#     def get_one(self, _id: str) -> BaseModel:
#         return self.storage.get(_id)
#
#     def set_one(self, _id: str, data: BaseModel) -> None:
#         self.storage[_id] = data
#
#     def add_one(self, data: BaseModel) -> None:
#         self.storage[data.event_id] = data
#
#     def delete_one(self, _id: str) -> None:
#         if _id in self.storage:
#             del self.storage[_id]
#
#     def get_storage(self):
#         return self.storage
#
# def main():
#
#     storage = Storage()
#     storage.add_one(Event(event_id='1', coefficient=1.2, deadline=int(time.time()) + 600, state=EventState.NEW))
#     storage.add_one(Event(event_id='2', coefficient=1.15, deadline=int(time.time()) + 60, state=EventState.NEW))
#     storage.add_one(Event(event_id='3', coefficient=1.67, deadline=int(time.time()) + 90, state=EventState.NEW))
#     print(storage.get_storage())
#     print(storage.get_one("1"))
#
# if __name__ == '__main__':
#     main()

import time
a = time.time()
print(a)
print(a + 60)