import asyncio
import logging

import aio_pika
import orjson
from src.bet.service import BetUpdateService

from .config import Config
from .database import async_session
from .singleton import singleton

logger = logging.getLogger(__name__)


@singleton
class RabbitMQ:

    def __init__(self):
        self.user = Config.RABBITMQ_USER
        self.password = Config.RABBIT_MQ_PASSWORD
        self.url = Config.RABBIT_MQ_URL
        self.connection = None

    async def initialize(self):
        try:
            self.connection = await aio_pika.connect_robust(
                f"amqp://{self.user}:{self.password}@{self.url}"
            )
            logger.info("Initialize RabbitMQ complete")
        except Exception as e:
            logger.error(f"Error initializing connection: {e}")
            raise

    async def create_queue(self, queue_name: str):
        channel = await self.connection.channel()
        queue = await channel.declare_queue(queue_name, auto_delete=False)
        logger.info(f"Queue {queue_name} created")
        return queue

    async def on_message(self, message: aio_pika.IncomingMessage):
        async with message.process():
            try:
                body = message.body.decode()
                data = orjson.loads(body)
                logger.info(f"Received message: {data}")

                await self.process_message(data)

            except Exception as e:
                logger.error(f"Error processing message: {e}")

    async def process_message(self, data: dict):
        logger.info(f"Processing message: {data}")
        async with async_session() as session:
            await BetUpdateService.update(session, data)
        # Пример: Обработка данных
        # Например, сохраняем данные в БД, запускаем процесс и т.д.

    async def start(self):
        if not self.connection:
            await self.initialize()

        async with self.connection:
            try:
                await self.connection.channel()
                queue = await self.create_queue("bet")
                await queue.consume(self.on_message)

                logger.info("Waiting for messages...")
                while True:
                    await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Error during RabbitMQ consumer: {e}")

    async def close(self):
        if self.connection:
            try:
                await self.connection.close()
                logger.info("RabbitMQ connection closed")
            except Exception as e:
                logger.error(f"Error closing RabbitMQ connection: {e}")
