import discord

from bot.embeds.dashboard_embed import DashboardEmbed
from bot.services.minecraft_service import MinecraftService


class DashboardView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

        self.minecraft = MinecraftService()

    @discord.ui.button(
        emoji="🚀",
        label="Start",
        style=discord.ButtonStyle.green
    )
    async def start(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        self.minecraft.start()

        info = self.minecraft.get_status()

        await interaction.response.edit_message(
            embed=DashboardEmbed.create(info),
            view=self
        )

    @discord.ui.button(
        emoji="⏹",
        label="Stop",
        style=discord.ButtonStyle.red
    )
    async def stop(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        self.minecraft.stop()

        info = self.minecraft.get_status()

        await interaction.response.edit_message(
            embed=DashboardEmbed.create(info),
            view=self
        )

    @discord.ui.button(
        emoji="🔄",
        label="Restart",
        style=discord.ButtonStyle.blurple
    )
    async def restart(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        self.minecraft.restart()

        info = self.minecraft.get_status()

        await interaction.response.edit_message(
            embed=DashboardEmbed.create(info),
            view=self
        )

    @discord.ui.button(
        emoji="📊",
        label="Refresh",
        style=discord.ButtonStyle.gray
    )
    async def refresh(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        info = self.minecraft.get_status()

        await interaction.response.edit_message(
            embed=DashboardEmbed.create(info),
            view=self
        )