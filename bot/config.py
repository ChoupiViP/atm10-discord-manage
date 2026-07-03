import os

from dotenv import load_dotenv

from bot.config_manager import ConfigManager

load_dotenv()


class Config:
    """Central application configuration."""

    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    AUTHORIZED_ROLE = os.getenv("AUTHORIZED_ROLE", "Admin")

    RCON_HOST = os.getenv("RCON_HOST", "host.docker.internal")
    RCON_PASSWORD = os.getenv("RCON_PASSWORD")
    RCON_PORT = int(os.getenv("RCON_PORT", "25575"))
    RCON_TIMEOUT = int(os.getenv("RCON_TIMEOUT", "5"))
    MC_SAVE_COMMAND = os.getenv("MC_SAVE_COMMAND", "save-all flush")

    @classmethod
    def get_docker_container(cls) -> str:
        """Return the Docker container configured through env or setup."""
        env_container = os.getenv("DOCKER_CONTAINER")
        if env_container:
            return env_container

        persisted_container = ConfigManager.get_docker_container()
        if persisted_container:
            return persisted_container

        raise ValueError(
            "DOCKER_CONTAINER manquant - définissez-le via .env ou utilisez /setup"
        )

    @classmethod
    def is_rcon_enabled(cls) -> bool:
        """Return whether RCON can be used with the current configuration."""
        return bool(cls.RCON_HOST and cls.RCON_PASSWORD and cls.RCON_PORT)


if not Config.DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN manquant")
