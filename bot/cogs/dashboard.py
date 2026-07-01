import asyncio

import discord
from discord import app_commands
from discord.ext import commands

from bot.embeds.dashboard_embed import DashboardEmbed
from bot.logger import logger
from bot.services.dashboard_service import DashboardService
from bot.services.minecraft_service import MinecraftService
from bot.utils.permissions import Permissions
from bot.views.dashboard_view import DashboardView


class Dashboard(commands.Cog):
    """Slash commands for the persistent Minecraft dashboard."""

    dashboard_group = app_commands.Group(
        name="dashboard",
        description="Gestion du dashboard Minecraft.",
    )

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.minecraft = MinecraftService()
        self.dashboard = DashboardService()

    @dashboard_group.command(
        name="create",
        description="Créer le dashboard permanent.",
    )
    async def create_dashboard(self, interaction: discord.Interaction) -> None:
        """Create and persist the unique dashboard message."""
        if not Permissions.has_permission(interaction):
            await interaction.response.send_message(
                "Vous n'avez pas la permission d'utiliser cette commande.",
                ephemeral=True,
            )
            return

        if self.dashboard.exists():
            await interaction.response.send_message(
                "Un dashboard existe déjà. Utilisez /dashboard refresh.",
                ephemeral=True,
            )
            return

        if interaction.guild is None or interaction.channel is None:
            await interaction.response.send_message(
                "Cette commande doit être utilisée dans un serveur Discord.",
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)
        info = await asyncio.to_thread(self.minecraft.status)
        message = await interaction.channel.send(
            embed=DashboardEmbed.create(info),
            view=DashboardView(self.minecraft),
        )
        self.dashboard.save(
            guild_id=interaction.guild.id,
            channel_id=interaction.channel.id,
            message_id=message.id,
        )
        await interaction.followup.send("Dashboard créé avec succès.", ephemeral=True)
        logger.info("Dashboard créé par %s", interaction.user)

    @dashboard_group.command(
        name="delete",
        description="Supprimer le dashboard permanent.",
    )
    async def delete_dashboard(self, interaction: discord.Interaction) -> None:
        """Delete the registered dashboard message and clear storage."""
        if not Permissions.has_permission(interaction):
            await interaction.response.send_message(
                "Vous n'avez pas la permission d'utiliser cette commande.",
                ephemeral=True,
            )
            return

        if not self.dashboard.exists():
            await interaction.response.send_message(
                "Aucun dashboard enregistré.",
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)
        try:
            channel = await self._get_channel(self.dashboard.get_channel_id())
            message = await channel.fetch_message(self.dashboard.get_message_id())
            await message.delete()
        except (discord.NotFound, ValueError):
            logger.info("Dashboard déjà absent côté Discord")
        except discord.HTTPException as exc:
            logger.warning("Suppression du dashboard impossible: %s", exc)

        self.dashboard.clear()
        await interaction.followup.send("Dashboard supprimé.", ephemeral=True)

    @dashboard_group.command(name="refresh", description="Mettre à jour le dashboard.")
    async def refresh_dashboard(self, interaction: discord.Interaction) -> None:
        """Refresh the registered dashboard message immediately."""
        if not self.dashboard.exists():
            await interaction.response.send_message(
                "Aucun dashboard enregistré.",
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)
        try:
            channel = await self._get_channel(self.dashboard.get_channel_id())
            message = await channel.fetch_message(self.dashboard.get_message_id())
            info = await asyncio.to_thread(self.minecraft.status)
            await message.edit(
                embed=DashboardEmbed.create(info),
                view=DashboardView(self.minecraft),
            )
            self.dashboard.touch()
        except (discord.NotFound, ValueError):
            self.dashboard.clear()
            await interaction.followup.send(
                "Le message dashboard n'existe plus. L'enregistrement a été nettoyé.",
                ephemeral=True,
            )
            return

        await interaction.followup.send("Dashboard mis à jour.", ephemeral=True)

    async def _get_channel(self, channel_id: int | None):
        if channel_id is None:
            raise ValueError("channel_id manquant")

        channel = self.bot.get_channel(channel_id)
        if channel is not None:
            return channel

        return await self.bot.fetch_channel(channel_id)


async def setup(bot: commands.Bot) -> None:
    """Register the dashboard cog."""
    await bot.add_cog(Dashboard(bot))
