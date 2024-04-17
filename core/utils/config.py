import os
from typing import List
from dataclasses import dataclass
import dotenv

dotenv.load_dotenv()

@dataclass
class Config:
    BOT_TOKEN: str
    ADMINS_IDS: List[int]

def get_config() -> Config:
    return Config(
        BOT_TOKEN=os.getenv("BOT_TOKEN"),
        ADMINS_IDS=list(map(int, os.getenv("ADMINS_IDS").split(',')))
    )

config = get_config()