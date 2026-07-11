import random
import re
from typing import Any

from bot.services.config_service import ConfigService


class LinkService:
    """Service de liaison Discord <-> Minecraft."""

    CODE_PATTERN = re.compile(r"\bAT10-\d{5}\b")
    _pending_codes: dict[str, int] = {}

    @classmethod
    def generate_link_code(cls, discord_id: int) -> str:
        while True:
            code = f"AT10-{random.randint(10000, 99999)}"
            if code not in cls._pending_codes:
                cls._pending_codes[code] = discord_id
                return code

    @classmethod
    def consume_link_code(cls, code: str) -> int | None:
        return cls._pending_codes.pop(code, None)

    @classmethod
    def find_code_in_message(cls, message: str) -> str | None:
        match = cls.CODE_PATTERN.search(message)
        return match.group(0) if match else None

    @classmethod
    def set_link(cls, discord_id: int, minecraft_name: str) -> None:
        config = ConfigService.load()

        if "links" not in config:
            config["links"] = {}

        # remove any existing minecraft_name linked to another discord id
        for stored_discord_id, stored_minecraft in list(config["links"].items()):
            if stored_minecraft.lower() == minecraft_name.lower() and int(stored_discord_id) != discord_id:
                del config["links"][stored_discord_id]

        config["links"][str(discord_id)] = minecraft_name
        ConfigService.save(config)

    @classmethod
    def remove_link(cls, discord_id: int) -> None:
        config = ConfigService.load()
        if "links" not in config:
            return

        config["links"].pop(str(discord_id), None)
        ConfigService.save(config)

    @classmethod
    def get_minecraft_name(cls, discord_id: int) -> str | None:
        config = ConfigService.load()
        return config.get("links", {}).get(str(discord_id))

    @classmethod
    def get_discord_id(cls, minecraft_name: str) -> int | None:
        config = ConfigService.load()
        for stored_discord_id, stored_minecraft in config.get("links", {}).items():
            if stored_minecraft.lower() == minecraft_name.lower():
                try:
                    return int(stored_discord_id)
                except ValueError:
                    continue
        return None

    @classmethod
    def get_all_links(cls) -> dict[int, str]:
        config = ConfigService.load()
        return {int(k): v for k, v in config.get("links", {}).items() if k.isdigit()}
