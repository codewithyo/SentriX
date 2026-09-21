"""Async, side-effect-free anti-spam decision engine."""

from dataclasses import dataclass
import re
import time

from .utils import has_url


@dataclass(frozen=True, slots=True)
class SpamDecision:
    violated: bool
    reason: str = ""


class AntiSpamFeature:
    def __init__(self) -> None:
        self._activity: dict[tuple[int, int], list[float]] = {}
        self._last_text: dict[tuple[int, int], tuple[str, float]] = {}

    async def inspect(self, chat_id: int, user_id: int, text: str) -> SpamDecision:
        now = time.monotonic()
        key = (chat_id, user_id)
        activity = [stamp for stamp in self._activity.get(key, []) if now - stamp <= 3]
        activity.append(now)
        self._activity[key] = activity[-12:]
        previous = self._last_text.get(key)
        self._last_text[key] = (text, now)
        if len(activity) >= 5:
            return SpamDecision(True, "Flooding")
        if previous and previous[0].strip().lower() == text.strip().lower() and now - previous[1] <= 10:
            return SpamDecision(True, "Repeated message")
        if has_url(text):
            return SpamDecision(False, "Link detected")
        if len(re.findall(r"@\w+", text)) >= 6:
            return SpamDecision(True, "Mass mentions")
        return SpamDecision(False)
