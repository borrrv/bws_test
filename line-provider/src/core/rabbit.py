import asyncio
import logging

import aio_pika
import orjson

from .config import Config
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
            except aio_pika.exceptions.AMQPConnectionError as e:
                logger.error(
                    f"Attempt {attempt}/{self.__max_retries}: Error initializing connection: {e}"
                )
                if attempt < self.__max_retries:
                    await asyncio.sleep(self.__retry_delay)
                else:
                    logger.error("All retry attempts failed")
                    raise

    async def publish_message(
        self,
        message_body: dict,
        exchange_name: str = "bet_exchange",
        routing_key: str = "bet_key",
    ):
        try:
            channel = await self.__connection.channel()
            exchange = await channel.declare_exchange(
                exchange_name, aio_pika.ExchangeType.TOPIC, durable=True
            )
            message = aio_pika.Message(
                body=orjson.dumps(message_body),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            )
            await exchange.publish(message, routing_key=routing_key)
            logger.info(
                f"Message published to exchange {exchange_name} with routing key {routing_key}"
            )
        except Exception as e:
            logger.error(f"Error publishing message: {e}")

    async def create_queue(self, queue_name: str):
        try:
            channel = await self.__connection.channel()
            queue = await channel.declare_queue(queue_name, auto_delete=False)
            logger.info(f"Queue {queue_name} created")
            return queue
        except Exception as e:
            logger.error(f"Error creating queue {queue_name}: {e}")
            raise

    async def create_exchange(self, exchange_name: str):
        try:
            channel = await self.__connection.channel()
            exchange = await channel.declare_exchange(
                exchange_name, aio_pika.ExchangeType.TOPIC, durable=True
            )
            logger.info(f"Exchange {exchange_name} created")
            return exchange
        except Exception as e:
            logger.error(f"Error creating exchange {exchange_name}: {e}")
            raise

    async def start(self):
        if not self.__connection:
            await self.initialize()

        async with self.__connection:
            try:
                exchange_bet = await self.create_exchange("bet_exchange")
                queue_bet = await self.create_queue("bet")
                await queue_bet.bind(exchange_bet, "bet_key")

                while True:
                    await asyncio.sleep(1)

            except Exception as e:
                logger.error(f"Error during RabbitMQ consumption: {e}")

    async def close(self):
        if self.__connection:
            try:
                await self.__connection.close()
                logger.info("Connection closed")
            except Exception as e:
                logger.error(f"Error closing connection: {e}")
