import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.core.config import Config
from src.core.logging import init_logger
from src.core.rabbit import RabbitMQ
from src.core.storage import Storage
from src.event.router import router as event_router
from src.grpc_event import grpc_server

origins = ["*"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_logger()
    app.state.storage = Storage()
    asyncio.create_task(grpc_server.serve())
    rabbitmq = RabbitMQ()
    app.state.rabbitmq = rabbitmq
    asyncio.create_task(rabbitmq.start())
    logger = logging.getLogger("START")
    logger.warning("===== Starting line-provider =====")
    yield
    await app.state.rabbitmq.close()


app = FastAPI(lifespan=lifespan, debug=Config.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(event_router, prefix="/api")
