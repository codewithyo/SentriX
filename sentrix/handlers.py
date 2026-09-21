"""Small handler facade for integrations that prefer explicit entrypoints."""

from .context import FeatureContext, FeatureResult
from .registry import FeatureRegistry


async def handle_command(registry: FeatureRegistry, command: str, args: list[str], context: FeatureContext) -> FeatureResult:
    return await registry.dispatch(command, args, context)
