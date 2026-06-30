import discord
from discord import app_commands
from discord.ext import commands

from bot.embeds.dashboard_embed import DashboardEmbed
from bot.services.minecraft_service import MinecraftService
from bot.views.dashboard_view import DashboardView


class Dashboard(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.minecraft = MinecraftService()

    @app_commands.command(
        name="dashboard",
        description="Affiche le dashboard du serveur."
    )
    async def dashboard(
        self,
        interaction: discord.Interaction
    ):

        info = self.minecraft.get_status()

        await interaction.response.send_message(
            embed=DashboardEmbed.create(info),
            view=DashboardView()
        )


async def setup(bot):
    await bot.add_cog(Dashboard(bot))