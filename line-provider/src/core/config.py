from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = getenv("DEBUG")
    LOCAL = getenv("LOCAL")
