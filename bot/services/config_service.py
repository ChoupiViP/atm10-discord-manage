import json
from pathlib import Path

from bot.logger import logger


class ConfigService:
    """Gestion de la configuration du bot."""

    CONFIG_FILE = Path("data/config.json")

    DEFAULT_CONFIG = {
        "docker": {
            "container": None
        },
        "rcon": {
            "host": "",
            "port": 25575,
            "password": ""
        },
        "dashboard": {
            "channel_id": None
        },
        "logs": {
            "channel_id": None
        },
        "notifications": {
            "channel_id": None
        }
    }

    @classmethod
    def load(cls) -> dict:
        """Charge la configuration."""

        if not cls.CONFIG_FILE.exists():
            cls.save(cls.DEFAULT_CONFIG.copy())

        try:
            with open(cls.CONFIG_FILE, "r", encoding="utf-8") as file:
                return json.load(file)

        except Exception as e:
            logger.exception(e)
            return cls.DEFAULT_CONFIG.copy()

    @classmethod
    def save(cls, config: dict):
        """Sauvegarde la configuration."""

        cls.CONFIG_FILE.parent.mkdir(exist_ok=True)

        with open(cls.CONFIG_FILE, "w", encoding="utf-8") as file:
            json.dump(config, file, indent=4)

    @classmethod
    def get(cls):

        return cls.load()

    @classmethod
    def reset(cls):

        cls.save(cls.DEFAULT_CONFIG.copy())

    # -------------------------
    # Docker
    # -------------------------

    @classmethod
    def set_container(cls, container: str):

        config = cls.load()

        config["docker"]["container"] = container

        cls.save(config)

    @classmethod
    def get_container(cls):

        return cls.load()["docker"]["container"]

    # -------------------------
    # RCON
    # -------------------------

    @classmethod
    def set_rcon(
        cls,
        host: str,
        port: int,
        password: str
    ):

        config = cls.load()

        config["rcon"]["host"] = host
        config["rcon"]["port"] = port
        config["rcon"]["password"] = password

        cls.save(config)

    @classmethod
    def get_rcon(cls):

        return cls.load()["rcon"]

    # -------------------------
    # Dashboard
    # -------------------------

    @classmethod
    def set_dashboard_channel(
        cls,
        channel_id: int
    ):

        config = cls.load()

        config["dashboard"]["channel_id"] = channel_id

        cls.save(config)

    @classmethod
    def get_dashboard_channel(cls):

        return cls.load()["dashboard"]["channel_id"]

    # -------------------------
    # Logs
    # -------------------------

    @classmethod
    def set_logs_channel(
        cls,
        channel_id: int
    ):

        config = cls.load()

        config["logs"]["channel_id"] = channel_id

        cls.save(config)

    @classmethod
    def get_logs_channel(cls):

        return cls.load()["logs"]["channel_id"]

    # -------------------------
    # Notifications
    # -------------------------

    @classmethod
    def set_notifications_channel(
        cls,
        channel_id: int
    ):

        config = cls.load()

        config["notifications"]["channel_id"] = channel_id

        cls.save(config)

    @classmethod
    def get_notifications_channel(cls):

        return cls.load()["notifications"]["channel_id"]