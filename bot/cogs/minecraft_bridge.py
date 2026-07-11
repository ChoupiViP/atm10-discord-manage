import asyncio

import discord
from discord.ext import commands

from bot.logger import logger
from bot.services.link_service import LinkService
from bot.services.config_service import ConfigService
from bot.services.minecraft_service import MinecraftService


class MinecraftBridge(commands.Cog):
    """Forward Discord messages from the chat channel into Minecraft chat."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.minecraft = MinecraftService()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        channel_id = ConfigService.get_chat_channel()
        if not channel_id or message.channel.id != channel_id:
            return

        if not message.content:
            return

        text = message.content.strip()
        if not text:
            return

        discord_name = message.author.display_name
        minecraft_name = LinkService.get_minecraft_name(message.author.id)
        suffix = f" ({minecraft_name})" if minecraft_name else ""
        payload = f"[Discord] {discord_name}{suffix}: {text}"
        if len(payload) > 250:
            payload = payload[:247] + "..."

        try:
            await asyncio.to_thread(self.minecraft.say, payload)
        except Exception as exc:
            logger.warning("Impossible d'envoyer le message Minecraft via RCON : %s", exc)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MinecraftBridge(bot))
