from typing import Any

from bot.logger import logger
from bot.services.docker_service import DockerService
from bot.services.rcon_service import PlayerList, RconService


class MinecraftService:
    """Application service for Minecraft server operations."""

    def __init__(
        self,
        docker_service: DockerService | None = None,
        rcon_service: RconService | None = None,
    ) -> None:
        self.docker = docker_service or DockerService()
        self.rcon = rcon_service or RconService()

    def status(self) -> dict[str, Any]:
        """Return the current Minecraft server status."""
        info = self.docker.get_status()
        info.update(self._player_status())
        return info

    def get_status(self) -> dict[str, Any]:
        """Backward-compatible alias used by existing cogs."""
        return self.status()

    def start(self) -> None:
        """Start the Minecraft server container."""
        self.docker.start_container()

    def stop(self) -> None:
        """Stop the Minecraft server container."""
        self.docker.stop_container()

    def restart(self) -> None:
        """Restart the Minecraft server container."""
        self.docker.restart_container()

    def command(self, command: str) -> str:
        """Run a Minecraft command through RCON."""
        return self.rcon.command(command)

    def list_players(self) -> PlayerList:
        """Return online players through RCON."""
        return self.rcon.list_players()

    def save_world(self) -> str:
        """Save the Minecraft world through RCON."""
        return self.rcon.save_world()

    def _player_status(self) -> dict[str, Any]:
        if not self.rcon.is_configured():
            return {
                "players_online": 0,
                "players_max": 0,
                "players": [],
                "players_summary": "RCON non configuré",
                "rcon_success": False,
            }

        try:
            players = self.rcon.list_players()
        except Exception as exc:
            logger.warning("Impossible de récupérer les joueurs via RCON: %s", exc)
            return {
                "players_online": 0,
                "players_max": 0,
                "players": [],
                "players_summary": "RCON indisponible",
                "rcon_success": False,
                "rcon_error": str(exc),
            }

        return {
            "players_online": players.online,
            "players_max": players.maximum,
            "players": players.names,
            "players_summary": players.summary,
            "rcon_success": True,
        }
