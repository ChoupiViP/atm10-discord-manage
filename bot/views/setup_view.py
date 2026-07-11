import discord
from docker.errors import DockerException

from bot.logger import logger
from bot.modals.rcon_modal import RconModal
from bot.services.config_service import ConfigService
from bot.services.docker_service import DockerService
from bot.views.channel_select_view import ChannelSelectView
from bot.views.docker_select_view import DockerSelectView


class SetupView(discord.ui.View):
    """Vue principale du menu de configuration."""

    def __init__(self):
        super().__init__(timeout=300)
        self.docker = DockerService()

    # --------------------------------------------------
    # Docker
    # --------------------------------------------------

    @discord.ui.button(
        label="Docker",
        emoji="🐳",
        style=discord.ButtonStyle.blurple,
        row=0,
        custom_id="setup_docker"
    )
    async def docker(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        try:
            self.docker.connect()

            containers = self.docker.client.containers.list(all=True)

            if not containers:

                embed = discord.Embed(
                    title="❌ Aucun conteneur",
                    description="Aucun conteneur Docker n'a été trouvé.",
                    color=discord.Color.red()
                )

                await interaction.response.send_message(
                    embed=embed,
                    ephemeral=True
                )
                return

            embed = discord.Embed(
                title="🐳 Configuration Docker",
                description="Sélectionnez le conteneur Minecraft à utiliser.",
                color=discord.Color.blurple()
            )

            await interaction.response.send_message(
                embed=embed,
                view=DockerSelectView(containers),
                ephemeral=True
            )

        except DockerException as e:

            logger.exception(e)

            embed = discord.Embed(
                title="❌ Docker",
                description=f"Impossible de communiquer avec Docker.\n\n```{e}```",
                color=discord.Color.red()
            )

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

        except Exception as e:

            logger.exception(e)

            embed = discord.Embed(
                title="❌ Erreur",
                description=f"```{e}```",
                color=discord.Color.red()
            )

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

    # --------------------------------------------------
    # RCON
    # --------------------------------------------------

    @discord.ui.button(
        label="RCON",
        emoji="📡",
        style=discord.ButtonStyle.green,
        row=0,
        custom_id="setup_rcon"
    )
    async def rcon(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_modal(RconModal())

    # --------------------------------------------------
    # Dashboard
    # --------------------------------------------------

    @discord.ui.button(
        label="Dashboard",
        emoji="📊",
        style=discord.ButtonStyle.secondary,
        row=1,
        custom_id="setup_dashboard"
    )
    async def dashboard(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        embed = discord.Embed(
            title="📊 Configuration du Dashboard",
            description="Sélectionnez le salon qui accueillera le dashboard permanent.",
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(
            embed=embed,
            view=ChannelSelectView("dashboard"),
            ephemeral=True
        )

    # --------------------------------------------------
    # Logs
    # --------------------------------------------------

    @discord.ui.button(
        label="Logs",
        emoji="📜",
        style=discord.ButtonStyle.secondary,
        row=1,
        custom_id="setup_logs"
    )
    async def logs(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        embed = discord.Embed(
            title="📜 Configuration des Logs Minecraft",
            description=(
                "Sélectionnez le salon qui recevra les logs Minecraft et les messages système."
            ),
            color=discord.Color.orange()
        )

        await interaction.response.send_message(
            embed=embed,
            view=ChannelSelectView("logs"),
            ephemeral=True
        )

    @discord.ui.button(
        label="Connexions",
        emoji="🔌",
        style=discord.ButtonStyle.secondary,
        row=1,
        custom_id="setup_connections"
    )
    async def connections(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        embed = discord.Embed(
            title="🔌 Configuration des Connexions Minecraft",
            description=(
                "Sélectionnez le salon qui recevra les messages de connexion et déconnexion Minecraft."
            ),
            color=discord.Color.green()
        )

        await interaction.response.send_message(
            embed=embed,
            view=ChannelSelectView("connections"),
            ephemeral=True
        )

    @discord.ui.button(
        label="Crashs",
        emoji="💥",
        style=discord.ButtonStyle.secondary,
        row=1,
        custom_id="setup_crash"
    )
    async def crash(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        embed = discord.Embed(
            title="💥 Configuration des Crashs Minecraft",
            description=(
                "Sélectionnez le salon qui recevra les messages de crash Minecraft."
            ),
            color=discord.Color.red()
        )

        await interaction.response.send_message(
            embed=embed,
            view=ChannelSelectView("crash"),
            ephemeral=True
        )

    @discord.ui.button(
        label="Chat",
        emoji="💬",
        style=discord.ButtonStyle.secondary,
        row=1,
        custom_id="setup_chat"
    )
    async def chat(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        embed = discord.Embed(
            title="💬 Configuration du Chat Minecraft",
            description=(
                "Sélectionnez le salon qui recevra le chat Minecraft."
            ),
            color=discord.Color.orange()
        )

        await interaction.response.send_message(
            embed=embed,
            view=ChannelSelectView("chat"),
            ephemeral=True
        )

    @discord.ui.button(
        label="Morts",
        emoji="💀",
        style=discord.ButtonStyle.secondary,
        row=2,
        custom_id="setup_deaths"
    )
    async def deaths(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        embed = discord.Embed(
            title="💀 Configuration des Morts Minecraft",
            description=(
                "Sélectionnez le salon qui recevra les messages de mort Minecraft."
            ),
            color=discord.Color.red()
        )

        await interaction.response.send_message(
            embed=embed,
            view=ChannelSelectView("death"),
            ephemeral=True
        )

    # --------------------------------------------------
    # Notifications
    # --------------------------------------------------

    @discord.ui.button(
        label="Notifications",
        emoji="🔔",
        style=discord.ButtonStyle.secondary,
        row=2,
        custom_id="setup_notifications"
    )
    async def notifications(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        embed = discord.Embed(
            title="🔔 Configuration des Notifications",
            description="Sélectionnez le salon qui recevra les notifications.",
            color=discord.Color.gold()
        )

        await interaction.response.send_message(
            embed=embed,
            view=ChannelSelectView("notifications"),
            ephemeral=True
        )

    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    @discord.ui.button(
        label="Reset",
        emoji="🗑️",
        style=discord.ButtonStyle.danger,
        row=2,
        custom_id="setup_reset"
    )
    async def reset(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        ConfigService.reset()

        embed = discord.Embed(
            title="♻️ Configuration réinitialisée",
            description="Toute la configuration du bot a été supprimée.\nVous pouvez maintenant relancer `/setup`.",
            color=discord.Color.green()
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

        logger.info(f"{interaction.user} a réinitialisé la configuration.")