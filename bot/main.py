from pathlib import Path

import discord
from discord.ext import commands

from bot.config import Config
from bot.logger import logger


class ATM10Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()

        # Pour les futures commandes et événements
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix="!",
            intents=intents,
        )

    async def setup_hook(self):
        cog_folder = Path(__file__).parent / "cogs"

        for file in cog_folder.glob("*.py"):
            if file.stem.startswith("_"):
                continue

            extension = f"bot.cogs.{file.stem}"

            try:
                await self.load_extension(extension)
                logger.info(f"✓ Cog chargé : {file.stem}")

            except Exception as e:
                logger.error(f"Impossible de charger {file.stem}")
                logger.exception(e)

        synced = await self.tree.sync()
        logger.info(f"{len(synced)} commande(s) synchronisée(s).")

    async def on_ready(self):
        logger.info("=" * 40)
        logger.info(f"Connecté : {self.user}")
        logger.info(f"ID : {self.user.id}")
        logger.info("=" * 40)


bot = ATM10Bot()
bot.run(Config.DISCORD_TOKEN)