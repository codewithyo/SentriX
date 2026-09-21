"""Rose-style interactive Help Center for SentriX."""

from dataclasses import dataclass

from .context import FeatureContext, FeatureResult


@dataclass(frozen=True, slots=True)
class CommandGuide:
    name: str
    description: str
    syntax: str
    example: str
    permissions: str
    notes: str
    related: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class HelpCategory:
    key: str
    title: str
    description: str
    commands: tuple[str, ...]


GUIDES = {
    "start": CommandGuide("/start", "Open the SentriX welcome screen.", "/start", "/start", "Everyone", "Works in private chats and groups.", ("/help", "/about")),
    "help": CommandGuide("/help", "Open this category-based Help Center.", "/help", "/help", "Everyone", "Use buttons to browse without sending another message.", ("/about", "/settings")),
    "about": CommandGuide("/about", "Learn what SentriX provides.", "/about", "/about", "Everyone", "A concise bot overview.", ("/help", "/ping")),
    "ping": CommandGuide("/ping", "Check whether SentriX is online.", "/ping", "/ping", "Everyone", "Returns a lightweight health response.", ("/about",)),
    "settings": CommandGuide("/settings", "Open the inline dashboard for the current group.", "/settings", "/settings", "Group administrators", "Settings changes are audited when a log channel is configured.", ("/setup", "/logsettings")),
    "setup": CommandGuide("/setup", "Start the interactive group setup wizard.", "/setup", "/setup", "Group administrators", "Configure welcome, rules, verification, anti-spam, filters, logging, and locks.", ("/settings", "/reset")),
    "ban": CommandGuide("/ban", "Remove a user from the group.", "/ban <user> [duration] [reason]", "/ban @spammer 7d Spam", "Moderators with ban permission", "Reply to a message or provide a user ID/@username.", ("/unban", "/warn")),
    "unban": CommandGuide("/unban", "Lift a user ban.", "/unban <user>", "/unban @member", "Moderators with unban permission", "Temporary-ban records are cancelled when manually unbanned.", ("/ban",)),
    "kick": CommandGuide("/kick", "Remove a user without a permanent ban.", "/kick <user> [reason]", "/kick @spammer Flooding", "Moderators with kick permission", "Admins and protected users cannot be kicked.", ("/ban", "/mute")),
    "mute": CommandGuide("/mute", "Restrict a user from speaking.", "/mute <user> [duration] [reason]", "/mute @member 2h Off-topic", "Moderators with mute permission", "Use a duration such as 30m, 2h, or 1d for a temporary mute.", ("/unmute", "/setflood")),
    "unmute": CommandGuide("/unmute", "Remove a speaking restriction.", "/unmute <user>", "/unmute @member", "Moderators with unmute permission", "Replying to a member is supported.", ("/mute",)),
    "warn": CommandGuide("/warn", "Issue a warning and apply the configured threshold action.", "/warn <user> [reason]", "/warn @member Advertising", "Moderators with warn permission", "Warning thresholds are configured with /warnmode.", ("/unwarn", "/warnings", "/warnmode")),
    "unwarn": CommandGuide("/unwarn", "Reset warnings for a user.", "/unwarn <user>", "/unwarn @member", "Moderators with warn permission", "This resets the group warning count.", ("/warn", "/warnings")),
    "warnings": CommandGuide("/warnings", "View a user's warning count.", "/warnings [user]", "/warnings @member", "Everyone; group details may require access", "Reply to a user's message or omit the target for your own count.", ("/warn", "/unwarn")),
    "purge": CommandGuide("/purge", "Delete a bounded range of messages.", "/purge [count]", "Reply to the first message, then /purge 25", "Moderators with delete permission", "The count is limited to protect Telegram API limits.", ("/del",)),
    "del": CommandGuide("/del", "Delete a replied message.", "/del", "Reply to a message, then /del", "Moderators with delete permission", "Protected users and messages cannot be removed through moderation.", ("/purge",)),
    "antispam": CommandGuide("/antispam", "Toggle automatic spam protection.", "/antispam on|off", "/antispam on", "Group administrators", "Detects flooding, repeated messages, links, mentions, and excessive emoji.", ("/setflood", "/antiraid")),
    "antiraid": CommandGuide("/antiraid", "Toggle raid-oriented protection rules.", "/antiraid on|off", "/antiraid on", "Group administrators", "Combine with verification for new-member protection.", ("/captcha", "/antispam")),
    "captcha": CommandGuide("/captcha", "Require new members to verify themselves.", "/captcha on|off", "/captcha on", "Group administrators", "New members receive an inline Verify Yourself button.", ("/welcome", "/antiraid")),
    "lock": CommandGuide("/lock", "Restrict a content type.", "/lock <type>", "/lock links", "Moderators with mute permission", "Supported types include links, media, stickers, GIFs, polls, and all.", ("/unlock", "/locktypes")),
    "unlock": CommandGuide("/unlock", "Remove a content lock.", "/unlock <type>", "/unlock links", "Moderators with mute permission", "Use /locklist to inspect active locks.", ("/lock",)),
    "setflood": CommandGuide("/setflood", "Configure messages-per-window flood limits.", "/setflood <messages> [seconds]", "/setflood 5 3", "Group administrators", "The default window is three seconds.", ("/antispam",)),
    "welcome": CommandGuide("/welcome", "Show the current welcome message.", "/welcome", "/welcome", "Everyone", "Use /setwelcome to change it.", ("/setwelcome", "/goodbye")),
    "setwelcome": CommandGuide("/setwelcome", "Save a new member welcome message.", "/setwelcome <text>", "/setwelcome Welcome {first}!", "Group administrators", "Variables include {first}, {last}, {username}, {id}, and {chat}.", ("/welcome", "/captcha")),
    "goodbye": CommandGuide("/goodbye", "Show the current goodbye message.", "/goodbye", "/goodbye", "Everyone", "Use /setgoodbye to change it.", ("/setgoodbye",)),
    "setgoodbye": CommandGuide("/setgoodbye", "Save a member departure message.", "/setgoodbye <text>", "/setgoodbye Goodbye {first}!", "Group administrators", "The same member variables as welcome messages are supported.", ("/goodbye",)),
    "filter": CommandGuide("/filter", "Create a keyword auto-response.", "/filter <keyword> <response>", "/filter rules Read #rules", "Group administrators", "Use -exact, -start, or -regex before the keyword for matching modes.", ("/filters", "/stop")),
    "filters": CommandGuide("/filters", "List active keyword filters.", "/filters", "/filters", "Group members", "Filter management requires administrator permission.", ("/filter", "/stopall")),
    "stop": CommandGuide("/stop", "Remove one keyword filter.", "/stop <keyword>", "/stop rules", "Group administrators", "Use /stopall to remove every filter.", ("/filter", "/stopall")),
    "stopall": CommandGuide("/stopall", "Remove every keyword filter.", "/stopall", "/stopall", "Group administrators", "This cannot be undone automatically.", ("/filters",)),
    "save": CommandGuide("/save", "Save reusable group information.", "/save <name> <text>", "/save rules Be respectful", "Group administrators", "Reply to media to save reusable media notes.", ("/get", "/notes")),
    "get": CommandGuide("/get", "Retrieve a saved note.", "/get <name>", "/get rules", "Everyone", "Notes can also be triggered with #name.", ("/save", "/notes")),
    "notes": CommandGuide("/notes", "List saved notes.", "/notes", "/notes", "Everyone", "Tap a note button to retrieve it.", ("/get", "/save")),
    "clear": CommandGuide("/clear", "Delete a saved note.", "/clear <name>", "/clear oldrules", "Group administrators", "Deleting a note removes its hashtag trigger.", ("/notes",)),
    "setlog": CommandGuide("/setlog", "Configure the dedicated admin log channel.", "/setlog <channel_id>", "/setlog -1001234567890", "Group administrators", "You may also forward a channel message and run /setlog.", ("/logchannel", "/unsetlog")),
    "unsetlog": CommandGuide("/unsetlog", "Remove the dedicated log channel.", "/unsetlog", "/unsetlog", "Group administrators", "Future events will not be sent to that channel.", ("/setlog",)),
    "logchannel": CommandGuide("/logchannel", "Show the configured log channel.", "/logchannel", "/logchannel", "Group administrators", "The channel ID is displayed for verification.", ("/setlog", "/logsettings")),
    "logsettings": CommandGuide("/logsettings", "Show enabled logging event types.", "/logsettings", "/logsettings", "Group administrators", "Moderation, filters, joins/leaves, and settings are supported.", ("/setlog",)),
    "rules": CommandGuide("/rules", "Display group rules.", "/rules", "/rules", "Everyone", "Use /setrules to change the text.", ("/setrules",)),
    "setrules": CommandGuide("/setrules", "Save group rules.", "/setrules <text>", "/setrules No spam or harassment.", "Group administrators", "Rules are shown publicly with /rules.", ("/rules",)),
    "reset": CommandGuide("/reset", "Reset modular group setup state.", "/reset", "/reset", "Group administrators", "Legacy moderation data is not deleted by this command.", ("/setup",)),
    "language": CommandGuide("/language", "Set the group language preference.", "/language <code>", "/language en", "Group administrators", "The setting is stored per group.", ("/settings",)),
    "connect": CommandGuide("/connect", "Connect a group for PM management.", "/connect <chat_id>", "/connect -1001234567890", "Authorized moderators", "Use /connection to inspect connection help.", ("/disconnect",)),
    "disconnect": CommandGuide("/disconnect", "Remove a group connection.", "/disconnect [chat_id|all]", "/disconnect all", "Authorized moderators", "Run in the bot private chat.", ("/connect",)),
    "connection": CommandGuide("/connection", "Show connection management help.", "/connection", "/connection", "Everyone", "Use /connections for the current list.", ("/connect", "/disconnect")),
    "connections": CommandGuide("/connections", "List and switch connected groups.", "/connections", "/connections", "Authorized moderators", "Run in the bot private chat.", ("/connect", "/disconnect")),
    "id": CommandGuide("/id", "Show a Telegram user or chat ID.", "/id [user]", "/id me", "Everyone", "Reply to a message or provide a username.", ("/info",)),
    "info": CommandGuide("/info", "Show basic SentriX chat information.", "/info", "/info", "Everyone", "Detailed moderation statistics use /stats.", ("/stats", "/id")),
    "admins": CommandGuide("/admins", "List SentriX-specific admins.", "/admins", "/admins", "Everyone", "SentriX admins do not receive Telegram admin privileges.", ("/adminlist", "/setadmin")),
    "stats": CommandGuide("/stats", "Show moderation statistics.", "/stats", "/stats", "Moderators", "Statistics are scoped to the current group.", ("/info",)),
    "report": CommandGuide("/report", "Report a message to group administrators.", "/report [reason]", "/report suspicious link", "Everyone", "Reply to the message you want to report.", ("/stats",)),
    "promote": CommandGuide("/promote", "Promote a member to Telegram admin.", "/promote <user>", "/promote @moderator", "Group administrators", "This changes Telegram privileges; /setadmin only changes SentriX access.", ("/demote", "/setadmin")),
    "demote": CommandGuide("/demote", "Remove Telegram admin privileges.", "/demote <user>", "/demote @moderator", "Group administrators", "Use carefully; SentriX-specific admin access is separate.", ("/promote", "/removeadmin")),
    "grant": CommandGuide("/grant", "Grant a grouped SentriX permission.", "/grant <user> <group>", "/grant @moderator ban", "Group owner, global admin, or holder of the `all` group", "Groups: ban, mute, warn, delete, pin, kick, lock, filter, welcome, logging, protection, settings, and all. `/grant @user` opens the interactive manager.", ("/revoke", "/grants")),
    "revoke": CommandGuide("/revoke", "Revoke a grouped SentriX permission.", "/revoke <user> <group>", "/revoke @moderator mute", "Group owner, global admin, or holder of the `all` group", "Use `all` to remove the user's group-level grants.", ("/grant", "/grants")),
    "grants": CommandGuide("/grants", "Display granted permission groups.", "/grants [user]", "/grants @moderator", "Everyone for self; grant managers for other users", "Permissions are isolated per group. The `all` group never grants owner/global-admin access.", ("/grant", "/revoke")),
}


