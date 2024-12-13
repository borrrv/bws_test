import logging

import event_pb2
import event_pb2_grpc
import grpc
from src.core.config import Config
from src.events.models import convert_events

logger = logging.getLogger(__name__)


async def get_event_all():
    async with grpc.aio.insecure_channel(
        f"{Config.LINE_SERVICE}:{Config.PORT_GRPC}"
    ) as channel:
        stub = event_pb2_grpc.EventServiceStub(channel)
        response: event_pb2.Response = await stub.GetEventAll(event_pb2.Request())
    result = convert_events(response)
    return result


async def get_event():
    async with grpc.aio.insecure_channel(
        f"{Config.LINE_SERVICE}:{Config.PORT_GRPC}"
    ) as channel:
        stub = event_pb2_grpc.EventServiceStub(channel)
        response: event_pb2.Response = await stub.GetEvent(event_pb2.Request())
    result = convert_events(response)
    return result


async def get_event_by_id(_id):
    async with grpc.aio.insecure_channel(
        f"{Config.LINE_SERVICE}:{Config.PORT_GRPC}"
    ) as channel:
        stub = event_pb2_grpc.EventServiceStub(channel)
        response: event_pb2.Response = await stub.GetEventById(
            event_pb2.RequestById(event_id=_id)
        )
    result = convert_events(response)
    return result


async def event_check_time(_id) -> bool:
    async with grpc.aio.insecure_channel(
        f"{Config.LINE_SERVICE}:{Config.PORT_GRPC}"
    ) as channel:
        stub = event_pb2_grpc.EventServiceStub(channel)
        response: event_pb2.Response = await stub.EventCheckTime(
            event_pb2.RequestById(event_id=_id)
        )
    return response.check
