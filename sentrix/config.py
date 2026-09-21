"""Typed, environment-backed configuration for SentriX."""

from dataclasses import dataclass
from functools import lru_cache
import os


@dataclass(frozen=True, slots=True)
class SentriXConfig:
    bot_token: str
    api_id: int
    api_hash: str
    owner_id: int
    admin_ids: frozenset[int] = frozenset()
    bot_username: str = "HR_sentrix_bot"
    log_group_id: int = 0
    support_url: str = "https://t.me/sentrix_support"
    updates_url: str = "https://t.me/sentrix_updates"
    storage_path: str = "/data/modbot"
    fallback_storage_path: str = "/tmp/modbot_fallback"
    backup_chat_id: int = 0
    port: int = 8000
    owner_debug_notifications: bool = False
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "hr_moderation_bot"
    webhook_url: str = ""

    @classmethod
    def from_env(cls) -> "SentriXConfig":
        return cls(
            bot_token=os.getenv("BOT_TOKEN", ""),
            api_id=int(os.getenv("API_ID", "0")),
            api_hash=os.getenv("API_HASH", ""),
            owner_id=int(os.getenv("OWNER_ID", "0")),
            admin_ids=frozenset(
                int(value.strip())
                for value in os.getenv("ADMIN_IDS", "").split(",")
                if value.strip().lstrip("-").isdigit()
            ),
            bot_username=os.getenv("SENTRIX_BOT_USERNAME", "HR_sentrix_bot").lstrip("@"),
            log_group_id=int(os.getenv("LOG_GROUP_ID", "0")),
            support_url=os.getenv("SENTRIX_SUPPORT_URL", "https://t.me/sentrix_updates"),
            updates_url=os.getenv("SENTRIX_UPDATES_URL", "https://t.me/sentrix_updates"),
            storage_path=os.getenv("STORAGE_PATH", "/data/modbot"),
            fallback_storage_path=os.getenv("FALLBACK_STORAGE_PATH", "/tmp/modbot_fallback"),
            backup_chat_id=int(os.getenv("BACKUP_CHAT_ID", "0")),
            port=int(os.getenv("PORT", "8000")),
            owner_debug_notifications=os.getenv("OWNER_DEBUG_NOTIFICATIONS", "0") == "1",
            mongodb_uri=os.getenv("MONGODB_URI", "mongodb://localhost:27017"),
            mongodb_db_name=os.getenv("MONGODB_DB_NAME", "hr_moderation_bot"),
            webhook_url=os.getenv("WEBHOOK_URL") or os.getenv("APP_URL", ""),
        )

    def validate(self) -> list[str]:
        errors = []
        if not self.bot_token:
            errors.append("BOT_TOKEN not set")
        if not self.api_hash:
            errors.append("API_HASH not set")
        if self.api_id <= 0:
            errors.append("API_ID not set")
        if self.owner_id <= 0:
            errors.append("OWNER_ID not set")
        return errors


@lru_cache(maxsize=1)
def get_config() -> SentriXConfig:
    """Return the process-wide configuration loaded from environment variables."""
    return SentriXConfig.from_env()