_ADDITIONAL_GUIDES = {
    "tban": ("Temporarily ban a user.", "/tban <user> <duration> [reason]"),
    "tmute": ("Temporarily mute a user.", "/tmute <user> <duration> [reason]"),
    "kickme": ("Remove yourself from the group.", "/kickme"),
    "pin": ("Pin a replied message.", "/pin"),
    "unpin": ("Remove the current pinned message.", "/unpin"),
    "auth": ("Authorize a SentriX moderator.", "/auth <user_id>"),
    "unauth": ("Remove SentriX moderator authorization.", "/unauth <user_id>"),
    "grant": ("Open the grouped Permission Grant Manager or grant a group directly.", "/grant <user> <group>"),
    "revoke": ("Revoke a grouped permission from a user.", "/revoke <user> <group>"),
    "grants": ("Show a user's granted permission groups.", "/grants [user]"),
    "freeze": ("Freeze a SentriX moderator.", "/freeze <user_id>"),
    "unfreeze": ("Unfreeze a SentriX moderator.", "/unfreeze <user_id>"),
    "badge": ("Set a moderator badge.", "/badge <user_id> <text>"),
    "warnconfig": ("Configure warning thresholds and automatic actions.", "/warnconfig <threshold|action|duration> <value>"),
    "warnmode": ("Configure warning thresholds and automatic actions.", "/warnmode <threshold|action|duration> <value>"),
    "admincache": ("Refresh the Telegram administrator cache.", "/admincache"),
    "adminlist": ("List Telegram group administrators.", "/adminlist"),
    "setadmin": ("Grant SentriX-specific admin access.", "/setadmin <user_id>"),
    "removeadmin": ("Remove SentriX-specific admin access.", "/removeadmin <user_id>"),
    "anonadmin": ("Configure anonymous administrator mode.", "/anonadmin on|off"),
    "adminerror": ("Configure administrator error replies.", "/adminerror on|off"),
    "zombies": ("Scan for deleted or bot accounts.", "/zombies"),
    "protect": ("Protect a user from moderation actions.", "/protect <user>"),
    "unprotect": ("Remove moderation protection from a user.", "/unprotect <user>"),
    "protected": ("List protected users.", "/protected"),
    "case": ("View a moderation case.", "/case <case_id>"),
    "mod": ("List SentriX moderators.", "/mod list"),
    "modinfo": ("Show moderator permissions and status.", "/modinfo [user]"),
    "locktype": ("Describe one supported lock type.", "/locktype <type>"),
    "locktypelist": ("List all supported lock types.", "/locktypelist"),
    "locktypes": ("List all supported lock types.", "/locktypes"),
    "locklist": ("Show active locks.", "/locklist"),
    "lockbot": ("Block bot commands in the group.", "/lockbot [duration]"),
    "locklink": ("Block links in the group.", "/locklink [duration]"),
    "unlockbot": ("Unblock bot commands.", "/unlockbot"),
    "unlocklink": ("Unblock links.", "/unlocklink"),
    "bot": ("Enable or disable SentriX for a group.", "/bot on|off"),
    "addblocklist": ("Add a blocked keyword.", "/addblocklist <keyword>"),
    "deleteblocklist": ("Remove a blocked keyword.", "/deleteblocklist <keyword>"),
    "blocklists": ("List blocked keywords.", "/blocklists"),
    "blocklistmode": ("Choose the blocklist action.", "/blocklistmode warn|mute|ban"),
    "custom": ("Create a reusable custom command.", "/custom <name> <response>"),
    "customcommands": ("List custom commands.", "/customcommands"),
    "delcustom": ("Delete a custom command.", "/delcustom <name>"),
    "broadcast": ("Broadcast a message to connected groups.", "/broadcast"),
    "appeal": ("Appeal a moderation case in bot DM.", "/appeal <case_id> <message>"),
    "ttt": ("Start a Tic-Tac-Toe game.", "/ttt [user_id]"),
    "tttleaderboard": ("Show the Tic-Tac-Toe leaderboard.", "/tttleaderboard"),
    "tttmystats": ("Show your Tic-Tac-Toe statistics.", "/tttmystats"),
    "tttend": ("Forfeit the current Tic-Tac-Toe game.", "/tttend"),
    "allowconnections": ("Allow or block PM connections.", "/allowconnections on|off"),
    "warns": ("View a user's warning count.", "/warns [user]"),
    "resetwarns": ("Reset warnings for a user.", "/resetwarns <user>"),
    "blocklist": ("Add a blocked keyword.", "/blocklist <keyword>"),
    "features": ("Show SentriX feature highlights.", "/features"),
}
for _command, (_description, _syntax) in _ADDITIONAL_GUIDES.items():
    GUIDES.setdefault(
        _command,
        CommandGuide(
            f"/{_command}", _description, _syntax, _syntax,
            "Group administrators or authorized moderators",
            "Use `/help` to return to categories and review related controls.",
        ),
    )


