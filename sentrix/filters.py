"""Keyword filter service."""

from .context import FeatureContext, FeatureResult


class FiltersFeature:
    commands = frozenset({"filter", "filters", "stop", "stopall"})

    async def handle(self, command: str, args: list[str], context: FeatureContext) -> FeatureResult:
        key = f"filters:{context.chat_id}"
        filters = await context.store.get(key, {})
        if not isinstance(filters, dict):
            filters = {}
        if command == "filters":
            return FeatureResult(True, "🔍 No filters active." if not filters else "🔍 **Filters**\n\n" + "\n".join(f"• `{name}`" for name in sorted(filters)))
        if not await context.permissions.require(context.chat_id, context.user_id, "filters"):
            return FeatureResult(True, "❌ Administrator permission required.")
        if command == "stopall":
            filters.clear()
        elif command == "stop":
            if not args:
                return FeatureResult(True, "Usage: `/stop <keyword>`")
            filters.pop(args[0].lower(), None)
        else:
            if len(args) < 2:
                return FeatureResult(True, "Usage: `/filter <keyword> <response>`")
            filters[args[0].lower()] = {"response": " ".join(args[1:]), "created_by": context.user_id}
        await context.store.set(key, filters)
        return FeatureResult(True, "✅ Filter configuration updated.")
