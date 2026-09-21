"""Centralized SentriX and Telegram permission checks."""

from collections.abc import Awaitable, Callable
from typing import Any


MemberFetcher = Callable[[int, int], Awaitable[tuple[dict | None, str | None]]]
AuthLoader = Callable[[], dict]


class PermissionService:
    """Single authority for owner, Telegram admin, and SentriX moderator checks."""

    ADMIN_STATUSES = {"creator", "administrator"}

    def __init__(
        self,
        owner_id: int,
        member_fetcher: MemberFetcher,
        auth_loader: AuthLoader,
        admin_ids: frozenset[int] = frozenset(),
    ):
        self.owner_id = int(owner_id)
        self.admin_ids = frozenset(int(user_id) for user_id in admin_ids)
        self._member_fetcher = member_fetcher
        self._auth_loader = auth_loader

    def is_owner(self, user_id: int) -> bool:
        """Return true for the configured owner or full-access SentriX admins."""
        return int(user_id) == self.owner_id or int(user_id) in self.admin_ids

    async def is_group_owner(self, chat_id: int, user_id: int) -> bool:
        member, error = await self._member_fetcher(int(chat_id), int(user_id))
        return not error and bool(member and member.get("status") == "creator")

    async def is_admin(self, chat_id: int, user_id: int) -> bool:
        member, error = await self._member_fetcher(int(chat_id), int(user_id))
        return not error and bool(member and member.get("status") in self.ADMIN_STATUSES)

    def is_sentrix_admin(self, user_id: int) -> bool:
        if self.is_owner(user_id):
            return True
        return str(user_id) in self._auth_loader()

    def has_permission(self, user_id: int, permission: str) -> bool:
        if self.is_owner(user_id):
            return True
        record = self._auth_loader().get(str(user_id), {})
        return bool(record.get("permissions", {}).get(permission, False))

    def is_frozen(self, user_id: int) -> bool:
        if self.is_owner(user_id):
            return False
        return bool(self._auth_loader().get(str(user_id), {}).get("frozen", False))

    async def can_manage(self, chat_id: int, user_id: int, permission: str | None = None) -> bool:
        """Return true for the owner, Telegram admins, or authorized SentriX admins."""
        if self.is_owner(user_id) or await self.is_admin(chat_id, user_id):
            return True
        if not self.is_sentrix_admin(user_id) or self.is_frozen(user_id):
            return False
        return permission is None or self.has_permission(user_id, permission)
