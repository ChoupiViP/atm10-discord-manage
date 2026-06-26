import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    DOCKER_CONTAINER = os.getenv("DOCKER_CONTAINER")

    if not DISCORD_TOKEN:
        raise ValueError("DISCORD_TOKEN manquant")

    if not DOCKER_CONTAINER:
        raise ValueError("DOCKER_CONTAINER manquant")