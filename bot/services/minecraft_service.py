from typing import Any

from bot.logger import logger
from bot.services.docker_service import DockerService
from bot.services.rcon_service import RconService


class MinecraftService:
    """Service principal de gestion du serveur Minecraft."""

    def __init__(
        self,
        docker_service: DockerService | None = None,
        rcon_service: RconService | None = None,
    ):
        self.docker = docker_service or DockerService()
        self.rcon = rcon_service or RconService()

    # --------------------------------------------------
    # Docker
    # --------------------------------------------------

    def status(self) -> dict[str, Any]:
        """Retourne l'état du serveur."""
        info = self.docker.get_status()
        info.update(self._player_status())
        return info

    def get_status(self) -> dict[str, Any]:
        return self.status()

    def start(self):
        self.docker.start_container()

    def stop(self):
        self.docker.stop_container()

    def restart(self):
        self.docker.restart_container()

    # --------------------------------------------------
    # RCON
    # --------------------------------------------------

    def command(self, command: str):
        return self.rcon.command(command)

    def list_players(self):
        return self.rcon.list_players()

    def say(self, message: str):
        return self.rcon.say(message)

    def save_all(self):
        return self.rcon.save_all()

    def save_off(self):
        return self.rcon.save_off()

    def save_on(self):
        return self.rcon.save_on()

    def stop_server(self):
        return self.rcon.stop()

    # --------------------------------------------------
    # Dashboard
    # --------------------------------------------------

    def _player_status(self) -> dict[str, Any]:
        """
        Récupère les informations sur les joueurs connectés.
        """

        try:

            response = self.rcon.list_players()

            return {
                "players_summary": response,
                "rcon_success": True
            }

        except Exception as exc:

            logger.warning(
                f"Impossible de récupérer les joueurs : {exc}"
            )

            return {
                "players_summary": "RCON indisponible",
                "rcon_success": False,
                "rcon_error": str(exc)
            }