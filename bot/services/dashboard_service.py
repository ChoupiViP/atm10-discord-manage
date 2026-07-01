import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from bot.logger import logger


class DashboardService:
    """Persist and expose the unique Discord dashboard message."""

    DEFAULT_DATA = {
        "guild_id": None,
        "channel_id": None,
        "message_id": None,
        "created_at": None,
        "updated_at": None,
    }

    def __init__(self, storage_path: Path | str | None = None) -> None:
        self.storage_path = Path(storage_path or "data/dashboard.json")
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.storage_path.exists():
            self.clear()

    def save(self, guild_id: int, channel_id: int, message_id: int) -> None:
        """Save the current dashboard Discord identifiers."""
        now = self._now()
        data = {
            "guild_id": guild_id,
            "channel_id": channel_id,
            "message_id": message_id,
            "created_at": now,
            "updated_at": now,
        }
        self._write(data)
        logger.info(
            "Dashboard enregistré: guild=%s channel=%s message=%s",
            guild_id,
            channel_id,
            message_id,
        )

    def clear(self) -> None:
        """Remove the registered dashboard while keeping the storage file valid."""
        self._write(self.DEFAULT_DATA.copy())
        logger.info("Dashboard réinitialisé")

    def exists(self) -> bool:
        """Return whether a dashboard message is registered."""
        data = self.get_data()
        return all(
            data.get(key) is not None
            for key in ("guild_id", "channel_id", "message_id")
        )

    def get_data(self) -> dict[str, Any]:
        """Return dashboard data, repairing invalid storage if needed."""
        try:
            with self.storage_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("dashboard.json invalide, réinitialisation: %s", exc)
            self.clear()
            return self.DEFAULT_DATA.copy()

        return self.DEFAULT_DATA | data

    def get_guild_id(self) -> int | None:
        """Return the registered guild ID."""
        return self.get_data().get("guild_id")

    def get_channel_id(self) -> int | None:
        """Return the registered channel ID."""
        return self.get_data().get("channel_id")

    def get_message_id(self) -> int | None:
        """Return the registered message ID."""
        return self.get_data().get("message_id")

    def touch(self) -> None:
        """Update the last refresh timestamp in storage."""
        data = self.get_data()
        data["updated_at"] = self._now()
        self._write(data)

    def _write(self, data: dict[str, Any]) -> None:
        with self.storage_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.write("\n")

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()
