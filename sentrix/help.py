"""Rose-style category help for SentriX."""

from .context import FeatureContext, FeatureResult


CATEGORIES = {
    "admin": ("👮 Admin", "/promote, /demote, /ban, /unban, /kick, /mute, /unmute, /warn, /unwarn, /warnings, /purge"),
    "protection": ("🛡️ Protection", "/antispam, /antiraid, /captcha, /lock, /unlock, /setflood"),
    "welcome": ("👋 Welcome", "/welcome, /setwelcome, /goodbye, /setgoodbye"),
    "filters": ("📝 Filters", "/filter, /filters, /stop, /stopall"),
    "notes": ("📚 Notes", "/save, /get, /notes, /clear"),
    "logging": ("📢 Logging", "/setlog, /unsetlog, /logchannel, /logsettings"),
    "setup": ("⚙️ Setup", "/setup, /settings, /rules, /setrules, /reset, /language"),
    "info": ("📊 Info", "/id, /info, /admins, /stats, /report"),
}


def help_markup() -> dict:
    keys = list(CATEGORIES)
    rows = [[{"text": CATEGORIES[keys[index]][0], "callback_data": f"sxhelp_{keys[index]}"} for index in range(start, min(start + 2, len(keys)))] for start in range(0, len(keys), 2)]
    return {"inline_keyboard": rows}


def help_text() -> str:
    return "🛡️ **SentriX Help**\n\nChoose a category:\n\n" + "\n".join(f"• {title}" for title, _ in CATEGORIES.values())


class HelpFeature:
    commands = frozenset({"help", "about", "ping"})

    async def handle(self, command: str, args: list[str], context: FeatureContext) -> FeatureResult:
        if command == "about":
            return FeatureResult(True, "🛡️ **SentriX**\n\nFast, secure, customizable Telegram group protection and management.")
        if command == "ping":
            return FeatureResult(True, "🏓 SentriX is online.")
        return FeatureResult(True, help_text(), help_markup())


def category_text(category: str) -> str | None:
    entry = CATEGORIES.get(category)
    if not entry:
        return None
    title, commands = entry
    return f"🛡️ **{title}**\n\n{commands}\n\nUse `/help` to return to categories."
