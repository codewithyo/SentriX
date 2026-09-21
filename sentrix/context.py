"""Dependency-injection contracts shared by all SentriX modules."""

from dataclasses import dataclass, field
from typing import Any, Protocol

from .config import SentriXConfig
from .database import AsyncStore


class TelegramGateway(Protocol):
    async def send(self, chat_id: int, text: str, **kwargs: Any) -> dict: ...
    async def edit(self, chat_id: int, message_id: int, text: str, **kwargs: Any) -> dict: ...
    async def delete(self, chat_id: int, message_id: int) -> dict: ...


class PermissionService(Protocol):
    async def is_owner(self, user_id: int) -> bool: ...
    async def is_admin(self, chat_id: int, user_id: int) -> bool: ...
    async def require(self, chat_id: int, user_id: int, permission: str) -> bool: ...


@dataclass(slots=True)
class FeatureResult:
    handled: bool = False
    text: str | None = None
    markup: dict | None = None


@dataclass(slots=True)
class FeatureContext:
    config: SentriXConfig
    store: AsyncStore
    telegram: TelegramGateway
    permissions: PermissionService
    update: dict = field(default_factory=dict)

    @property
    def message(self) -> dict:
        return self.update.get("message", self.update)

    @property
    def chat_id(self) -> int:
        return int(self.message.get("chat", {}).get("id", 0))

    @property
    def user_id(self) -> int:
        return int((self.message.get("from") or {}).get("id", 0))
