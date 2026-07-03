import re
from dataclasses import dataclass

from mcrcon import MCRcon

from bot.config import Config
from bot.logger import logger


@dataclass(slots=True)
class PlayerList:
    """Parsed Minecraft player list returned by the RCON list command."""

    online: int
    maximum: int
    names: list[str]
    raw: str

    @property
    def summary(self) -> str:
        """Return a compact player count for embeds."""
        return f"{self.online} / {self.maximum}"


class RconService:
    """Minecraft RCON client wrapper."""

    LIST_PATTERN = re.compile(
        r"There are (?P<online>\d+) of a max of (?P<maximum>\d+) players online",
        re.IGNORECASE,
    )

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        password: str | None = None,
        timeout: int | None = None,
    ) -> None:
        self.host = host or Config.RCON_HOST
        self.port = port or Config.RCON_PORT
        self.password = password or Config.RCON_PASSWORD
        self.timeout = timeout or Config.RCON_TIMEOUT

    def is_configured(self) -> bool:
        """Return whether RCON credentials are configured."""
        return bool(self.host and self.port and self.password)

    def command(self, command: str) -> str:
        """Run a raw Minecraft command through RCON."""
        if not self.is_configured():
            raise ValueError("RCON non configuré")

        safe_command = command.strip().lstrip("/")
        if not safe_command:
            raise ValueError("Commande Minecraft vide")

        logger.info("Commande RCON exécutée: %s", safe_command)
        with MCRcon(
            self.host,
            self.password,
            port=self.port,
            timeout=self.timeout,
        ) as client:
            return client.command(safe_command)

    def list_players(self) -> PlayerList:
        """Return the current Minecraft player list."""
        response = self.command("list")
        match = self.LIST_PATTERN.search(response)

        online = int(match.group("online")) if match else 0
        maximum = int(match.group("maximum")) if match else 0
        names = self._parse_names(response)

        return PlayerList(
            online=online,
            maximum=maximum,
            names=names,
            raw=response,
        )

    def save_world(self) -> str:
        """Ask Minecraft to flush the world to disk."""
        return self.command(Config.MC_SAVE_COMMAND)

    @staticmethod
    def _parse_names(response: str) -> list[str]:
        if ":" not in response:
            return []

        names_part = response.split(":", 1)[1].strip()
        if not names_part:
            return []

        return [name.strip() for name in names_part.split(",") if name.strip()]
