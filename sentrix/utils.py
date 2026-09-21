"""Pure helpers shared by SentriX feature modules."""

from datetime import timedelta
import re


def parse_duration(value: str | None) -> int | None:
    if not value or len(value) < 2:
        return None
    number, unit = value[:-1], value[-1].lower()
    if not number.isdigit() or unit not in "smhdw":
        return None
    seconds = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}[unit]
    result = int(number) * seconds
    return result if result > 0 else None


def format_duration(seconds: int) -> str:
    return str(timedelta(seconds=max(0, int(seconds))))


def command_parts(text: str) -> tuple[str, list[str]]:
    parts = text.strip().split()
    if not parts or not parts[0].startswith("/"):
        return "", []
    return parts[0].split("@", 1)[0].lstrip("/").lower(), parts[1:]


def has_url(text: str) -> bool:
    return bool(re.search(r"(?:https?://|www\\.|t\\.me/|telegram\\.me/)", text or "", re.IGNORECASE))


def render_template(template: str, user: dict, chat_name: str = "") -> str:
    first = str(user.get("first_name") or "User")
    last = str(user.get("last_name") or "")
    username = str(user.get("username") or "")
    user_id = str(user.get("id") or "")
    name = " ".join(part for part in (first, last) if part)
    return (template or "").replace("{first}", first).replace("{last}", last).replace(
        "{name}", name
    ).replace("{username}", username).replace("{id}", user_id).replace("{chat}", chat_name)
