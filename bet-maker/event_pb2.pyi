from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class Request(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RequestById(_message.Message):
    __slots__ = ("event_id",)
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    def __init__(self, event_id: _Optional[str] = ...) -> None: ...

class Event(_message.Message):
    __slots__ = ("event_id", "coefficient", "deadline", "state")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    COEFFICIENT_FIELD_NUMBER: _ClassVar[int]
    DEADLINE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    coefficient: str
    deadline: str
    state: str
    def __init__(
        self,
        event_id: _Optional[str] = ...,
        coefficient: _Optional[str] = ...,
        deadline: _Optional[str] = ...,
        state: _Optional[str] = ...,
    ) -> None: ...

class Response(_message.Message):
    __slots__ = ("events",)
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[Event]
    def __init__(
        self, events: _Optional[_Iterable[_Union[Event, _Mapping]]] = ...
    ) -> None: ...

class ResponseCheck(_message.Message):
    __slots__ = ("check",)
    CHECK_FIELD_NUMBER: _ClassVar[int]
    check: bool
    def __init__(self, check: bool = ...) -> None: ...
