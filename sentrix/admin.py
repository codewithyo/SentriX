"""Administrator and owner command contract."""

from .context import FeatureContext, FeatureResult


class AdminFeature:
    commands = frozenset({"promote", "demote", "adminlist", "protect", "unprotect"})

    async def handle(self, command: str, args: list[str], context: FeatureContext) -> FeatureResult:
        if not await context.permissions.require(context.chat_id, context.user_id, "admin"):
            return FeatureResult(True, "❌ Administrator permission required.")
        return FeatureResult(True, f"ℹ️ SentriX admin action queued: `/{command}`.")
