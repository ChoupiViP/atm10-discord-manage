import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

    if DISCORD_TOKEN is None:
        raise ValueError("DISCORD_TOKEN est introuvable dans le fichier .env")