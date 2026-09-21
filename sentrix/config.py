"""Typed, environment-backed configuration for SentriX."""

from dataclasses import dataclass
import os


@dataclass(frozen=True, slots=True)
class SentriXConfig:
    bot_token: str
    api_id: int
    api_hash: str
    owner_id: int
    bot_username: str = "sentrix_bot"
    log_group_id: int = 0
    support_url: str = "https://t.me/sentrix_support"
    updates_url: str = "https://t.me/sentrix_updates"
    storage_path: str = "/data/modbot"

    @classmethod
    def from_env(cls) -> "SentriXConfig":
        return cls(
            bot_token=os.getenv("BOT_TOKEN", ""),
            api_id=int(os.getenv("API_ID", "0")),
            api_hash=os.getenv("API_HASH", ""),
            owner_id=int(os.getenv("OWNER_ID", "0")),
            bot_username=os.getenv("SENTRIX_BOT_USERNAME", "sentrix_bot").lstrip("@"),
            log_group_id=int(os.getenv("LOG_GROUP_ID", "0")),
            support_url=os.getenv("SENTRIX_SUPPORT_URL", "https://t.me/sentrix_support"),
            updates_url=os.getenv("SENTRIX_UPDATES_URL", "https://t.me/sentrix_updates"),
            storage_path=os.getenv("STORAGE_PATH", "/data/modbot"),
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
