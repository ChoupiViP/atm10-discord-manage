from typing import Any

import discord

from bot.services.rcon_service import PlayerList


class MinecraftEmbed:
    """Factory for Minecraft RCON command embeds."""

    @staticmethod
    def players(players: PlayerList) -> discord.Embed:
        """Build an embed for the online player list."""
        names = "\n".join(f"- {name}" for name in players.names)
        names = names or "Aucun joueur en ligne"
        embed = discord.Embed(
            title="Joueurs Minecraft",
            description=names,
            color=discord.Color.green(),
        )
        embed.add_field(name="Connectés", value=players.summary, inline=True)
        return embed

    @staticmethod
    def command(command: str, response: str) -> discord.Embed:
        """Build an embed for a raw RCON command response."""
        embed = discord.Embed(
            title="Commande Minecraft",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="Commande", value=f"/{command}", inline=False)
        embed.add_field(
            name="Réponse",
            value=MinecraftEmbed._format_response(response),
            inline=False,
        )
        return embed

    @staticmethod
    def success(title: str, response: str) -> discord.Embed:
        """Build a generic success embed."""
        return discord.Embed(
            title=title,
            description=MinecraftEmbed._format_response(response),
            color=discord.Color.green(),
        )

    @staticmethod
    def error(message: Any) -> discord.Embed:
        """Build a generic error embed."""
        return discord.Embed(
            title="Erreur Minecraft",
            description=str(message),
            color=discord.Color.red(),
        )

    @staticmethod
    def _format_response(response: str) -> str:
        response = response.strip() or "Commande exécutée."
        if len(response) > 3900:
            response = f"{response[:3897]}..."
        return f"```text\n{response}\n```"
