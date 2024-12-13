from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = getenv("DEBUG")
    LOCAL = getenv("LOCAL")

    RABBITMQ_USER = getenv("RABBIT_MQ_USER")
    RABBIT_MQ_PASSWORD = getenv("RABBIT_MQ_PASSWORD")
    RABBIT_MQ_URL = getenv("RABBIT_MQ_URL")