CATEGORIES = (
    HelpCategory("admin", "👮 Admin", "Moderate members and manage administrators.", ("grant", "revoke", "grants", "promote", "demote", "adminlist", "setadmin", "removeadmin", "admincache", "auth", "unauth", "freeze", "unfreeze", "badge", "ban", "tban", "unban", "kick", "kickme", "mute", "tmute", "unmute", "warn", "unwarn", "warnings", "warns", "resetwarns", "warnconfig", "warnmode", "del", "purge", "pin", "unpin", "protect", "unprotect", "protected", "case", "mod", "modinfo", "anonadmin", "adminerror", "zombies")),
    HelpCategory("protection", "🛡️ Protection", "Protect your group from spam, raids, and unwanted content.", ("antispam", "antiraid", "captcha", "setflood", "lock", "unlock", "locktype", "locktypes", "locktypelist", "locklist", "lockbot", "locklink", "unlockbot", "unlocklink", "addblocklist", "blocklist", "deleteblocklist", "blocklists", "blocklistmode", "bot")),
    HelpCategory("welcome", "👋 Welcome", "Configure join and leave messages.", ("welcome", "setwelcome", "goodbye", "setgoodbye")),
    HelpCategory("filters", "📝 Filters", "Create and manage automatic keyword replies.", ("filter", "filters", "stop", "stopall")),
    HelpCategory("notes", "📚 Notes", "Save reusable group information.", ("save", "get", "notes", "clear")),
    HelpCategory("logging", "📢 Logging", "Configure the dedicated admin log channel.", ("setlog", "unsetlog", "logchannel", "logsettings", "broadcast")),
    HelpCategory("setup", "⚙️ Setup", "Configure the current group interactively.", ("setup", "settings", "rules", "setrules", "reset", "language")),
    HelpCategory("connections", "🔗 Connections", "Manage groups from the bot private chat.", ("connect", "connections", "disconnect", "connection", "allowconnections")),
    HelpCategory("info", "📊 Information", "Inspect IDs, admins, reports, statistics, games, and appeals.", ("id", "info", "admins", "stats", "report", "appeal", "ttt", "tttleaderboard", "tttmystats", "tttend")),
    HelpCategory("bot", "🤖 Bot", "SentriX status and discovery commands.", ("start", "help", "about", "ping", "features", "custom", "customcommands", "delcustom")),
)

