import discord
from discord import app_commands
from discord.ext import commands
from json import dump

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


def create_dashboard(guild_id, channel_id):
    # Création du message
    message = bot.get_channel(channel_id).send(embed=DashboardEmbed().create(self.minecraft.get_status()))

    # Enregistrement des informations dans dashboard.json
    with open('data/dashboard.json', 'w') as f:
        json.dump({'guild_id': guild_id, 'channel_id': channel_id, 'message_id': message.id}, f)

async def modify_dashboard(interaction: discord.Interaction):
    info = self.minecraft.get_status()

    await interaction.response.send_message(
        embed=DashboardEmbed.create(info),
        view=DashboardView()
    )

async def delete_dashboard(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    channel_id = interaction.channel.id

    with open('data/dashboard.json', 'r') as f:
        data = json.load(f)

    if data['guild_id'] == guild_id and data['channel_id'] == channel_id:
        message_id = data['message_id']

        message = bot.get_channel(channel_id).get_message(message_id)
        await interaction.response.send_message("Dashboard supprimé avec succès.")

async def setup(bot):
    await bot.add_cog(Dashboard(bot))
