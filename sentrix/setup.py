"""Interactive first-run group setup wizard."""

from .context import FeatureContext, FeatureResult


STEPS = ("Welcome", "Rules", "Verification", "Anti-Spam", "Filters", "Logging", "Locks")


def setup_markup() -> dict:
    return {"inline_keyboard": [[{"text": "Continue ➜", "callback_data": "sxsetup_continue"}]]}


class SetupFeature:
    commands = frozenset({"setup", "reset", "language"})

    async def handle(self, command: str, args: list[str], context: FeatureContext) -> FeatureResult:
        if not await context.permissions.require(context.chat_id, context.user_id, "setup"):
            return FeatureResult(True, "❌ Administrator permission required.")
        key = f"setup:{context.chat_id}"
        state = await context.store.get(key, {})
        if command == "reset":
            await context.store.set(key, {})
            return FeatureResult(True, "♻️ SentriX group setup has been reset.")
        if command == "language":
            if not args:
                return FeatureResult(True, f"🌐 Current language: `{state.get('language', 'en')}`")
            state["language"] = args[0].lower()
            await context.store.set(key, state)
            return FeatureResult(True, f"✅ Language set to `{args[0].lower()}`.")
        return FeatureResult(
            True,
            "🛡️ **SentriX Setup**\n\n" + "\n".join(f"{index + 1}️⃣ {step}" for index, step in enumerate(STEPS)),
            setup_markup(),
        )
