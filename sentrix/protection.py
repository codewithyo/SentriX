"""Protection settings command surface."""

from .context import FeatureContext, FeatureResult


class ProtectionFeature:
    commands = frozenset({"antispam", "antiraid", "setflood"})

    async def handle(self, command: str, args: list[str], context: FeatureContext) -> FeatureResult:
        if not await context.permissions.require(context.chat_id, context.user_id, "protection"):
            return FeatureResult(True, "❌ Administrator permission required.")
        key = f"protection:{context.chat_id}"
        settings = await context.store.get(key, {})
        if not isinstance(settings, dict):
            settings = {}
        if command == "setflood":
            if not args or not args[0].isdigit() or int(args[0]) < 2:
                return FeatureResult(True, "Usage: `/setflood <messages> [seconds]`")
            settings["flood_limit"] = int(args[0])
            settings["flood_window"] = int(args[1]) if len(args) > 1 and args[1].isdigit() else 3
        else:
            settings[command] = args[0].lower() in {"on", "enable", "yes"} if args else not settings.get(command, False)
        await context.store.set(key, settings)
        status = "on" if settings.get(command, False) else "off"
        return FeatureResult(True, f"✅ `{command}` is now **{status}**.")
