"""Information command surface."""

from .context import FeatureContext, FeatureResult


class InformationFeature:
    commands = frozenset({"info"})

    async def handle(self, command: str, args: list[str], context: FeatureContext) -> FeatureResult:
        return FeatureResult(True, f"📊 **SentriX Information**\n\nChat ID: `{context.chat_id}`\nYour ID: `{context.user_id}`")
