from typing import Any

from bot.services.docker_service import DockerService


class MinecraftService:
    """Application service for Minecraft server operations."""

    def __init__(self, docker_service: DockerService | None = None) -> None:
        self.docker = docker_service or DockerService()

    def status(self) -> dict[str, Any]:
        """Return the current Minecraft server status."""
        return self.docker.get_status()

    def get_status(self) -> dict[str, Any]:
        """Backward-compatible alias used by existing cogs."""
        return self.status()

    def start(self) -> None:
        """Start the Minecraft server container."""
        self.docker.start_container()

    def stop(self) -> None:
        """Stop the Minecraft server container."""
        self.docker.stop_container()

    def restart(self) -> None:
        """Restart the Minecraft server container."""
        self.docker.restart_container()
