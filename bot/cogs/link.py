import discord
from discord import app_commands
from discord.ext import commands

from bot.embeds.minecraft_embed import MinecraftEmbed
from bot.services.link_service import LinkService


class Link(commands.Cog):
    """Commande de liaison Discord <-> Minecraft."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="link", description="Lier votre compte Discord à votre pseudo Minecraft.")
    async def link(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)

        code = LinkService.generate_link_code(interaction.user.id)
        await interaction.followup.send(
            embed=MinecraftEmbed.success(
                "Lien créé",
                (
                    "Pour lier votre compte, envoyez ce code dans le chat Minecraft :\n"
                    f"`{code}`\n\n"
                    "Puis attendez la confirmation ici."
                ),
            ),
            ephemeral=True,
        )

    @app_commands.command(name="unlink", description="Supprimer votre lien Discord/Minecraft.")
    async def unlink(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)

        LinkService.remove_link(interaction.user.id)
        await interaction.followup.send(
            embed=MinecraftEmbed.success(
                "Lien supprimé",
                "Votre compte Discord n'est plus lié à un pseudo Minecraft.",
            ),
            ephemeral=True,
        )

    @app_commands.command(name="myprofile", description="Voir votre lien Discord/Minecraft.")
    async def myprofile(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)

        minecraft_name = LinkService.get_minecraft_name(interaction.user.id)
        if not minecraft_name:
            await interaction.followup.send(
                embed=MinecraftEmbed.error(
                    "Aucun lien trouvé. Utilisez `/link` pour lier votre pseudo Minecraft."
                ),
                ephemeral=True,
            )
            return

        await interaction.followup.send(
            embed=MinecraftEmbed.success(
                "Profil lié",
                f"Discord : {interaction.user.display_name}\nMinecraft : {minecraft_name}",
            ),
            ephemeral=True,
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Link(bot))
