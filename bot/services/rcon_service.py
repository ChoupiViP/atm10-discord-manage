from mctools import RCONClient

from bot.logger import logger
from bot.services.config_service import ConfigService


class RconService:
    """Service de communication avec le serveur Minecraft via RCON."""

    def __init__(self):
        self.client = None

    # --------------------------------------------------
    # Connexion
    # --------------------------------------------------

    def connect(self):
        """Connexion au serveur RCON."""

        config = ConfigService.get_rcon()
        host = config.get("host")
        port = config.get("port")
        password = config.get("password")

        if not host:
            raise ValueError("Host RCON non configuré.")

        if not port:
            raise ValueError("Port RCON non configuré.")

        if not password:
            raise ValueError("Mot de passe RCON non configuré.")

        self.client = RCONClient(
            host,
            port=int(port)
        )

        self.client.login(config["password"])

        logger.info(
            f"Connexion RCON établie ({config['host']}:{config['port']})"
        )

    # --------------------------------------------------
    # Déconnexion
    # --------------------------------------------------

    def disconnect(self):
        """Ferme la connexion RCON."""

        if self.client:

            try:
                self.client.stop()

            except Exception:
                pass

            self.client = None

    # --------------------------------------------------
    # Commande générique
    # --------------------------------------------------

    def command(self, command: str):
        """Exécute une commande RCON."""

        try:

            self.connect()

            logger.info(f"Commande RCON : {command}")

            response = self.client.command(command)

            return response

        finally:

            self.disconnect()

    # --------------------------------------------------
    # Méthodes Minecraft
    # --------------------------------------------------

    def list_players(self):
        return self.command("list")

    def say(self, message: str):
        return self.command(f"say {message}")

    def save_all(self):
        return self.command("save-all")

    def save_off(self):
        return self.command("save-off")

    def save_on(self):
        return self.command("save-on")

    def stop(self):
        return self.command("stop")

    def tps(self):
        response = self.command("tps")

        if self._is_unknown_command(response):
            logger.info("Commande RCON 'tps' non supportée, tentative de 'forge tps'")
            response = self.command("forge tps")

        if self._is_unknown_command(response):
            logger.info("Commande RCON 'forge tps' non supportée, tentative de 'neoforge tps'")
            response = self.command("neoforge tps")

        return response

    @staticmethod
    def _is_unknown_command(response: str) -> bool:
        if not isinstance(response, str):
            return False

        lowered = response.strip().lower()
        return (
            "unknown or incomplete command" in lowered
            or "unknown command" in lowered
            or "incomplete command" in lowered
        )

    def time(self):
        return self.command("time query daytime")

    def weather(self):
        return self.command("weather query")

    def difficulty(self):
        return self.command("difficulty")

    def whitelist(self):
        return self.command("whitelist list")

    def version(self):
        return self.command("version")

    def execute(self, command: str):
        """Alias plus explicite de command()."""
        return self.command(command)