import logging

import event_pb2
import event_pb2_grpc
import grpc
from src.core.storage import Storage

logger = logging.getLogger(__name__)


class EventService(event_pb2_grpc.EventServiceServicer):
    async def GetEventAll(
        self,
        request: event_pb2.Request,
        context: grpc.aio.ServicerContext,
    ) -> event_pb2.Response:
        storage = Storage()
        events = storage.get_storage
        return storage.get_convert_storage(events, event_pb2)

    async def GetEvent(
        self,
        request: event_pb2.Request,
        context: grpc.aio.ServicerContext,
    ) -> event_pb2.Response:
        storage = Storage()
        valid_events = storage.get_valid_event()
        return storage.get_convert_storage(valid_events, event_pb2)

    async def GetEventById(
        self,
        request: event_pb2.RequestById,
        context: grpc.aio.ServicerContext,
    ) -> event_pb2.Response:
        storage = Storage()
        valid_events = storage.get_one(_id=request.event_id)
        return storage.get_convert_storage(valid_events, event_pb2)

    async def EventCheckTime(
        self,
        request: event_pb2.RequestById,
        context: grpc.aio.ServicerContext,
    ) -> event_pb2.Response:
        storage = Storage()
        check = storage.get_valid_one_event(request.event_id)
        return event_pb2.ResponseCheck(check=check)


async def serve() -> None:
    server = grpc.aio.server()
    event_pb2_grpc.add_EventServiceServicer_to_server(EventService(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()
