import re
from typing import Any

from bot.logger import logger
from bot.services.docker_service import DockerService
from bot.services.rcon_service import RconService


class MinecraftService:
    """Service principal de gestion du serveur Minecraft."""

    _PLAYERS_PATTERN = re.compile(
        r"There are (\d+) of a maximum of (\d+) players",
        re.IGNORECASE,
    )
    _PLAYERS_SHORT_PATTERN = re.compile(
        r"There are (\d+) of a max(?:imum)? of (\d+) players",
        re.IGNORECASE,
    )
    _PLAYERS_FALLBACK_PATTERN = re.compile(
        r"(\d+)\s*/\s*(\d+)\s*(?:players|slots)?",
        re.IGNORECASE,
    )
    _PLAYER_LIST_PATTERN = re.compile(r"There are \d+ of a maximum of \d+ players(?: online:)?\s*(.*)$", re.IGNORECASE)
    _PLAYER_NAME_PATTERN = re.compile(r"\b{player}\b")
    _TPS_MULTI_PATTERN = re.compile(
        r"(?:from last.*?:|last.*?:)\s*(\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?)",
        re.IGNORECASE,
    )
    _TPS_OVERALL_PATTERN = re.compile(
        r"Overall:\s*(\d+(?:\.\d+)?)\s*TPS",
        re.IGNORECASE,
    )
    _TPS_SINGLE_PATTERN = re.compile(r"(\d+(?:\.\d+)?)")

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

    def player_info(self, player: str) -> dict[str, str]:
        """Récupère les informations principales d'un joueur Minecraft."""
        online_players = self.online_players()
        online = player in online_players
        position = self._get_player_data(player, "Pos")
        dimension = self._get_player_data(player, "Dimension")
        playtime = self._get_player_data(player, "Stats.minecraft.custom.minecraft.play_time")
        ping = self._get_player_data(player, "Ping")

        if playtime is not None:
            playtime = self._format_playtime(playtime)

        return {
            "player": player,
            "online": "Oui" if online else "Non",
            "playtime": playtime or "N/A",
            "position": position or "N/A",
            "dimension": dimension or "N/A",
            "ping": f"{ping} ms" if ping is not None else "N/A",
        }

    def say(self, message: str):
        return self.rcon.say(message)

    def online_players(self) -> list[str]:
        response = self.rcon.list_players()
        return self._parse_online_players(response)

    def save_all(self):
        return self.rcon.save_all()

    def save_off(self):
        return self.rcon.save_off()

    def save_on(self):
        return self.rcon.save_on()

    def stop_server(self):
        return self.rcon.stop()

    def tps(self):
        return self.rcon.tps()

    # --------------------------------------------------
    # Dashboard
    # --------------------------------------------------

    def _player_status(self) -> dict[str, Any]:
        """
        Récupère les informations sur les joueurs connectés et le TPS.
        """

        result = {
            "players_summary": "RCON indisponible",
            "players": 0,
            "max_players": 0,
            "tps": "N/A",
            "rcon_success": False,
        }

        try:
            response = self.rcon.list_players()
            players, max_players = self._parse_player_counts(response)
            if players == 0 and max_players == 0 and response:
                logger.warning(
                    "Réponse list RCON non reconnue : %s", response
                )

            result.update(
                {
                    "players_summary": response,
                    "players": players,
                    "max_players": max_players,
                    "rcon_success": True,
                }
            )

        except Exception as exc:

            logger.warning(
                f"Impossible de récupérer les joueurs : {exc}"
            )
            result["players_summary"] = "RCON indisponible"
            result["rcon_error"] = str(exc)

        try:
            tps_response = self.rcon.tps()
            result["tps"] = self._parse_tps(tps_response)
            if result["tps"] == "N/A" and tps_response:
                logger.warning(
                    "Réponse tps RCON non reconnue : %s", tps_response
                )
        except Exception as exc:
            logger.warning("Impossible de récupérer le TPS : %s", exc)
            result["tps"] = "N/A"

        return result

    def _parse_player_counts(self, response: str) -> tuple[int, int]:
        match = self._PLAYERS_PATTERN.search(response)
        if not match:
            match = self._PLAYERS_SHORT_PATTERN.search(response)
        if not match:
            match = self._PLAYERS_FALLBACK_PATTERN.search(response)

        if match:
            return int(match.group(1)), int(match.group(2))

        logger.warning("Aucun format de joueurs reconnu dans la réponse RCON : %s", response)
        return 0, 0

    def _parse_tps(self, response: str) -> str:
        match = self._TPS_OVERALL_PATTERN.search(response)
        if match:
            return f"{match.group(1)} TPS"

        match = self._TPS_MULTI_PATTERN.search(response)
        if match:
            return f"{match.group(1)} TPS"

        values = self._TPS_SINGLE_PATTERN.findall(response)
        return f"{values[0]} TPS" if values else "N/A"

    def _parse_online_players(self, response: str) -> list[str]:
        match = self._PLAYER_LIST_PATTERN.search(response)
        if not match:
            return []

        player_list = match.group(1).strip()
        if not player_list:
            return []

        return [name.strip() for name in player_list.split(",") if name.strip()]

    def _get_player_data(self, player: str, path: str) -> str | None:
        try:
            response = self.rcon.command(f"data get entity {player} {path}")
            return self._parse_data_get_response(response)
        except Exception:
            return None

    def _parse_data_get_response(self, response: str) -> str | None:
        if not isinstance(response, str):
            return None

        lines = response.strip().splitlines()
        if not lines:
            return None

        last_line = lines[-1]
        if ": " in last_line:
            return last_line.split(": ", 1)[1].strip()

        return last_line.strip()

    def _format_playtime(self, value: str) -> str:
        try:
            ticks = int(re.search(r"-?\d+", value).group(0))
        except Exception:
            return "N/A"

        seconds = ticks // 20
        days, remainder = divmod(seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        parts = []
        if days:
            parts.append(f"{days}j")
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        if seconds or not parts:
            parts.append(f"{seconds}s")

        return " ".join(parts)