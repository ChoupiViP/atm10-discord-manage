import discord
from discord import app_commands
from discord.ext import commands

from bot.services.minecraft_service import MinecraftService


class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.minecraft = MinecraftService()

    server = app_commands.Group(
        name="server",
        description="Gestion du serveur Minecraft"
    )

    @server.command(
        name="status",
        description="Affiche le statut du serveur."
    )
    async def status(self, interaction: discord.Interaction):

        try:
            info = self.minecraft.get_status()

            color = (
                discord.Color.green()
                if info["status"] == "running"
                else discord.Color.red()
            )

            embed = discord.Embed(
                title="🎮 ATM10 Server",
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
                name="🔄 Politique de redémarrage",
                value=info["restart"],
                inline=False
            )

            await interaction.response.send_message(embed=embed)

        except Exception as e:

            embed = discord.Embed(
                title="❌ Erreur",
                description="Impossible de communiquer avec Docker.",
                color=discord.Color.red()
            )

            embed.add_field(
                name="Détails",
                value=f"```{e}```",
                inline=False
            )

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(Server(bot))