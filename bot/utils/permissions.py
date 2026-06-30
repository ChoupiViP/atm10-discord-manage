import discord

from bot.config import Config


class Permissions:

    @staticmethod
    def has_permission(interaction: discord.Interaction) -> bool:

        if interaction.user.guild_permissions.administrator:
            return True

        for role in interaction.user.roles:
            if role.name == Config.AUTHORIZED_ROLE:
                return True

        return False