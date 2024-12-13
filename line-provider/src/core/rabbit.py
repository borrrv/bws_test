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

    async def publish_message(
        self,
        message_body: dict,
        exchange_name: str = "bet_exchange",
        routing_key: str = "bet_key",
    ):
        try:
            channel = await self.connection.channel()
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
            channel = await self.connection.channel()
            queue = await channel.declare_queue(queue_name, auto_delete=False)
            logger.info(f"Queue {queue_name} created")
            return queue
        except Exception as e:
            logger.error(f"Error creating queue {queue_name}: {e}")
            raise

    async def create_exchange(self, exchange_name: str):
        try:
            channel = await self.connection.channel()
            exchange = await channel.declare_exchange(
                exchange_name, aio_pika.ExchangeType.TOPIC, durable=True
            )
            logger.info(f"Exchange {exchange_name} created")
            return exchange
        except Exception as e:
            logger.error(f"Error creating exchange {exchange_name}: {e}")
            raise

    async def start(self):
        if not self.connection:
            await self.initialize()

        async with self.connection:
            try:
                exchange_bet = await self.create_exchange("bet_exchange")
                queue_bet = await self.create_queue("bet")
                await queue_bet.bind(exchange_bet, "bet_key")

                while True:
                    await asyncio.sleep(1)

            except Exception as e:
                logger.error(f"Error during RabbitMQ consumption: {e}")

    async def close(self):
        if self.connection:
            try:
                await self.connection.close()
                logger.info("Connection closed")
            except Exception as e:
                logger.error(f"Error closing connection: {e}")
