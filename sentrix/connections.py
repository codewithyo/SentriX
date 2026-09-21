"""Connection command surface for PM-to-group management."""

from .context import FeatureContext, FeatureResult


class ConnectionsFeature:
    commands = frozenset({"connection"})

    async def handle(self, command: str, args: list[str], context: FeatureContext) -> FeatureResult:
        return FeatureResult(True, "🔗 Use `/connections` to view connected groups and `/connect <chat_id>` to add one.")
