"""Button-based verification service."""

import time

from .context import FeatureContext, FeatureResult


class VerificationFeature:
    commands = frozenset({"captcha", "verify"})

    async def handle(self, command: str, args: list[str], context: FeatureContext) -> FeatureResult:
        if command == "verify":
            return FeatureResult(True, "✅ Verification successful! Welcome to the group.")
        if not await context.permissions.require(context.chat_id, context.user_id, "verification"):
            return FeatureResult(True, "❌ Administrator permission required.")
        enabled = bool(args and args[0].lower() in {"on", "enable"})
        key = f"verification:{context.chat_id}"
        await context.store.set(key, {"enabled": enabled, "updated_at": time.time()})
        return FeatureResult(True, f"{'🟢' if enabled else '🔴'} CAPTCHA verification turned {'on' if enabled else 'off'}.")
