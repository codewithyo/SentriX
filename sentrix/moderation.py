"""Moderation command contract for the SentriX dispatcher."""

from .context import FeatureContext, FeatureResult


class ModerationFeature:
    commands = frozenset({"ban", "unban", "mute", "unmute", "kick", "warn", "unwarn", "warnings", "purge"})

    async def handle(self, command: str, args: list[str], context: FeatureContext) -> FeatureResult:
        permission = "delete" if command == "purge" else "warn" if command in {"warn", "unwarn", "warnings"} else command
        if not await context.permissions.require(context.chat_id, context.user_id, permission):
            return FeatureResult(True, "❌ You do not have permission to use this command.")
        return FeatureResult(True, f"ℹ️ SentriX moderation action queued: `/{command}`.")
