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
    _ANSI_PATTERN = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
    _MINECRAFT_COLOR_PATTERN = re.compile(r"§[0-9A-FK-ORa-fk-or]")
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
        logger.info(f"[PLAYER_INFO] Vérification du joueur '{player}' (bytes: {[ord(c) for c in player]}) dans la liste: {online_players!r}")
        
        # Vérifier le joueur avec case-insensitive si pas de match exact
        online = player in online_players
        logger.info(f"[PLAYER_INFO] Match exact: {online}")
        
        if not online:
            # Chercher avec correspondance case-insensitive
            online = any(p.lower() == player.lower() for p in online_players)
            if online:
                logger.info(f"[PLAYER_INFO] Match trouvé avec case-insensitive pour {player}")
        
        logger.info(f"[PLAYER_INFO] Résultat final - Joueur {player} connecté: {online}")
        
        position = self._get_player_data(player, "Pos")
        dimension = self._get_player_data(player, "Dimension")
        # Utiliser ticksLived au lieu de Stats qui peut être très volumineux (risque d'erreur RCON packet size)
        playtime = self._get_player_data(player, "ticksLived")
        ping = self._get_player_data(player, "Ping")

        if playtime is not None:
            playtime = self._format_playtime(playtime)

        return {
            "player": player,
            "online": "Oui" if online else "Non",
            "playtime": playtime or "N/A",
            "position": self._clean_rcon_value(position) or "N/A",
            "dimension": self._clean_rcon_value(dimension) or "N/A",
            "ping": f"{ping}" if ping and "Found no elements" not in str(ping) else "N/A",
        }

    def say(self, message: str):
        return self.rcon.say(message)

    def online_players(self) -> list[str]:
        response = self.rcon.list_players()
        logger.debug(f"[RCON] list_players response: {response!r}")
        players = self._parse_online_players(response)
        logger.debug(f"[RCON] parsed online players: {players}")
        return players

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
            logger.debug(f"Aucun match pour PLAYER_LIST_PATTERN dans: {response!r}")
            return []

        player_list = match.group(1).strip()
        if not player_list:
            logger.debug("Liste de joueurs vide")
            return []

        logger.info(f"[LIST] Raw player_list extrait: {player_list!r}")

        # Nettoyer d'abord les codes ANSI/couleurs
        player_list = self._ANSI_PATTERN.sub("", player_list)
        player_list = self._MINECRAFT_COLOR_PATTERN.sub("", player_list)
        logger.info(f"[LIST] Après nettoyage ANSI/couleurs: {player_list!r}")
        
        players = [name.strip() for name in player_list.split(",") if name.strip()]
        logger.info(f"[LIST] Joueurs en ligne détectés: {players!r}")
        
        # Debug: afficher les bytes pour chaque joueur
        for p in players:
            logger.debug(f"[LIST] Joueur '{p}' ({[ord(c) for c in p[:20]]}...)")
        
        return players

    def _get_player_data(self, player: str, path: str) -> str | None:
        try:
            response = self.rcon.command(f"data get entity {player} {path}")
            logger.debug(f"[RCON] data get entity {player} {path} => {response!r}")
            
            # Si la commande retourne "Found no elements", c'est une erreur, pas une réponse valide
            if isinstance(response, str) and "Found no elements" in response:
                logger.debug(f"Chemin NBT non trouvé pour {path}")
                return response
            
            # Détecter l'erreur de taille de paquet RCON
            if isinstance(response, str) and "invalid packet size" in response.lower():
                logger.warning(f"Erreur RCON packet size pour {path} du joueur {player}: {response}")
                return None
            
            result = self._parse_data_get_response(response)
            logger.debug(f"[RCON] parsed result: {result!r}")
            return result
        except Exception as exc:
            logger.warning(f"Erreur lors de la récupération de {path} pour {player}: {exc}")
            return None

    def _parse_data_get_response(self, response: str) -> str | None:
        if not isinstance(response, str):
            logger.debug(f"Response non-string: {type(response)}")
            return None

        # Nettoyer d'abord les codes ANSI/couleurs
        cleaned = self._ANSI_PATTERN.sub("", response)
        cleaned = self._MINECRAFT_COLOR_PATTERN.sub("", cleaned)
        cleaned = cleaned.replace("\x00", "").strip()

        if not cleaned:
            logger.debug(f"Response vide après nettoyage: {response!r}")
            return None

        logger.debug(f"Cleaned response: {cleaned!r}")

        # Chercher le format "key: value"
        if ": " in cleaned:
            parts = cleaned.split(": ", 1)
            value = parts[1].strip()
            logger.debug(f"Extracted value from key:value format: {value!r}")
            return value

        # Sinon retourner la ligne entière nettoyée
        logger.debug(f"No key:value format, returning cleaned: {cleaned!r}")
        return cleaned

    def _clean_rcon_value(self, value: str | None) -> str | None:
        if value is None:
            return None

        value = self._ANSI_PATTERN.sub("", value)
        value = self._MINECRAFT_COLOR_PATTERN.sub("", value)
        value = value.replace("\x00", "")
        value = value.strip()
        
        # Retirer les guillemets des strings Minecraft
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        
        # Formater les listes NBT [x, y, z] en coordonnées
        if value.startswith('[') and value.endswith(']'):
            # Extraire et formater: [-32.13888434360863d, 81.0d, 311.470264499304d] -> (-32.14, 81, 311.47)
            try:
                coords = value[1:-1].split(',')
                coords = [float(c.strip().rstrip('d')) for c in coords]
                value = f"({coords[0]:.2f}, {coords[1]:.0f}, {coords[2]:.2f})"
            except Exception:
                pass  # Garder la valeur originale si parse échoue
        
        return value or None

    def _format_playtime(self, value: str) -> str:
        if not value or "Found no elements" in value:
            logger.debug(f"Temps de jeu indisponible: {value!r}")
            return "N/A"
        
        try:
            match = re.search(r"-?\d+", value)
            if not match:
                logger.warning(f"Impossible de parser le temps de jeu: {value!r}")
                return "N/A"
            
            ticks = int(match.group(0))
        except Exception as exc:
            logger.warning(f"Erreur parsing temps de jeu: {exc}")
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