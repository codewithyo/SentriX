"""Administrator and owner command contract."""

from .context import FeatureContext, FeatureResult


class AdminFeature:
    commands = frozenset({"admins", "setadmin", "removeadmin", "promote", "demote", "adminlist", "protect", "unprotect"})

    async def handle(self, command: str, args: list[str], context: FeatureContext) -> FeatureResult:
        key = f"sentrix_admins:{context.chat_id}"
        admins = await context.store.get(key, {})
        if not isinstance(admins, dict):
            admins = {}
        if command == "admins":
            if not admins:
                return FeatureResult(True, "👑 No SentriX-specific admins configured.")
            lines = ["👑 **SentriX Admins**", "", "These admins have SentriX permissions without Telegram admin privileges."]
            lines.extend(f"• `{user_id}` · {data.get('role', 'moderator')}" for user_id, data in sorted(admins.items()))
            return FeatureResult(True, "\n".join(lines))
        if command in {"setadmin", "removeadmin"}:
            if not await context.permissions.is_owner(context.user_id):
                return FeatureResult(True, "❌ Only the bot owner can manage SentriX admins.")
            if not args or not args[0].lstrip("-").isdigit():
                return FeatureResult(True, f"Usage: `/{command} <user_id>`")
            target_id = str(int(args[0]))
            if command == "setadmin":
                admins[target_id] = {"role": "moderator", "added_by": context.user_id}
                message = f"✅ `{target_id}` is now a SentriX admin. Telegram admin privileges were not changed."
            else:
                if target_id not in admins:
                    return FeatureResult(True, "❌ That user is not a SentriX admin.")
                admins.pop(target_id)
                message = f"✅ SentriX admin access removed from `{target_id}`."
            await context.store.set(key, admins)
            return FeatureResult(True, message)
        if not await context.permissions.require(context.chat_id, context.user_id, "admin"):
            return FeatureResult(True, "❌ Administrator permission required.")
        return FeatureResult(True, f"ℹ️ SentriX admin action queued: `/{command}`.")
