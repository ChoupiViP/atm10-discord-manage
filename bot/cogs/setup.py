import discord
from discord import app_commands
from discord.ext import commands

from bot.logger import logger
from bot.utils.permissions import Permissions
from bot.views.setup_view import SetupView


class Setup(commands.Cog):
    """Configuration du bot."""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="setup",
        description="Ouvre le panneau de configuration du bot."
    )
    async def setup(
        self,
        interaction: discord.Interaction
    ):

        if not Permissions.has_permission(interaction):

            embed = discord.Embed(
                title="❌ Accès refusé",
                description="Vous n'avez pas la permission d'utiliser cette commande.",
                color=discord.Color.red()
            )

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

            return

        embed = discord.Embed(
            title="⚙ Configuration ATM10 Discord Manager",
            description=(
                "Bienvenue dans le centre de configuration.\n\n"
                "Choisissez un élément à configurer."
            ),
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="🐳 Docker",
            value="Configurer le conteneur Docker.",
            inline=False
        )

        embed.add_field(
            name="📡 RCON",
            value="Configurer la connexion RCON.",
            inline=False
        )

        embed.add_field(
            name="📊 Dashboard",
            value="Configurer le salon du dashboard.",
            inline=False
        )

        embed.add_field(
            name="📜 Logs",
            value="Configurer le salon des logs.",
            inline=False
        )

        embed.add_field(
            name="🔔 Notifications",
            value="Configurer le salon des notifications.",
            inline=False
        )

        embed.add_field(
            name="🗑 Reset",
            value="Réinitialiser la configuration.",
            inline=False
        )

        await interaction.response.send_message(
            embed=embed,
            view=SetupView(),
            ephemeral=True
        )

        logger.info(f"{interaction.user} a ouvert le menu Setup")


async def setup(bot):
    await bot.add_cog(Setup(bot))