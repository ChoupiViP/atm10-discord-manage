from pathlib import Path

import discord
from discord.ext import commands

from bot.config import Config
from bot.logger import logger
from bot.tasks.dashboard_task import DashboardTask
from bot.views.dashboard_view import DashboardView


class ATM10Bot(commands.Bot):
    """Discord bot entrypoint for ATM10 Discord Manager."""

    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix="!",
            intents=intents,
        )
        self.dashboard_task: DashboardTask | None = None

    async def setup_hook(self) -> None:
        """Register persistent views, load cogs and start background tasks."""
        self.add_view(DashboardView())
        await self._load_cogs()

        self.dashboard_task = DashboardTask(self)
        self.dashboard_task.start()

        synced = await self.tree.sync()
        logger.info("%s commande(s) synchronisée(s).", len(synced))

    async def on_ready(self) -> None:
        """Log bot identity once Discord is ready."""
        logger.info("=" * 40)
        logger.info("Connecté : %s", self.user)
        logger.info("ID : %s", self.user.id if self.user else "inconnu")
        logger.info("=" * 40)

    async def _load_cogs(self) -> None:
        cog_folder = Path(__file__).parent / "cogs"

        for file in cog_folder.glob("*.py"):
            if file.stem.startswith("_"):
                continue

            extension = f"bot.cogs.{file.stem}"
            try:
                await self.load_extension(extension)
                logger.info("Cog chargé : %s", file.stem)
            except Exception:
                logger.exception("Impossible de charger l'extension %s", extension)


bot = ATM10Bot()
bot.run(Config.DISCORD_TOKEN)
