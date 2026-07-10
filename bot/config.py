import os

from dotenv import load_dotenv

from bot.services.config_service import ConfigService

load_dotenv()


class Config:
    """Central application configuration."""

    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    AUTHORIZED_ROLE = os.getenv("AUTHORIZED_ROLE", "Admin")

    @classmethod
    def get_docker_container(cls) -> str:
        """Return the Docker container configured through env or setup."""
        env_container = os.getenv("DOCKER_CONTAINER")
        if env_container:
            return env_container

        persisted_container = ConfigService.get_docker_container()
        if persisted_container:
            return persisted_container

        raise ValueError(
            "DOCKER_CONTAINER manquant - définissez-le via .env ou utilisez /setup"
        )



if not Config.DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN manquant")
