import discord

from bot.logger import logger
from bot.services.config_service import ConfigService


class RconModal(discord.ui.Modal, title="Configuration RCON"):

    host = discord.ui.TextInput(
        label="Host",
        placeholder="mc ou 192.168.1.100",
        required=True,
        max_length=100
    )

    port = discord.ui.TextInput(
        label="Port",
        placeholder="25575",
        default="25575",
        required=True,
        max_length=5
    )

    password = discord.ui.TextInput(
        label="Mot de passe",
        placeholder="Mot de passe RCON",
        required=True,
        style=discord.TextStyle.short
    )

    async def on_submit(
        self,
        interaction: discord.Interaction
    ):

        try:

            port = int(self.port.value)

            ConfigService.set_rcon(
                host=self.host.value.strip(),
                port=port,
                password=self.password.value
            )

            embed = discord.Embed(
                title="✅ Configuration RCON",
                description="Les informations RCON ont été enregistrées avec succès.",
                color=discord.Color.green()
            )

            embed.add_field(
                name="Host",
                value=f"`{self.host.value}`",
                inline=False
            )

            embed.add_field(
                name="Port",
                value=f"`{port}`",
                inline=True
            )

            embed.add_field(
                name="Password",
                value="`********`",
                inline=True
            )

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

            logger.info(
                f"{interaction.user} a configuré le RCON ({self.host.value}:{port})"
            )

        except ValueError:

            embed = discord.Embed(
                title="❌ Erreur",
                description="Le port doit être un nombre.",
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