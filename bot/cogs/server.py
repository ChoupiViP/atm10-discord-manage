import discord
from discord import app_commands
from discord.ext import commands

from bot.embeds.server_embed import ServerEmbed
from bot.services.minecraft_service import MinecraftService
from bot.views.confirm_view import ConfirmView
from bot.utils.permissions import Permissions

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
        description="Affiche l'état du serveur."
    )
    async def status(
        self,
        interaction: discord.Interaction
    ):

        info = self.minecraft.get_status()

        if not info["success"]:

            await interaction.response.send_message(
                embed=ServerEmbed.error(
                    f"Impossible de communiquer avec Docker.\n\n```{info['error']}```"
                ),
                ephemeral=True
            )

            return

        await interaction.response.send_message(
            embed=ServerEmbed.status(info)
        )

    @server.command(
        name="start",
        description="Démarre le serveur."
    )
    async def start(
        self,
        interaction: discord.Interaction
    ):

        if not Permissions.has_permission(interaction):

            await interaction.response.send_message(
                embed=ServerEmbed.error(
                    "Vous n'avez pas la permission d'utiliser cette commande."
                ),
                ephemeral=True
            )
            return

        try:

            self.minecraft.start()

            await interaction.response.send_message(
                embed=ServerEmbed.success(
                    "Le serveur a été démarré."
                )
            )

        except Exception as e:

            await interaction.response.send_message(
                embed=ServerEmbed.error(str(e)),
                ephemeral=True
            )

    @server.command(
    name="stop",
        description="Arrête le serveur."
    )
    async def stop(
        self,
        interaction: discord.Interaction
    ):

        if not Permissions.has_permission(interaction):

            await interaction.response.send_message(
                embed=ServerEmbed.error(
                    "Vous n'avez pas la permission d'utiliser cette commande."
                ),
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="⚠ Confirmation",
            description="Voulez-vous vraiment arrêter le serveur ?",
            color=discord.Color.orange()
        )

        await interaction.response.send_message(
            embed=embed,
            view=ConfirmView(self.minecraft.stop)
        )

    @server.command(
        name="restart",
        description="Redémarre le serveur."
    )
    async def restart(
        self,
        interaction: discord.Interaction
    ):

        if not Permissions.has_permission(interaction):

            await interaction.response.send_message(
                embed=ServerEmbed.error(
                    "Vous n'avez pas la permission d'utiliser cette commande."
                ),
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="⚠ Confirmation",
            description="Voulez-vous vraiment redémarrer le serveur ?",
            color=discord.Color.orange()
        )

        await interaction.response.send_message(
            embed=embed,
            view=ConfirmView(self.minecraft.restart)
        )


async def setup(bot):
    await bot.add_cog(Server(bot))