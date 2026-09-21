"""Structured logging boundary for SentriX features."""

from collections.abc import Awaitable, Callable
from datetime import datetime
from typing import Any
import logging


LOGGER = logging.getLogger("sentrix")
Sender = Callable[..., Awaitable[dict]]


def configure_logging(level: int = logging.INFO) -> None:
    if not LOGGER.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s sentrix: %(message)s"))
        LOGGER.addHandler(handler)
    LOGGER.setLevel(level)


def feature_error(feature: str, error: Exception) -> None:
    LOGGER.exception("%s feature failed: %s", feature, error)


def format_admin_event(
    event: str,
    user: str = "Unknown",
    admin: str = "System",
    reason: str = "No reason provided",
    extra: str = "",
) -> str:
    """Create the stable human-readable format used in the Telegram log channel."""
    lines = [
        f"🛡️ **{event.upper()}**",
        "",
        f"User: {user}",
        f"Admin: {admin}",
        f"Reason: {reason}",
        f"Time: {datetime.now().strftime('%H:%M')}",
    ]
    if extra:
        lines.extend(["", extra])
    return "\n".join(lines)


class AdminLogService:
    """Send structured events to the configured dedicated Telegram log channel."""

    def __init__(self, sender: Sender, channel_id: int):
        self._sender = sender
        self.channel_id = channel_id

    async def record(self, event: str, **fields: Any) -> dict:
        if not self.channel_id:
            LOGGER.warning("Skipped admin event %s: LOG_GROUP_ID is not configured", event)
            return {"ok": False, "description": "log channel not configured"}
        return await self._sender(
            self.channel_id,
            format_admin_event(event, **fields),
            parse_mode="Markdown",
        )
