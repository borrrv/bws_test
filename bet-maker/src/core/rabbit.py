import asyncio
import logging

import aio_pika
import orjson
from aio_pika.exceptions import AMQPConnectionError

from src.bet.service import BetUpdateService

from .config import Config
from .database import async_session
from .singleton import singleton

logger = logging.getLogger(__name__)


@singleton
class RabbitMQ:

    def __init__(self):
        self.__user = Config.RABBITMQ_USER
        self.__password = Config.RABBIT_MQ_PASSWORD
        self.__url = Config.RABBIT_MQ_URL
        self.__connection = None
        self.__max_retries = 5
        self.__retry_delay = 15

    async def initialize(self):
        for attempt in range(1, self.__max_retries + 1):
            try:
                self.__connection = await aio_pika.connect_robust(
                    f"amqp://{self.__user}:{self.__password}@{self.__url}"
                )
                logger.info("Initialize RabbitMQ complete")
                return
            except AMQPConnectionError as e:
                logger.error(
                    f"Attempt {attempt}/{self.__max_retries}: Error initializing connection: {e}"
                )
                if attempt < self.__max_retries:
                    await asyncio.sleep(self.__retry_delay)
                else:
                    logger.error("All retry attempts failed")
                    raise

    async def create_queue(self, queue_name: str):
        channel = await self.__connection.channel()
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
        if not self.__connection:
            await self.initialize()

        async with self.__connection:
            try:
                await self.__connection.channel()
                queue = await self.create_queue("bet")
                await queue.consume(self.on_message)

                logger.info("Waiting for messages...")
                while True:
                    await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Error during RabbitMQ consumer: {e}")

    async def close(self):
        if self.__connection:
            try:
                await self.__connection.close()
                logger.info("RabbitMQ connection closed")
            except Exception as e:
                logger.error(f"Error closing RabbitMQ connection: {e}")
