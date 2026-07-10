import copy
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
            "channel_id": None,
            "message_id": None,
            "guild_id": None
        },
        "logs": {
            "channel_id": None
        },
        "notifications": {
            "channel_id": None
        }
    }

    _config_cache: dict | None = None

    @classmethod
    def _merge_defaults(cls, config: dict) -> dict:
        """Ajoute automatiquement les clés manquantes."""

        merged = copy.deepcopy(cls.DEFAULT_CONFIG)

        for section, values in config.items():

            if isinstance(values, dict) and section in merged:

                merged[section].update(values)

            else:

                merged[section] = values

        return merged

    @classmethod
    def load(cls) -> dict:

        if cls._config_cache is not None:
            return copy.deepcopy(cls._config_cache)

        if not cls.CONFIG_FILE.exists():
            config = copy.deepcopy(cls.DEFAULT_CONFIG)
            cls.save(config)
            return copy.deepcopy(config)

        try:
            with open(cls.CONFIG_FILE, "r", encoding="utf-8") as file:
                content = file.read()

            if not content.strip():
                raise ValueError("Fichier de configuration vide")

            loaded_config = json.loads(content)
            config = cls._merge_defaults(loaded_config)

            if config != loaded_config:
                cls.save(config)
            else:
                cls._config_cache = copy.deepcopy(config)

            return copy.deepcopy(config)

        except Exception as e:
            logger.exception(e)
            if cls.CONFIG_FILE.exists():
                try:
                    cls.CONFIG_FILE.unlink()
                except Exception:
                    logger.warning("Impossible de supprimer le fichier de configuration corrompu")

            config = copy.deepcopy(cls.DEFAULT_CONFIG)
            cls.save(config)
            return copy.deepcopy(config)

    @classmethod
    def save(cls, config: dict):

        cls.CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

        with open(cls.CONFIG_FILE, "w", encoding="utf-8") as file:
            json.dump(config, file, indent=4)

        cls._config_cache = copy.deepcopy(config)

    @classmethod
    def get(cls):
        return cls.load()

    @classmethod
    def reset(cls):
        cls.save(copy.deepcopy(cls.DEFAULT_CONFIG))
        cls._config_cache = copy.deepcopy(cls.DEFAULT_CONFIG)

    # --------------------------------------------------
    # Docker
    # --------------------------------------------------

    @classmethod
    def set_container(cls, container: str):

        config = cls.load()

        config["docker"]["container"] = container

        cls.save(config)

    @classmethod
    def get_container(cls):

        return cls.load()["docker"]["container"]

    # --------------------------------------------------
    # RCON
    # --------------------------------------------------

    @classmethod
    def set_rcon(cls, host: str, port: int, password: str):

        config = cls.load()

        config["rcon"]["host"] = host
        config["rcon"]["port"] = port
        config["rcon"]["password"] = password

        cls.save(config)

    @classmethod
    def get_rcon(cls):

        return cls.load()["rcon"]

    # --------------------------------------------------
    # Dashboard
    # --------------------------------------------------

    @classmethod
    def set_dashboard_channel(cls, channel_id: int):

        config = cls.load()

        config["dashboard"]["channel_id"] = channel_id

        cls.save(config)

    @classmethod
    def get_dashboard_channel(cls):

        return cls.load()["dashboard"]["channel_id"]

    @classmethod
    def set_dashboard_message(cls, guild_id: int, channel_id: int, message_id: int):

        config = cls.load()

        config["dashboard"]["guild_id"] = guild_id
        config["dashboard"]["channel_id"] = channel_id
        config["dashboard"]["message_id"] = message_id

        cls.save(config)

    @classmethod
    def get_dashboard(cls):

        return cls.load()["dashboard"]

    # --------------------------------------------------
    # Logs
    # --------------------------------------------------

    @classmethod
    def set_logs_channel(cls, channel_id: int):

        config = cls.load()

        config["logs"]["channel_id"] = channel_id

        cls.save(config)

    @classmethod
    def get_logs_channel(cls):

        return cls.load()["logs"]["channel_id"]

    # --------------------------------------------------
    # Notifications
    # --------------------------------------------------

    @classmethod
    def set_notifications_channel(cls, channel_id: int):

        config = cls.load()

        config["notifications"]["channel_id"] = channel_id

        cls.save(config)

    @classmethod
    def get_notifications_channel(cls):

        return cls.load()["notifications"]["channel_id"]