from typing import Any

import discord


class MinecraftEmbed:
    """Factory des embeds Minecraft."""

    @staticmethod
    def players(response: str) -> discord.Embed:
        """Affiche la réponse de la commande /list."""

        response = response.strip() or "Aucun joueur en ligne."

        embed = discord.Embed(
            title="👥 Joueurs connectés",
            description=f"```text\n{response}\n```",
            color=discord.Color.green()
        )

        return embed

    @staticmethod
    def command(command: str, response: str) -> discord.Embed:
        """Embed générique pour une commande RCON."""

        embed = discord.Embed(
            title="📡 Commande Minecraft",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="Commande",
            value=f"`/{command}`",
            inline=False
        )

        embed.add_field(
            name="Réponse",
            value=MinecraftEmbed._format_response(response),
            inline=False
        )

        return embed

    @staticmethod
    def success(title: str, response: str) -> discord.Embed:

        return discord.Embed(
            title=f"✅ {title}",
            description=MinecraftEmbed._format_response(response),
            color=discord.Color.green()
        )

    @staticmethod
    def error(message: Any) -> discord.Embed:

        return discord.Embed(
            title="❌ Erreur",
            description=str(message),
            color=discord.Color.red()
        )

    @staticmethod
    def _format_response(response: str) -> str:

        response = response.strip()

        if not response:
            response = "Commande exécutée."

        if len(response) > 3900:
            response = response[:3897] + "..."

        return f"```text\n{response}\n```"