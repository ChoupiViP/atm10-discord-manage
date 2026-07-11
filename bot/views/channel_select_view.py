import discord

from bot.logger import logger
from bot.services.config_service import ConfigService


class ChannelSelect(discord.ui.ChannelSelect):

    def __init__(self, config_key: str):

        self.config_key = config_key

        super().__init__(
            placeholder="Sélectionnez un salon...",
            min_values=1,
            max_values=1,
            channel_types=[
                discord.ChannelType.text
            ]
        )

    async def callback(self, interaction: discord.Interaction):

        channel = self.values[0]

        if self.config_key == "dashboard":
            ConfigService.set_dashboard_channel(channel.id)

        elif self.config_key == "logs":
            ConfigService.set_logs_channel(channel.id)

        elif self.config_key == "chat":
            ConfigService.set_chat_channel(channel.id)

        elif self.config_key == "death":
            ConfigService.set_death_channel(channel.id)

        elif self.config_key == "connections":
            ConfigService.set_connections_channel(channel.id)

        elif self.config_key == "crash":
            ConfigService.set_crash_channel(channel.id)

        elif self.config_key == "notifications":
            ConfigService.set_notifications_channel(channel.id)

        embed = discord.Embed(
            title="✅ Configuration enregistrée",
            description=f"Salon sélectionné : {channel.mention}",
            color=discord.Color.green()
        )

        logger.info(
            f"{interaction.user} a configuré {self.config_key} -> {channel.id}"
        )

        await interaction.response.edit_message(
            embed=embed,
            view=None
        )


class ChannelSelectView(discord.ui.View):

    def __init__(self, config_key: str):

        super().__init__(timeout=300)

        self.add_item(ChannelSelect(config_key))