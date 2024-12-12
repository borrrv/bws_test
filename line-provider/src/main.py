import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.core.config import Config
from src.core.logging import init_logger
from src.core.storage import Storage
from src.core.test_values import add_values
from src.event.router import router as event_router

origins = ["*"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_logger()
    app.state.storage = Storage()
    add_values()
    logger = logging.getLogger("START")
    logger.warning("===== Starting line-provider =====")
    yield


app = FastAPI(lifespan=lifespan, debug=Config.DEBUG)

app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

app.include_router(event_router, prefix="/api")
