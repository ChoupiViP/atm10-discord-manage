print("docker.py chargé")

import discord
from discord import app_commands
from discord.ext import commands

from bot.services.docker_service import DockerService


class Docker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.docker = DockerService()

    @app_commands.command(
        name="docker",
        description="Affiche les informations du conteneur Docker."
    )
    async def docker_info(self, interaction: discord.Interaction):

        try:
            info = self.docker.get_status()

            color = (
                discord.Color.green()
                if info["status"] == "running"
                else discord.Color.red()
            )

            embed = discord.Embed(
                title="🐳 Docker - ATM10 Server",
                color=color
            )

            embed.add_field(
                name="📦 Conteneur",
                value=info["name"],
                inline=True
            )

            embed.add_field(
                name="📊 Statut",
                value=info["status"],
                inline=True
            )

            embed.add_field(
                name="🏷️ Image",
                value=info["image"],
                inline=False
            )

            embed.add_field(
                name="🔄 Redémarrage",
                value=info["restart"],
                inline=True
            )

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(
                f"❌ Impossible de récupérer les informations Docker.\n```{e}```",
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(Docker(bot))