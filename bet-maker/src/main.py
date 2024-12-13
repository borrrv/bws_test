import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.bet.database import Bet
from src.bet.router import router as bet_router
from src.core.config import Config
from src.core.database import create_db_and_tables, insert_bets
from src.core.logging import init_logger
from src.core.rabbit import RabbitMQ
from src.events.router import router as event_router
from starlette.middleware.cors import CORSMiddleware

origins = ["*"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_logger()
    rabbitmq = RabbitMQ()
    await rabbitmq.initialize()
    asyncio.create_task(rabbitmq.start())
    app.state.rabbitmq = rabbitmq
    await create_db_and_tables([Bet])
    await insert_bets(Bet)
    logger = logging.getLogger("START")
    logger.warning("===== Starting bet-maker =====")
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
app.include_router(bet_router, prefix="/api")
