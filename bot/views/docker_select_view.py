import discord

from bot.logger import logger
from bot.services.config_service import ConfigService


class DockerSelect(discord.ui.Select):

    def __init__(self, containers):

        options = []

        for container in containers:

            options.append(
                discord.SelectOption(
                    label=container.name,
                    description=f"Status : {container.status}",
                    value=container.name
                )
            )

        super().__init__(
            placeholder="Sélectionnez un conteneur...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        ConfigService.set_container(self.values[0])

        embed = discord.Embed(
            title="✅ Docker configuré",
            description=f"Conteneur sélectionné : **{self.values[0]}**",
            color=discord.Color.green()
        )

        logger.info(
            f"{interaction.user} a configuré Docker ({self.values[0]})"
        )

        await interaction.response.edit_message(
            embed=embed,
            view=None
        )


class DockerSelectView(discord.ui.View):

    def __init__(self, containers):

        super().__init__(timeout=300)

        self.add_item(DockerSelect(containers))