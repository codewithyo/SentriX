"""Welcome and goodbye message configuration."""

from .context import FeatureContext, FeatureResult
from .utils import render_template


class WelcomeFeature:
    commands = frozenset({"setwelcome", "setgoodbye", "welcome", "goodbye"})

    async def handle(self, command: str, args: list[str], context: FeatureContext) -> FeatureResult:
        if not await context.permissions.require(context.chat_id, context.user_id, "welcome"):
            return FeatureResult(True, "❌ Administrator permission required.")
        key = f"welcome:{context.chat_id}"
        values = await context.store.get(key, {})
        if not isinstance(values, dict):
            values = {}
        field = "goodbye" if command in {"setgoodbye", "goodbye"} else "welcome"
        if command in {"welcome", "goodbye"} and not args:
            return FeatureResult(True, values.get(field, {}).get("text", f"No {field} message configured."))
        if not args:
            return FeatureResult(True, f"Usage: `/{command} <text>`")
        values[field] = {"text": " ".join(args), "enabled": True, "created_by": context.user_id}
        await context.store.set(key, values)
        return FeatureResult(True, f"✅ {field.title()} message saved. Preview:\n{render_template(' '.join(args), {'id': context.user_id, 'first_name': 'User'})}")
