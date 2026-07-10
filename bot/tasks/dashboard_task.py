import asyncio

import discord
from discord.ext import tasks

from bot.embeds.dashboard_embed import DashboardEmbed
from bot.logger import logger
from bot.services.dashboard_service import DashboardService
from bot.services.minecraft_service import MinecraftService
from bot.views.dashboard_view import DashboardView


class DashboardTask:
    """Background refresh loop for the persistent dashboard message."""

    def __init__(self, bot: discord.Client) -> None:
        self.bot = bot
        self.dashboard = DashboardService()
        self.minecraft = MinecraftService()

    def start(self) -> None:
        """Start the refresh loop if it is not already running."""
        if not self.refresh_dashboard.is_running():
            self.refresh_dashboard.start()
            logger.info("Tâche dashboard démarrée")

    def stop(self) -> None:
        """Stop the refresh loop."""
        self.refresh_dashboard.cancel()

    @tasks.loop(seconds=30)
    async def refresh_dashboard(self) -> None:
        """Refresh the registered dashboard message every 30 seconds."""
        if not self.dashboard.exists():
            return

        try:
            channel = await self._get_channel(self.dashboard.get_channel_id())
            message = await channel.fetch_message(self.dashboard.get_message_id())
            info = await asyncio.to_thread(self.minecraft.status)
            await message.edit(
                embed=DashboardEmbed.create(info),
                view=DashboardView(self.minecraft),
            )
            self.dashboard.touch()
        except (discord.NotFound, ValueError):
            logger.warning(
                "Dashboard Discord introuvable, suppression de l'enregistrement"
            )
            self.dashboard.clear()
        except discord.Forbidden:
            logger.warning("Permissions insuffisantes pour rafraîchir le dashboard")
        except discord.HTTPException as exc:
            if getattr(exc, 'status', None) == 429:
                logger.warning(
                    "Rate limit lors du refresh dashboard, pause de 10 secondes"
                )
                await asyncio.sleep(10)
                return
            logger.warning("Erreur Discord pendant le refresh dashboard: %s", exc)
        except Exception:
            logger.exception("Erreur inattendue pendant le refresh dashboard")

    @refresh_dashboard.before_loop
    async def before_refresh_dashboard(self) -> None:
        """Wait until Discord is ready before refreshing messages."""
        await self.bot.wait_until_ready()

    async def _get_channel(self, channel_id: int | None):
        if channel_id is None:
            raise ValueError("channel_id manquant")

        channel = self.bot.get_channel(channel_id)
        if channel is not None:
            return channel

        return await self.bot.fetch_channel(channel_id)
