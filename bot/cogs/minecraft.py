import asyncio

import discord
from discord import app_commands
from discord.ext import commands

from bot.embeds.minecraft_embed import MinecraftEmbed
from bot.services.minecraft_service import MinecraftService
from bot.utils.permissions import Permissions


class Minecraft(commands.Cog):
    """Minecraft RCON slash commands."""

    minecraft_group = app_commands.Group(
        name="minecraft",
        description="Commandes Minecraft via RCON.",
    )

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.minecraft = MinecraftService()

    @minecraft_group.command(
        name="players",
        description="Afficher les joueurs connectés.",
    )
    async def players(self, interaction: discord.Interaction) -> None:
        """Show online Minecraft players."""
        await interaction.response.defer(ephemeral=True)

        try:
            players = await asyncio.to_thread(self.minecraft.list_players)
        except Exception as exc:
            await interaction.followup.send(
                embed=MinecraftEmbed.error(exc),
                ephemeral=True,
            )
            return

        await interaction.followup.send(
            embed=MinecraftEmbed.players(players),
            ephemeral=True,
        )

    @minecraft_group.command(
        name="command",
        description="Exécuter une commande Minecraft via RCON.",
    )
    @app_commands.describe(command="Commande Minecraft sans slash initial")
    async def command(
        self,
        interaction: discord.Interaction,
        command: str,
    ) -> None:
        """Run a raw Minecraft command through RCON."""
        if not Permissions.has_permission(interaction):
            await interaction.response.send_message(
                embed=MinecraftEmbed.error(
                    "Vous n avez pas la permission d utiliser cette commande."
                ),
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)
        safe_command = command.strip().lstrip("/")

        try:
            response = await asyncio.to_thread(self.minecraft.command, safe_command)
        except Exception as exc:
            await interaction.followup.send(
                embed=MinecraftEmbed.error(exc),
                ephemeral=True,
            )
            return

        await interaction.followup.send(
            embed=MinecraftEmbed.command(safe_command, response),
            ephemeral=True,
        )

    @minecraft_group.command(
        name="save",
        description="Forcer une sauvegarde du monde Minecraft.",
    )
    async def save(self, interaction: discord.Interaction) -> None:
        """Force a Minecraft world save through RCON."""
        if not Permissions.has_permission(interaction):
            await interaction.response.send_message(
                embed=MinecraftEmbed.error(
                    "Vous n avez pas la permission d utiliser cette commande."
                ),
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)

        try:
            response = await asyncio.to_thread(self.minecraft.save_world)
        except Exception as exc:
            await interaction.followup.send(
                embed=MinecraftEmbed.error(exc),
                ephemeral=True,
            )
            return

        await interaction.followup.send(
            embed=MinecraftEmbed.success("Sauvegarde demandée", response),
            ephemeral=True,
        )


async def setup(bot: commands.Bot) -> None:
    """Register the Minecraft cog."""
    await bot.add_cog(Minecraft(bot))
