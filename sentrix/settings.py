"""Per-group settings service and command surface."""

from .context import FeatureContext, FeatureResult


def settings_markup() -> dict:
    return {
        "inline_keyboard": [
            [{"text": "🛡️ Moderation", "callback_data": "settings_moderation"}, {"text": "🚫 Anti-Spam", "callback_data": "settings_antispam"}],
            [{"text": "🔗 Link Protection", "callback_data": "settings_links"}, {"text": "👋 Welcome", "callback_data": "settings_welcome"}],
            [{"text": "🔐 Verification", "callback_data": "settings_verification"}, {"text": "🔒 Locks", "callback_data": "settings_locks"}],
            [{"text": "📝 Filters", "callback_data": "settings_filters"}, {"text": "📊 Statistics", "callback_data": "settings_statistics"}],
            [{"text": "📢 Logging", "callback_data": "settings_logging"}],
        ]
    }


def settings_text() -> str:
    return (
        "⚙️ **SentriX Settings**\n\n"
        "Choose a category below to configure this group.\n"
        "Changes are restricted to Telegram administrators and are logged."
    )


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
            return FeatureResult(True, settings_text(), settings_markup())
        if len(args) < 2:
            return FeatureResult(True, "Usage: `/setsetting <name> <value>`")
        values[args[0].lower()] = " ".join(args[1:])
        await context.store.set(key, values)
        return FeatureResult(True, f"✅ Setting `{args[0].lower()}` saved.")
