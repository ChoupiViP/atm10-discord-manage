from datetime import datetime, timezone
from typing import Any

import docker
from docker.errors import DockerException, NotFound

from bot.config import Config
from bot.logger import logger


class DockerService:
    """Facade around Docker SDK operations for the Minecraft container."""

    def __init__(self) -> None:
        self.client = None

    def connect(self) -> None:
        """Initialize the Docker SDK client lazily."""
        if self.client is None:
            self.client = docker.from_env()

    def get_container(self):
        """Return the configured Minecraft Docker container."""
        self.connect()
        container_name = Config.get_docker_container()
        return self.client.containers.get(container_name)

    def get_status(self) -> dict[str, Any]:
        """Return a normalized status snapshot for dashboard rendering."""
        try:
            container = self.get_container()
            container.reload()
            stats = self._get_runtime_stats(container)

            return {
                "success": True,
                "name": container.name,
                "status": container.status,
                "image": self._image_name(container),
                "restart": container.attrs.get("HostConfig", {})
                .get("RestartPolicy", {})
                .get("Name", "unknown"),
                "cpu": stats["cpu"],
                "ram": stats["ram"],
                "disk": stats["disk"],
                "uptime": self._uptime(container),
            }
        except (DockerException, NotFound, ValueError) as exc:
            logger.warning("Impossible de récupérer le statut Docker: %s", exc)
            return {
                "success": False,
                "name": self._configured_container_name(),
                "status": "unavailable",
                "error": str(exc),
                "cpu": "N/A",
                "ram": "N/A",
                "disk": "N/A",
                "uptime": "N/A",
            }

    def start_container(self) -> None:
        """Start the configured container."""
        self.get_container().start()
        logger.info("Container Minecraft démarré")

    def stop_container(self) -> None:
        """Stop the configured container."""
        self.get_container().stop()
        logger.info("Container Minecraft arrêté")

    def restart_container(self) -> None:
        """Restart the configured container."""
        self.get_container().restart()
        logger.info("Container Minecraft redémarré")

    def _get_runtime_stats(self, container) -> dict[str, str]:
        if container.status != "running":
            return {"cpu": "0%", "ram": "0 MiB", "disk": "Bientôt"}

        try:
            stats = container.stats(stream=False)
        except DockerException as exc:
            logger.warning("Stats Docker indisponibles: %s", exc)
            return {"cpu": "N/A", "ram": "N/A", "disk": self._get_disk_usage(container)}

        return {
            "cpu": self._format_cpu(stats),
            "ram": self._format_memory(stats),
            "disk": self._get_disk_usage(container),
        }

    @staticmethod
    def _format_cpu(stats: dict[str, Any]) -> str:
        cpu_stats = stats.get("cpu_stats", {})
        previous_cpu = stats.get("precpu_stats", {})
        cpu_delta = (
            cpu_stats.get("cpu_usage", {}).get("total_usage", 0)
            - previous_cpu.get("cpu_usage", {}).get("total_usage", 0)
        )
        system_delta = (
            cpu_stats.get("system_cpu_usage", 0)
            - previous_cpu.get("system_cpu_usage", 0)
        )
        online_cpus = cpu_stats.get("online_cpus") or len(
            cpu_stats.get("cpu_usage", {}).get("percpu_usage", [])
        )

        if cpu_delta <= 0 or system_delta <= 0 or online_cpus <= 0:
            return "0%"

        return f"{(cpu_delta / system_delta) * online_cpus * 100:.1f}%"

    @staticmethod
    def _format_memory(stats: dict[str, Any]) -> str:
        memory_stats = stats.get("memory_stats", {})
        usage = memory_stats.get("usage", 0)
        limit = memory_stats.get("limit", 0)

        if not usage:
            return "0 MiB"

        usage_mib = usage / 1024 / 1024
        if not limit:
            return f"{usage_mib:.0f} MiB"

        limit_mib = limit / 1024 / 1024
        return f"{usage_mib:.0f} / {limit_mib:.0f} MiB"

    def _get_disk_usage(self, container) -> str:
        try:
            info = self.client.api.inspect_container(container.id, size=True)
            size_rootfs = info.get("SizeRootFs")
            if size_rootfs is None:
                return "N/A"
            return self._format_size(size_rootfs)
        except DockerException as exc:
            logger.warning("Disk Docker indisponible: %s", exc)
            return "N/A"

    @staticmethod
    def _format_size(value: int) -> str:
        if value < 1024:
            return f"{value} B"
        kib = value / 1024
        if kib < 1024:
            return f"{kib:.1f} KiB"
        mib = kib / 1024
        if mib < 1024:
            return f"{mib:.1f} MiB"
        gib = mib / 1024
        return f"{gib:.1f} GiB"

    @staticmethod
    def _image_name(container) -> str:
        tags = getattr(container.image, "tags", [])
        return tags[0] if tags else "Aucune"

    @staticmethod
    def _uptime(container) -> str:
        if container.status != "running":
            return "Arrêté"

        started_at = container.attrs.get("State", {}).get("StartedAt")
        if not started_at:
            return "N/A"

        started = DockerService._parse_docker_datetime(started_at)
        delta = datetime.now(timezone.utc) - started
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes = remainder // 60

        if days:
            return f"{days}j {hours}h {minutes}m"
        if hours:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"

    @staticmethod
    def _parse_docker_datetime(value: str) -> datetime:
        value = value.replace("Z", "+00:00")
        if "." not in value:
            return datetime.fromisoformat(value)

        prefix, suffix = value.split(".", 1)
        fraction = suffix[:6]
        timezone_part = suffix[6:]
        if "+" not in timezone_part and "-" not in timezone_part:
            timezone_part = "+00:00"

        return datetime.fromisoformat(f"{prefix}.{fraction}{timezone_part}")

    @staticmethod
    def _configured_container_name() -> str:
        try:
            return Config.get_docker_container()
        except ValueError:
            return "Non configuré"
