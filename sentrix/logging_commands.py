"""Telegram command surface for the dedicated SentriX log channel."""

from .context import FeatureContext, FeatureResult


class LoggingFeature:
    commands = frozenset({"setlog", "unsetlog", "logchannel", "logsettings"})

    async def handle(self, command: str, args: list[str], context: FeatureContext) -> FeatureResult:
        if not await context.permissions.require(context.chat_id, context.user_id, "logging"):
            return FeatureResult(True, "❌ Administrator permission required.")
        key = f"logging:{context.chat_id}"
        settings = await context.store.get(key, {})
        if not isinstance(settings, dict):
            settings = {}
        if command == "logchannel":
            channel = settings.get("channel_id")
            return FeatureResult(True, f"📢 Log channel: `{channel}`" if channel else "📢 No log channel configured.")
        if command == "logsettings":
            enabled = settings.get("enabled_events", ["all"])
            return FeatureResult(True, "📢 **Log Settings**\n\nEvents: " + ", ".join(enabled))
        if command == "unsetlog":
            await context.store.set(key, {})
            return FeatureResult(True, "✅ Dedicated log channel removed.")
        channel_id = None
        if args and args[0].lstrip("-").isdigit():
            channel_id = int(args[0])
        elif context.message.get("forward_from_chat", {}).get("id"):
            channel_id = context.message["forward_from_chat"]["id"]
        if not channel_id:
            return FeatureResult(True, "Usage: `/setlog <channel_id>` or forward a message from the desired channel.")
        await context.store.set(key, {"channel_id": channel_id, "enabled_events": ["all"]})
        return FeatureResult(True, f"✅ Log channel configured: `{channel_id}`")
