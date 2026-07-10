from datetime import datetime
from typing import Any

import discord


class DashboardEmbed:
    """Factory for the persistent Minecraft dashboard embed."""

    @staticmethod
    def create(info: dict[str, Any]) -> discord.Embed:
        """Build a modern status embed from a Minecraft status snapshot."""
        status = info.get("status", "unknown")
        container_running = info.get("success") and status == "running"
        server_online = info.get("rcon_success") is True
        color = discord.Color.green() if container_running and server_online else discord.Color.red()
        server_status = "🟢 En ligne" if server_online else "🔴 Hors ligne"

        embed = discord.Embed(
            title="Manager Server Minecraft",
            description="Dashboard permanent du serveur Minecraft Docker",
            color=color,
            timestamp=datetime.now(),
        )

        embed.add_field(name="Serveur", value=server_status, inline=True)
        embed.add_field(name="Docker", value=DashboardEmbed._value(status), inline=True)
        embed.add_field(
            name="Nom du conteneur",
            value=DashboardEmbed._value(info.get("name")),
            inline=True,
        )
        embed.add_field(
            name="CPU",
            value=DashboardEmbed._value(info.get("cpu")),
            inline=True,
        )
        embed.add_field(
            name="RAM",
            value=DashboardEmbed._value(info.get("ram")),
            inline=True,
        )
        embed.add_field(
            name="Disque",
            value=DashboardEmbed._value(info.get("disk", "Bientôt")),
            inline=True,
        )
        embed.add_field(
            name="Uptime",
            value=DashboardEmbed._value(info.get("uptime")),
            inline=True,
        )

        players = info.get("players")
        max_players = info.get("max_players")
        player_value = (
            f"{players} / {max_players}"
            if players is not None and max_players is not None
            else "N/A"
        )

        embed.add_field(name="Joueurs", value=player_value, inline=True)
        embed.add_field(name="TPS", value=DashboardEmbed._value(info.get("tps", "N/A")), inline=True)

        if not info.get("success") and info.get("error"):
            embed.add_field(
                name="Diagnostic",
                value=DashboardEmbed._trim(str(info["error"])),
                inline=False,
            )

        updated_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        embed.set_footer(text=f"Dernière mise à jour : {updated_at}")
        return embed

    @staticmethod
    def _value(value: Any) -> str:
        return str(value) if value not in (None, "") else "N/A"

    @staticmethod
    def _trim(value: str, limit: int = 900) -> str:
        if len(value) <= limit:
            return value
        return f"{value[:limit - 3]}..."
