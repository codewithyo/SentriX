"""Centralized SentriX and Telegram permission checks."""

from collections.abc import Awaitable, Callable
from typing import Any


MemberFetcher = Callable[[int, int], Awaitable[tuple[dict | None, str | None]]]
AuthLoader = Callable[[], dict]
GroupGrantLoader = Callable[[int], dict]


PERMISSION_GROUPS = {
    "ban": frozenset({"ban", "unban", "tban"}),
    "mute": frozenset({"mute", "unmute", "tmute"}),
    "warn": frozenset({"warn", "unwarn", "warnings", "warns", "resetwarns"}),
    "delete": frozenset({"del", "purge"}),
    "pin": frozenset({"pin", "unpin"}),
    "kick": frozenset({"kick"}),
    "lock": frozenset({"lock", "unlock", "locktype", "locktypes", "locktypelist", "locklist", "lockbot", "locklink", "unlockbot", "unlocklink"}),
    "filter": frozenset({"filter", "filters", "stop", "stopall"}),
    "welcome": frozenset({"welcome", "setwelcome", "goodbye", "setgoodbye"}),
    "logging": frozenset({"setlog", "logchannel", "unsetlog", "logsettings"}),
    "protection": frozenset({"antispam", "antiraid", "captcha", "setflood"}),
    "settings": frozenset({"settings", "setup"}),
}
ALL_GROUP = "all"
GROUP_LABELS = {
    "ban": "🔨 Ban",
    "mute": "🔇 Mute",
    "warn": "⚠️ Warn",
    "delete": "🧹 Delete",
    "pin": "📌 Pin",
    "kick": "👢 Kick",
    "lock": "🔒 Lock",
    "filter": "📝 Filter",
    "welcome": "👋 Welcome",
    "logging": "📢 Logging",
    "protection": "🛡️ Protection",
    "settings": "⚙️ Settings",
    "all": "👑 All",
}


def grant_manager_markup(chat_id: int, user_id: int) -> dict:
    groups = tuple(PERMISSION_GROUPS) + (ALL_GROUP,)
    rows = []
    for index in range(0, len(groups), 3):
        rows.append([
            {"text": GROUP_LABELS[group], "callback_data": f"sxgrant_{chat_id}_{user_id}_{group}"}
            for group in groups[index:index + 3]
        ])
    rows.append([
        {"text": "✖️ Close", "callback_data": "sxgrant_close"},
    ])
    return {"inline_keyboard": rows}


def permission_group_for(command: str) -> str | None:
    command = command.lstrip("/").lower()
    return next((group for group, commands in PERMISSION_GROUPS.items() if command in commands), None)


class PermissionService:
    """Single authority for owner, Telegram admin, and SentriX moderator checks."""

    ADMIN_STATUSES = {"creator", "administrator"}

    def __init__(
        self,
        owner_id: int,
        member_fetcher: MemberFetcher,
        auth_loader: AuthLoader,
        admin_ids: frozenset[int] = frozenset(),
        group_grant_loader: GroupGrantLoader | None = None,
    ):
        self.owner_id = int(owner_id)
        self.admin_ids = frozenset(int(user_id) for user_id in admin_ids)
        self._member_fetcher = member_fetcher
        self._auth_loader = auth_loader
        self._group_grant_loader = group_grant_loader or (lambda chat_id: {})

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

    def granted_groups(self, chat_id: int, user_id: int) -> frozenset[str]:
        grants = self._group_grant_loader(int(chat_id))
        value = grants.get(str(user_id), []) if isinstance(grants, dict) else []
        return frozenset(value) if isinstance(value, (list, tuple, set, frozenset)) else frozenset()

    def has_group(self, chat_id: int, user_id: int, group: str) -> bool:
        if self.is_owner(user_id) or self.is_sentrix_admin(user_id):
            return True
        groups = self.granted_groups(chat_id, user_id)
        return ALL_GROUP in groups or group in groups

    async def can_manage(self, chat_id: int, user_id: int, permission: str | None = None) -> bool:
        """Return true for the owner, Telegram admins, or authorized SentriX admins."""
        if self.is_owner(user_id) or await self.is_admin(chat_id, user_id):
            return True
        if self.is_sentrix_admin(user_id) and not self.is_frozen(user_id):
            return True
        if self.is_frozen(user_id):
            return False
        if permission is None:
            return False
        return self.has_group(chat_id, user_id, permission_group_for(permission) or permission)

    async def can_grant(self, chat_id: int, user_id: int) -> bool:
        """Grant authority: group owner, global admin, or group `all` grant."""
        if self.is_owner(user_id) or self.is_sentrix_admin(user_id):
            return not self.is_frozen(user_id)
        if await self.is_group_owner(chat_id, user_id):
            return True
        return self.has_group(chat_id, user_id, ALL_GROUP)
