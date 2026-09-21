"""Per-group content lock configuration."""

from .context import FeatureContext, FeatureResult


class LocksFeature:
    commands = frozenset({"lock", "unlock", "locks"})

    async def handle(self, command: str, args: list[str], context: FeatureContext) -> FeatureResult:
        if not await context.permissions.require(context.chat_id, context.user_id, "locks"):
            return FeatureResult(True, "❌ Administrator permission required.")
        key = f"locks:{context.chat_id}"
        locks = await context.store.get(key, [])
        locks = list(locks) if isinstance(locks, list) else []
        if command == "locks":
            return FeatureResult(True, "🔒 No active locks." if not locks else "🔒 Active locks: " + ", ".join(f"`{item}`" for item in locks))
        if not args:
            return FeatureResult(True, f"Usage: `/{command} <type>`")
        lock_type = args[0].lower()
        if command == "lock" and lock_type not in locks:
            locks.append(lock_type)
        if command == "unlock":
            locks = [item for item in locks if item != lock_type]
        await context.store.set(key, locks)
        return FeatureResult(True, f"✅ `{lock_type}` {'locked' if command == 'lock' else 'unlocked'}.")
