import asyncio

import discord
from docker.errors import DockerException

from bot.embeds.dashboard_embed import DashboardEmbed
from bot.logger import logger
from bot.services.minecraft_service import MinecraftService
from bot.utils.permissions import Permissions


class DashboardView(discord.ui.View):
    """Persistent controls for the Minecraft Docker dashboard."""

    def __init__(self, minecraft_service: MinecraftService | None = None) -> None:
        super().__init__(timeout=None)
        self.minecraft = minecraft_service or MinecraftService()

    @discord.ui.button(
        emoji="🚀",
        label="Start",
        style=discord.ButtonStyle.green,
        custom_id="atm10_dashboard:start",
    )
    async def start(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ) -> None:
        """Start the Minecraft container and refresh the dashboard."""
        await self._run_action(interaction, self.minecraft.start)

    @discord.ui.button(
        emoji="⏹",
        label="Stop",
        style=discord.ButtonStyle.red,
        custom_id="atm10_dashboard:stop",
    )
    async def stop(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ) -> None:
        """Stop the Minecraft container and refresh the dashboard."""
        await self._run_action(interaction, self.minecraft.stop)

    @discord.ui.button(
        emoji="🔄",
        label="Restart",
        style=discord.ButtonStyle.blurple,
        custom_id="atm10_dashboard:restart",
    )
    async def restart(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ) -> None:
        """Restart the Minecraft container and refresh the dashboard."""
        await self._run_action(interaction, self.minecraft.restart)

    @discord.ui.button(
        emoji="📊",
        label="Refresh",
        style=discord.ButtonStyle.gray,
        custom_id="atm10_dashboard:refresh",
    )
    async def refresh(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ) -> None:
        """Refresh the dashboard without changing the server state."""
        await self._refresh_message(interaction)

    async def _run_action(self, interaction: discord.Interaction, action) -> None:
        if not Permissions.has_permission(interaction):
            await interaction.response.send_message(
                "Vous n'avez pas la permission d'utiliser cette action.",
                ephemeral=True,
            )
            return

        await interaction.response.defer()
        try:
            await asyncio.to_thread(action)
        except (DockerException, ValueError) as exc:
            logger.warning("Action dashboard impossible: %s", exc)
            await interaction.followup.send(str(exc), ephemeral=True)
            return

        info = await asyncio.to_thread(self.minecraft.status)
        await interaction.edit_original_response(
            embed=DashboardEmbed.create(info),
            view=self,
        )

    async def _refresh_message(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        info = await asyncio.to_thread(self.minecraft.status)
        await interaction.edit_original_response(
            embed=DashboardEmbed.create(info),
            view=self,
        )
