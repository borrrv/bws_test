from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = getenv("DEBUG")
    LOCAL = getenv("LOCAL")

    POSTGRES_USER = getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
    DB_HOST = getenv("DB_HOST")
    POSTGRES_DB = getenv("POSTGRES_DB")
    DB_PORT = getenv("DB_PORT")
    SQLALCHEMY_DATABASE_URI = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}/{POSTGRES_DB}"

    LINE_SERVICE = getenv("LINE_SERVICE")
    PORT_GRPC = getenv("PORT_GRPC")

    RABBITMQ_USER = getenv("RABBIT_MQ_USER")
    RABBIT_MQ_PASSWORD = getenv("RABBIT_MQ_PASSWORD")
    RABBIT_MQ_URL = getenv("RABBIT_MQ_URL")
