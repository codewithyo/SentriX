<div align="center">

# 🛡️ SentriX

**Professional Telegram Group Management & Moderation Bot**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0.106-00A3E0?style=for-the-badge&logo=telegram)](https://docs.pyrogram.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.0%2B-13AA52?style=for-the-badge&logo=mongodb)](https://mongodb.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

*Moderate Smarter. Stay Safer.*

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [📖 Commands](#-commands) • [⚙️ Deploy](#️-deployment) • [💬 Support](#-support)

</div>

---

## 📌 Overview

**SentriX** is an enterprise-grade Telegram group moderation bot built with **FastAPI** and **Pyrogram**. It provides intelligent moderation, multi-group management, and a complete audit trail — all backed by MongoDB.

- ✅ **Intelligent Moderation** — Progressive discipline with auto-enforcement
- ✅ **Multi-Group Management** — Manage unlimited groups simultaneously
- ✅ **Enterprise Persistence** — MongoDB + JSON fallback + auto-backup
- ✅ **Performance Optimized** — Async processing with intelligent caching
- ✅ **Complete Audit Trail** — Every action logged and traceable
- ✅ **Security First** — Auth, authorization, and anti-nuke protection

---

## ✨ Features

<details>
<summary><b>🛡️ Moderation</b></summary>

- Progressive Discipline: Warnings → Mute → Ban
- Timed actions with flexible durations (`30m`, `2h`, `1d`, `7d`)
- Auto-action on warning threshold (configurable)
- Case management — every action is traceable and appealable
- Protected users — prevent important members from accidental moderation

</details>

<details>
<summary><b>🔐 Permission System</b></summary>

- Role-based access: Owner → Moderator → User
- Fine-grained permissions: `ban` · `unban` · `mute` · `unmute` · `kick` · `warn` · `delete` · `pin`
- Moderator freeze — disable actions temporarily (anti-nuke)
- Per-group permission isolation

</details>

<details>
<summary><b>📊 Data Persistence</b></summary>

```
Local Cache (5min TTL)
        ↓
Local JSON Files (Primary)
        ↓
MongoDB (Authoritative)
        ↓
Fallback Files (Recovery)
```

- Auto-sync with MongoDB on startup
- Atomic writes with fallback protection
- Per-group data isolation
- Auto-bootstrap on first group connection

</details>

<details>
<summary><b>📝 Filters, Notes & Blocklist</b></summary>

- Keyword, exact-match, start-of-message, and regex filters
- Automatic responses on filter match
- Group notes with hashtag triggers (`#notename`)
- Blocklist with configurable actions (`warn`, `mute`, `ban`)

</details>

<details>
<summary><b>👋 Welcome & Logging</b></summary>

- Custom welcome and goodbye messages with variables (`{name}`, `{mention}`, `{id}`, `{chat}`)
- Dedicated log channel for every moderation event
- Structured log format with user, admin, reason, and timestamp

</details>

<details>
<summary><b>🎮 Games</b></summary>

- Tic-Tac-Toe with custom board sizes (3×3 to 5×5)
- Leaderboard and personal stats tracking

</details>

---

## 🧩 Architecture

The `sentrix/` package is the feature layer — async, dependency-injected, testable without Telegram or MongoDB.

| Module | Responsibility |
|--------|----------------|
| `start.py` | Welcome screen, inline keyboards |
| `admin.py` | Administrator actions and permission contracts |
| `moderation.py` | User moderation command contracts |
| `antispam.py` | Flood, repeat, link, and mention decisions |
| `filters.py` | Keyword filter persistence and management |
| `welcome.py` | Welcome and goodbye configuration |
| `locks.py` | Per-group content lock state |
| `notes.py` | Persistent group notes |
| `verification.py` | CAPTCHA and member verification settings |
| `settings.py` | Generic per-group settings |
| `help.py` | Category-based help navigation |
| `setup.py` | Interactive seven-step group setup wizard |
| `logging_commands.py` | `/setlog`, `/unsetlog`, `/logchannel`, `/logsettings` |
| `protection.py` | Anti-spam, anti-raid, and flood settings |
| `connections.py` | Multi-group connection surface |
| `information.py` | Group and user information commands |

> Shared contracts: `sentrix/context.py` · `sentrix/database.py` · `sentrix/config.py` · `sentrix/utils.py`  
> `sentrix/registry.py` — isolated command dispatch and error handling  
> `api/index.py` — ASGI import surface only

---

## 📖 Commands

### 👤 User Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/start` | Bot welcome screen | `/start` |
| `/help` | Interactive help menu | `/help` |
| `/id` | User or group info | `/id`, `/id @user`, `/id me` |
| `/stats` | Group moderation stats | `/stats` |
| `/modinfo` | View moderator info | `/modinfo [@user]` |
| `/warns` | View warnings | `/warns @user` |
| `/appeal` | Appeal a moderation action (DM only) | `/appeal <case_id> <reason>` |
| `/ping` | Check bot availability | `/ping` |

---

### 🚫 Moderation Commands

> Most commands support **reply mode** (reply to a message) or **direct mode** (`/ban @user 2h reason`).

| Command | Description | Example |
|---------|-------------|---------|
| `/ban` | Permanently ban a user | `/ban @user spam` |
| `/tban` | Temporarily ban a user | `/tban @user 7d spam` |
| `/unban` | Unban a user | `/unban @user` |
| `/kick` | Kick a user | `/kick @user` |
| `/kickme` | Kick yourself | `/kickme` |
| `/mute` | Permanently mute a user | `/mute @user` |
| `/tmute` | Temporarily mute a user | `/tmute @user 2h` |
| `/unmute` | Unmute a user | `/unmute @user` |
| `/warn` | Issue a warning | `/warn @user off-topic` |
| `/unwarn` | Remove a warning | `/unwarn @user` |
| `/resetwarns` | Reset all warnings | `/resetwarns @user` |
| `/warnings` | View user warnings | `/warnings @user` |
| `/pin` | Pin a message | `/pin` (reply) |
| `/unpin` | Unpin a message | `/unpin` |
| `/del` | Delete a message | `/del` (reply) |
| `/purge` | Purge messages | `/purge` |
| `/zombies` | Scan and kick deleted accounts | `/zombies` |
| `/case` | View case details | `/case <case_id>` |

---

### 🔐 Owner / Admin Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/protect` | Protect user from moderation | `/protect @user` |
| `/unprotect` | Remove protection | `/unprotect @user` |
| `/auth` | Authorize a moderator | `/auth 123456789` |
| `/unauth` | Remove authorization | `/unauth 123456789` |
| `/grant` | Grant a permission | `/grant ban 123456789` |
| `/revoke` | Revoke a permission | `/revoke ban 123456789` |
| `/freeze` | Freeze a moderator (anti-nuke) | `/freeze 123456789` |
| `/unfreeze` | Unfreeze a moderator | `/unfreeze 123456789` |
| `/badge` | Set moderator badge | `/badge 123456789 🟢 Senior Mod` |
| `/setadmin` | Add SentriX admin (no Telegram role) | `/setadmin 123456789` |
| `/removeadmin` | Remove SentriX admin | `/removeadmin 123456789` |
| `/warnconfig` | Configure warning system | `/warnconfig threshold 3` |
| `/promote` | Promote to admin | `/promote @user` |
| `/demote` | Demote from admin | `/demote @user` |

---

### 🛡️ Protection Commands

| Command | Description |
|---------|-------------|
| `/antispam [on\|off]` | Toggle anti-spam |
| `/antiraid [on\|off]` | Toggle anti-raid |
| `/captcha [on\|off]` | Toggle CAPTCHA verification |
| `/lock <type>` | Lock a content type |
| `/unlock <type>` | Unlock a content type |
| `/setflood <msgs> [secs]` | Configure flood limits |

---

### 📝 Filters & Blocklist

| Command | Description | Example |
|---------|-------------|---------|
| `/filter <keyword> <response>` | Add auto-reply filter | `/filter spam No spam allowed` |
| `/filter -regex <pattern> <response>` | Regex filter | `/filter -regex ^\d{10}$ Wrong format` |
| `/filter -start <keyword> <response>` | Start-of-message filter | `/filter -start !cmd Not a command` |
| `/filters` | List all filters | `/filters` |
| `/stop <keyword>` | Remove a filter | `/stop spam` |
| `/stopall` | Remove all filters | `/stopall` |
| `/addblocklist <keyword>` | Block a keyword | `/addblocklist badword` |
| `/deleteblocklist <keyword>` | Remove blocked keyword | `/deleteblocklist badword` |
| `/blocklists` | List blocked keywords | `/blocklists` |
| `/blocklistmode <action>` | Set blocklist action | `/blocklistmode ban` |

---

### 📚 Notes

```bash
/save rules    Follow the group rules please.  # Save a note
/get rules                                      # Get a note (also: #rules)
/notes                                          # List all notes
/clear rules                                    # Delete a note
```

---

### 👋 Welcome & Goodbye

```bash
/setwelcome Welcome {mention} to {chat}! 👋
/setgoodbye  Goodbye {name}, we'll miss you!
/setrules    No spam. Be respectful.
```

**Variables:** `{name}` · `{mention}` · `{id}` · `{chat}`

---

### 📢 Log Channel

```bash
/setlog <channel_id>   # Set log channel (or forward a message from the channel)
/logchannel            # Show configured log channel
/unsetlog              # Remove log channel
/logsettings           # View enabled log event types
```

**Example log entry:**
```
🛡️ BAN

User:   @username
Admin:  @admin
Reason: Spam
Time:   14:32
Case:   #42
```

**Logged events:** Bans · Unbans · Mutes · Kicks · Warnings · Deleted messages · Member joins/leaves · Filter triggers · Settings changes · Permission changes

---

### 🔗 Connections & Broadcast

| Command | Description | Usage |
|---------|-------------|-------|
| `/connect` | Connect group to PM management | `/connect <chat_id>` |
| `/connections` | View / switch connected groups | `/connections` |
| `/disconnect` | Disconnect a group | `/disconnect [all]` |
| `/allowconnections` | Control connection permissions | `/allowconnections yes\|no` |
| `/broadcast` | Broadcast to all connected groups (DM only) | `/broadcast` |

---

### ⚙️ Warning Configuration

```bash
/warnconfig threshold 3       # Set warning limit
/warnconfig action ban        # Auto-action on threshold (ban / mute / kick)
/warnconfig duration 1d       # Duration for timed auto-action
```

**Duration formats:** `30m` · `2h` · `1d` · `3d` · `7d`

---

### 🎮 Game Commands

| Command | Description |
|---------|-------------|
| `/ttt @opponent [size]` | Start Tic-Tac-Toe (3×3 to 5×5) |
| `/tttleaderboard` | View top players |
| `/tttmystats` | Your personal stats |
| `/tttend` | Forfeit current game |

---

### 📊 Information Commands

| Command | Description |
|---------|-------------|
| `/id` | Get user or chat ID |
| `/info` | User information |
| `/admins` | List SentriX admins |
| `/adminlist` | List Telegram group admins |
| `/stats` | Moderation statistics |
| `/report` | Report a user |

---

## 👑 Permission Hierarchy

```
👑  Owner
    └── 🛡️  SentriX Global Admin
               └── 👑  Telegram Group Owner
                          └── 👮  Telegram Group Admin
                                     └── 🔑  Granted Moderator
                                                └── 👤  Regular User
```

> `ADMIN_IDS` — bot-level access, separate from Telegram group admins.  
> Group-level permissions are fully isolated between groups.

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/codewithyo/SentriX.git
cd SentriX
pip install -r requirements.txt
cp .env.example .env
```

### 2. Configure `.env`

```env
# Required
API_ID=                          # From my.telegram.org
API_HASH=                        # From my.telegram.org
BOT_TOKEN=                       # From @BotFather
OWNER_ID=                        # Your Telegram user ID
SENTRIX_BOT_USERNAME=hr_sentrix_bot

# Optional but recommended
ADMIN_IDS=123456789,987654321    # Comma-separated Global Admin IDs
LOG_GROUP_ID=0                   # 0 = auto-detect
BACKUP_CHAT_ID=0

# MongoDB (recommended — without it, data is lost on restart)
MONGODB_URI=mongodb+srv://<user>:<pass>@<cluster>/?appName=Cluster0
MONGODB_DB_NAME=hr_moderation_bot

# Server
PORT=8000
STORAGE_PATH=/data/modbot
OWNER_DEBUG_NOTIFICATIONS=0
```

### 3. Run

```bash
python start.py
```

### 4. Setup in Telegram

```bash
# 1. Start a DM with the bot
/start

# 2. Add the bot to your group as admin

# 3. Authorize your first moderator (run as owner)
/auth <moderator_user_id>

# 4. Done!
/help
```

---

## ☁️ Deployment

### 🐳 Docker

```bash
# Build
docker build -t sentrix .

# Run
docker run -d \
  -e API_ID=123456 \
  -e API_HASH=abcdef \
  -e BOT_TOKEN=123456:ABC \
  -e OWNER_ID=987654321 \
  -e MONGODB_URI=mongodb://host:port/db \
  -p 8000:8000 \
  --name sentrix \
  sentrix
```

### ☁️ Cloud Platforms

| Platform | How to Deploy |
|----------|--------------|
| **Koyeb** (Recommended) | Push to GitHub → Connect repo → Set env vars → Deploy |
| **Render** | Connect GitHub → Set env vars → Auto-restart enabled |
| **Railway** | Link GitHub → Select repo → Add env vars → One-click |

---

## 📂 File Structure

```
SentriX/
├── sentrix/                   # Modular feature package
│   ├── start.py
│   ├── admin.py
│   ├── moderation.py
│   ├── antispam.py
│   ├── filters.py
│   ├── welcome.py
│   ├── locks.py
│   ├── notes.py
│   ├── verification.py
│   ├── settings.py
│   ├── help.py
│   ├── setup.py
│   ├── logging_commands.py
│   ├── protection.py
│   ├── connections.py
│   ├── information.py
│   ├── context.py
│   ├── database.py
│   ├── config.py
│   ├── utils.py
│   ├── registry.py
│   └── application.py
├── api/
│   └── index.py               # ASGI import surface
├── db.py                      # MongoDB wrapper
├── games.py                   # Tic-Tac-Toe engine
├── start.py                   # Production entry point
├── run_local.py               # Local dev runner
├── Dockerfile
├── requirements.txt
├── .env.example
├── BOT_FEATURES.md
└── CHANGES.md
```

---

## 📦 Dependencies

```
pyrogram==2.0.106    # Telegram MTProto client
tgcrypto             # Pyrogram crypto operations
fastapi              # Web framework (webhook receiver)
httpx                # HTTP client (Telegram Bot API)
uvicorn[standard]    # ASGI server
pymongo>=4.0         # MongoDB driver
```

---

## 🔒 Security Best Practices

1. **Never commit `.env`** — keep credentials private
2. **Use HTTPS** — enable SSL in production
3. **Minimal permissions** — grant only what moderators need
4. **Audit regularly** — review `/case` logs
5. **Anti-nuke** — `/freeze` suspicious moderators immediately
6. **Backups** — MongoDB + local JSON fallback always active

---

## 🐛 Troubleshooting

<details>
<summary><b>Bot not responding</b></summary>

```bash
curl http://localhost:8000/api/status
curl http://localhost:8000/api/setup_webhook
```

Check bot has admin permissions in the group and `BOT_TOKEN` is correct.
</details>

<details>
<summary><b>Data not persisting after restart</b></summary>

- Verify `MONGODB_URI` is set and the cluster is reachable
- Check `STORAGE_PATH` directory exists and has write permissions: `chmod 755 /data/modbot`
- Review startup logs for MongoDB connection errors
</details>

<details>
<summary><b>Command not working</b></summary>

1. Check your permissions: `/modinfo`
2. Verify syntax: `/help <command>`
3. Confirm bot is admin in the group
</details>

---

## 💬 Support

- 🐛 **Bugs / Features** — [Open a GitHub Issue](https://github.com/codewithyo/SentriX/issues)
- 📖 **Detailed docs** — [BOT_FEATURES.md](BOT_FEATURES.md)
- 👨‍💼 **Developer** — [@dreamm_ca](https://t.me/dreamm_ca)

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

Built with ❤️ using **Pyrogram** · **FastAPI** · **MongoDB**

---

<div align="center">

🛡️ **SentriX** — *Your Community. Secured.*

⭐ Star the repo if you find it useful!

</div>
