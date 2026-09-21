"""SentriX public welcome screen and feature discovery."""

from .context import FeatureContext, FeatureResult


class StartFeature:
    commands = frozenset({"start", "features"})

    def _markup(self, context: FeatureContext) -> dict:
        return {
            "inline_keyboard": [
                [{"text": "➕ Add to Group", "url": f"https://t.me/{context.config.bot_username}?startgroup=true"}],
                [{"text": "📚 Help & Commands", "callback_data": "start_help"}, {"text": "🛡️ Features", "callback_data": "start_features"}],
                [{"text": "📢 Updates", "url": context.config.updates_url}, {"text": "💬 Support", "url": context.config.support_url}],
            ]
        }

    async def handle(self, command: str, args: list[str], context: FeatureContext) -> FeatureResult:
        if command == "features":
            return FeatureResult(True, self.features_text())
        return FeatureResult(
            True,
            "🛡️ **Welcome to SentriX**\n\n"
            "Your all-in-one Telegram group management & protection bot.\n\n"
            "Keep your community **safe, clean and automated** with powerful moderation tools.\n\n"
            "⚡ Fast • Secure • Customizable",
            self._markup(context),
        )

    @staticmethod
    def features_text() -> str:
        return (
            "🛡️ **SentriX Features**\n\n"
            "• Moderation: ban, mute, kick, warn, purge and admin tools\n"
            "• Protection: anti-spam, repeat and link controls\n"
            "• Filters: custom keyword replies\n"
            "• Welcome: greetings, goodbye messages and verification\n"
            "• Locks: links, media, stickers, GIFs and polls\n"
            "• AutoMod: delete → warn → mute → ban actions\n"
            "• Notes and custom commands for reusable group information"
        )
