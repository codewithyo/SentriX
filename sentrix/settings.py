"""Per-group settings service and command surface."""

from .context import FeatureContext, FeatureResult


class SettingsFeature:
    commands = frozenset({"settings", "setsetting"})

    async def handle(self, command: str, args: list[str], context: FeatureContext) -> FeatureResult:
        if not await context.permissions.require(context.chat_id, context.user_id, "settings"):
            return FeatureResult(True, "❌ Administrator permission required.")
        key = f"settings:{context.chat_id}"
        values = await context.store.get(key, {})
        if not isinstance(values, dict):
            values = {}
        if command == "settings":
            if not values:
                return FeatureResult(True, "⚙️ No custom settings configured.")
            return FeatureResult(True, "⚙️ **SentriX Settings**\n\n" + "\n".join(f"• `{k}`: `{v}`" for k, v in sorted(values.items())))
        if len(args) < 2:
            return FeatureResult(True, "Usage: `/setsetting <name> <value>`")
        values[args[0].lower()] = " ".join(args[1:])
        await context.store.set(key, values)
        return FeatureResult(True, f"✅ Setting `{args[0].lower()}` saved.")
