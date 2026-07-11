import asyncio
import re
import threading
import time

import discord

from bot.logger import logger
from bot.services.config_service import ConfigService
from bot.services.docker_service import DockerService
from bot.services.minecraft_service import MinecraftService


class MinecraftChatTask:
    """Background task that syncs Minecraft chat and death events to Discord."""

    _CHAT_PATTERN = re.compile(r"^\[.*?\] \[.*?\]: <(.+?)> (.+)$")
    _DEATH_PATTERN = re.compile(
        r"^\[.*?\] \[.*?\]: (.+? (?:died|was slain by|went up in flames|went up in flames|fell from a high place|fell out of the world|walked into a cactus|walked into fire|walked into danger|was shot by|was killed by|was blown up|was killed trying to hurt|hit the ground too hard|drowned|suffocated|burned to death|walked into a wall|was pricked to death|withered away|went off with a bang|blew up|tried to swim in lava|tried to sleep in a non-empty bed|lost the game).*)$",
        re.IGNORECASE,
    )
    _DISCORD_BRIDGE = "[Discord]"
    _JOIN_PATTERN = re.compile(r"^\[.*?\] \[.*?\]: (.+?) joined the game$")
    _LEAVE_PATTERN = re.compile(r"^\[.*?\] \[.*?\]: (.+?) left the game$")
    _CRASH_PATTERN = re.compile(
        r"\b(crash|crashed|exception|stacktrace|fatal|error)\b",
        re.IGNORECASE,
    )

    _ANSI_PATTERN = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")

    def __init__(self, bot: discord.Client) -> None:
        self.bot = bot
        self.minecraft = MinecraftService()
        self.docker = DockerService()
        self.queue: asyncio.Queue[str] = asyncio.Queue()
        self.thread: threading.Thread | None = None
        self.task: asyncio.Task | None = None
        self._events_channel_id: int | None = None
        self._events_channel: discord.TextChannel | None = None
        self._chat_channel_id: int | None = None
        self._chat_channel: discord.TextChannel | None = None
        self._death_channel_id: int | None = None
        self._death_channel: discord.TextChannel | None = None
        self._log_buffer = ""

    def start(self) -> None:
        if self.task is None or self.task.done():
            self.task = asyncio.create_task(self._run())
            logger.info("Tâche Minecraft chat démarrée")

    async def _run(self) -> None:
        await self.bot.wait_until_ready()
        self._start_thread()

        while not self.bot.is_closed():
            line = await self.queue.get()
            try:
                await self._handle_log_line(line)
            except Exception:
                logger.exception("Erreur pendant le traitement d'une ligne de log Minecraft")

    def _start_thread(self) -> None:
        if self.thread and self.thread.is_alive():
            return

        self.thread = threading.Thread(target=self._read_logs, daemon=True)
        self.thread.start()

    def _read_logs(self) -> None:
        while True:
            try:
                container = self.docker.get_container()
                for raw in container.logs(
                    stream=True,
                    follow=True,
                    stdout=True,
                    stderr=True,
                    tail=1,
                ):
                    if raw is None:
                        continue

                    decoded = raw.decode("utf-8", errors="replace")
                    decoded = self._ANSI_PATTERN.sub("", decoded)
                    self._log_buffer += decoded

                    while "\n" in self._log_buffer:
                        line, self._log_buffer = self._log_buffer.split("\n", 1)
                        line = self._clean_log_line(line).strip()
                        if not line:
                            continue

                        asyncio.run_coroutine_threadsafe(
                            self.queue.put(line),
                            self.bot.loop,
                        )
            except Exception as exc:
                logger.warning(
                    "Impossible de suivre les logs Minecraft : %s",
                    exc,
                )
                time.sleep(5)

    async def _handle_log_line(self, line: str) -> None:
        if self._is_discord_bridge_line(line):
            return

        chat_channel = await self._get_chat_channel()
        death_channel = await self._get_death_channel()
        events_channel = await self._get_logs_channel()

        chat_match = self._CHAT_PATTERN.match(line)
        if chat_match and (chat_channel is not None or events_channel is not None):
            target = chat_channel or events_channel
            author = chat_match.group(1)
            message = chat_match.group(2)
            await target.send(f"**{author}** : {message}")
            return

        death_message = self._parse_death_line(line)
        if death_message and (death_channel is not None or events_channel is not None or chat_channel is not None):
            target = death_channel or events_channel or chat_channel
            embed = discord.Embed(
                title="💀 Mort Minecraft",
                description=death_message,
                color=discord.Color.red(),
            )
            await target.send(embed=embed)
            return

        join_player = self._parse_join_line(line)
        if join_player and events_channel is not None:
            embed = discord.Embed(
                title="✅ Connexion Minecraft",
                description=f"{join_player} est connecté.",
                color=discord.Color.green(),
            )
            await events_channel.send(embed=embed)
            return

        leave_player = self._parse_leave_line(line)
        if leave_player and events_channel is not None:
            embed = discord.Embed(
                title="❌ Déconnexion Minecraft",
                description=f"{leave_player} s'est déconnecté.",
                color=discord.Color.orange(),
            )
            await events_channel.send(embed=embed)
            return

        if self._is_crash_line(line) and events_channel is not None:
            embed = discord.Embed(
                title="🚨 Crash Minecraft",
                description=line,
                color=discord.Color.dark_red(),
            )
            await events_channel.send(embed=embed)
            return

        if events_channel is not None:
            await events_channel.send(f"`{line}`")

    async def _get_logs_channel(self) -> discord.TextChannel | None:
        channel_id = ConfigService.get_logs_channel()
        if channel_id is None:
            self._events_channel_id = None
            self._events_channel = None
            return None

        if self._events_channel_id == channel_id and self._events_channel is not None:
            return self._events_channel

        self._events_channel_id = channel_id
        channel = self.bot.get_channel(channel_id)
        if channel is not None and isinstance(channel, discord.TextChannel):
            self._events_channel = channel
            return channel

        try:
            fetched = await self.bot.fetch_channel(channel_id)
        except discord.NotFound:
            self._events_channel = None
            return None

        if isinstance(fetched, discord.TextChannel):
            self._events_channel = fetched
            return fetched

        self._events_channel = None
        return None

    async def _get_chat_channel(self) -> discord.TextChannel | None:
        channel_id = ConfigService.get_chat_channel()
        if channel_id is None:
            self._chat_channel_id = None
            self._chat_channel = None
            return None

        if self._chat_channel_id == channel_id and self._chat_channel is not None:
            return self._chat_channel

        self._chat_channel_id = channel_id
        channel = self.bot.get_channel(channel_id)
        if channel is not None and isinstance(channel, discord.TextChannel):
            self._chat_channel = channel
            return channel

        try:
            fetched = await self.bot.fetch_channel(channel_id)
        except discord.NotFound:
            self._chat_channel = None
            return None

        if isinstance(fetched, discord.TextChannel):
            self._chat_channel = fetched
            return fetched

        self._chat_channel = None
        return None

    async def _get_death_channel(self) -> discord.TextChannel | None:
        channel_id = ConfigService.get_death_channel()
        if channel_id is None:
            self._death_channel_id = None
            self._death_channel = None
            return None

        if self._death_channel_id == channel_id and self._death_channel is not None:
            return self._death_channel

        self._death_channel_id = channel_id
        channel = self.bot.get_channel(channel_id)
        if channel is not None and isinstance(channel, discord.TextChannel):
            self._death_channel = channel
            return channel

        try:
            fetched = await self.bot.fetch_channel(channel_id)
        except discord.NotFound:
            self._death_channel = None
            return None

        if isinstance(fetched, discord.TextChannel):
            self._death_channel = fetched
            return fetched

        self._death_channel = None
        return None

    def _is_discord_bridge_line(self, line: str) -> bool:
        return self._DISCORD_BRIDGE in line

    def _clean_log_line(self, line: str) -> str:
        line = self._ANSI_PATTERN.sub("", line)
        line = line.replace("\r", "")
        return "".join(ch for ch in line if ch == "\t" or ch >= " ")

    def _parse_join_line(self, line: str) -> str | None:
        match = self._JOIN_PATTERN.match(line)
        return match.group(1).strip() if match else None

    def _parse_leave_line(self, line: str) -> str | None:
        match = self._LEAVE_PATTERN.match(line)
        return match.group(1).strip() if match else None

    def _is_crash_line(self, line: str) -> bool:
        return bool(self._CRASH_PATTERN.search(line))

    def _parse_death_line(self, line: str) -> str | None:
        match = self._DEATH_PATTERN.match(line)
        if not match:
            return None

        return match.group(1).strip()
