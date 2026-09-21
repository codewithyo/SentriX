"""Persistent group notes feature."""

from .context import FeatureContext, FeatureResult


class NotesFeature:
    commands = frozenset({"save", "get", "notes", "clear"})

    async def handle(self, command: str, args: list[str], context: FeatureContext) -> FeatureResult:
        key = f"notes:{context.chat_id}"
        notes = await context.store.get(key, {})
        if not isinstance(notes, dict):
            notes = {}
        if command == "notes":
            names = sorted(notes)
            return FeatureResult(True, "📋 No notes saved." if not names else "📋 **Notes**\n\n" + "\n".join(f"• `#{name}`" for name in names))
        if not args:
            return FeatureResult(True, f"Usage: `/{command} <name> [text]`")
        name = args[0].lower()
        if command == "get":
            return FeatureResult(True, notes.get(name, {}).get("content", f"❌ Note `{name}` not found."))
        if not await context.permissions.require(context.chat_id, context.user_id, "notes"):
            return FeatureResult(True, "❌ Administrator permission required.")
        if command == "clear":
            notes.pop(name, None)
        else:
            if len(args) < 2:
                return FeatureResult(True, "Usage: `/save <name> <text>`")
            notes[name] = {"content": " ".join(args[1:]), "created_by": context.user_id}
        await context.store.set(key, notes)
        return FeatureResult(True, f"✅ Note `{name}` updated.")
