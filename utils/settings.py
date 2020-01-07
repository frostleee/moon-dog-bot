import os
from dotenv import load_dotenv

load_dotenv()


def get(name: str, default=None) -> object:
    name = name.upper()
    if name in os.environ:
        return os.getenv(name)
    else:
        return default