PAGE_SIZE = 6


def _category(key: str):
    return next((item for item in CATEGORIES if item.key == key), None)


def _nav(*buttons):
    return [{"text": text, "callback_data": data} for text, data in buttons]


def home_markup():
    rows = []
    for index in range(0, len(CATEGORIES), 3):
        rows.append(_nav(*[(item.title, f"sxhelp_cat_{item.key}_0") for item in CATEGORIES[index:index + 3]]))
    rows.append(_nav(("📖 Guides", "sxhelp_guides_0")))
    rows.append(_nav(("↩️ Back", "sxhelp_home"), ("🏠 Home", "sxhelp_home"), ("✖️ Close", "sxhelp_close")))
    return {"inline_keyboard": rows}


def home_text():
    return "🛡️ **SentriX Help Center**\n\nChoose a category or open the Guides section.\n\nEvery command page includes syntax, examples, permissions, notes, and related commands."


def category_page(category_key: str, page: int = 0):
    category = _category(category_key)
    if not category:
        return None
    page_count = max(1, (len(category.commands) + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(0, min(page, page_count - 1))
    current = category.commands[page * PAGE_SIZE:(page + 1) * PAGE_SIZE]
    rows = []
    for index in range(0, len(current), 3):
        rows.append([
            {"text": f"/{name}", "callback_data": f"sxhelp_cmd_{category.key}_{name}"}
            for name in current[index:index + 3]
        ])
    navigation = []
    if page > 0:
        navigation.append(("⬅️ Prev", f"sxhelp_cat_{category.key}_{page - 1}"))
    if page < page_count - 1:
        navigation.append(("Next ➡️", f"sxhelp_cat_{category.key}_{page + 1}"))
    if navigation:
        rows.append(_nav(*navigation))
    rows.append(_nav(("↩️ Back", "sxhelp_home"), ("🏠 Home", "sxhelp_home"), ("✖️ Close", "sxhelp_close")))
    text = f"🛡️ **{category.title}**\n\n{category.description}\n\nSelect a command: **Page {page + 1}/{page_count}**"
    return text, {"inline_keyboard": rows}


def guides_page(page: int = 0):
    guides = ("getting_started", "group_setup", "log_channel", "moderation", "anti_spam", "welcome", "verification", "filters", "locks")
    titles = {"getting_started": "🚀 Getting Started", "group_setup": "⚙️ Group Setup", "log_channel": "📢 Log Channel Setup", "moderation": "👮 Moderation", "anti_spam": "🛡️ Anti-Spam", "welcome": "👋 Welcome", "verification": "🔐 Verification", "filters": "📝 Filters", "locks": "🔒 Locks"}
    page_count = max(1, (len(guides) + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(0, min(page, page_count - 1))
    current = guides[page * PAGE_SIZE:(page + 1) * PAGE_SIZE]
    rows = []
    for index in range(0, len(current), 3):
        rows.append([
            {"text": titles[key], "callback_data": f"sxhelp_guide_{key}"}
            for key in current[index:index + 3]
        ])
    navigation = []
    if page > 0:
        navigation.append(("⬅️ Prev", f"sxhelp_guides_{page - 1}"))
    if page < page_count - 1:
        navigation.append(("Next ➡️", f"sxhelp_guides_{page + 1}"))
    if navigation:
        rows.append(_nav(*navigation))
    rows.append(_nav(("↩️ Back", "sxhelp_home"), ("🏠 Home", "sxhelp_home"), ("✖️ Close", "sxhelp_close")))
    return "📖 **SentriX Guides**\n\nChoose a guide:", {"inline_keyboard": rows}


GUIDE_TEXT = {
    "getting_started": "🚀 **Getting Started**\n\nAdd SentriX to your group, promote it with the required permissions, then run `/setup`. Use `/help` any time to browse commands.",
    "group_setup": "⚙️ **Group Setup**\n\nRun `/setup` for the guided wizard or `/settings` for direct inline configuration. Rules use `/setrules` and `/rules`.",
    "log_channel": "📢 **Log Channel Setup**\n\nCreate or select a private admin channel, forward one of its messages, and run `/setlog`. Check it with `/logchannel` and remove it with `/unsetlog`.",
    "moderation": "👮 **Moderation**\n\nUse `/ban`, `/mute`, `/kick`, and `/warn` with a reply or target. Temporary actions accept `30m`, `2h`, or `1d`. Review warnings with `/warnings`.",
    "anti_spam": "🛡️ **Anti-Spam**\n\nUse `/antispam on` and `/setflood 5 3`. SentriX can detect flooding, repeated messages, suspicious links, mass mentions, and excessive emoji.",
    "welcome": "👋 **Welcome**\n\nSet messages with `/setwelcome` and `/setgoodbye`. Variables include `{first}`, `{last}`, `{username}`, `{id}`, and `{chat}`.",
    "verification": "🔐 **Verification**\n\nEnable `/captcha on` to show new members a Verify Yourself button. Combine it with anti-raid settings for safer joins.",
    "filters": "📝 **Filters**\n\nCreate `/filter rules Read #rules`, inspect `/filters`, remove one with `/stop rules`, or clear all with `/stopall`.",
    "locks": "🔒 **Locks**\n\nUse `/lock links`, `/lock media`, or another supported type. Remove restrictions with `/unlock <type>`.",
}


def guide_page(key: str):
    text = GUIDE_TEXT.get(key)
    if not text:
        return None
    return text, {"inline_keyboard": [_nav(("↩️ Back", "sxhelp_guides_0"), ("🏠 Home", "sxhelp_home"), ("✖️ Close", "sxhelp_close"))]}


def command_page(name: str, category: str = ""):
    guide = GUIDES.get(name)
    if not guide:
        return None
    related = " ".join(f"`{item}`" for item in guide.related) or "None"
    text = (f"🛡️ **{guide.name}**\n\n**Description**\n{guide.description}\n\n**Syntax**\n`{guide.syntax}`\n\n**Example**\n`{guide.example}`\n\n**Permissions**\n{guide.permissions}\n\n**Usage notes**\n{guide.notes}\n\n**Related commands**\n{related}")
    back = f"sxhelp_cat_{category}_0" if category else "sxhelp_home"
    return text, {"inline_keyboard": [_nav(("↩️ Back", back), ("🏠 Home", "sxhelp_home"), ("✖️ Close", "sxhelp_close"))]}


def render_callback(data: str):
    parts = data.split("_")
    if data in {"sxhelp_home", "sxhelp_close"}:
        return ("", {}) if data.endswith("close") else (home_text(), home_markup())
    if data == "sxhelp_guides" or data.startswith("sxhelp_guides_"):
        page = int(parts[-1]) if parts[-1].isdigit() else 0
        return guides_page(page)
    if data.startswith("sxhelp_cat_"):
        category = parts[2]
        page = int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else 0
        return category_page(category, page)
    if data.startswith("sxhelp_cmd_"):
        command_data = data.removeprefix("sxhelp_cmd_")
        category, _, name = command_data.partition("_")
        return command_page(name or category, category if name else "")
    if data.startswith("sxhelp_guide_"):
        return guide_page(data.removeprefix("sxhelp_guide_"))
    return None


def help_markup():
    return home_markup()


def help_text():
    return home_text()


class HelpFeature:
    commands = frozenset({"help", "about", "ping"})

    async def handle(self, command: str, args: list[str], context: FeatureContext) -> FeatureResult:
        if command == "about":
            return FeatureResult(True, "🛡️ **SentriX**\n\nFast, secure, customizable Telegram group protection and management.")
        if command == "ping":
            return FeatureResult(True, "🏓 SentriX is online.")
        return FeatureResult(True, home_text(), home_markup())


def category_text(category: str):
    page = category_page(category, 0)
    return page[0] if page else None
