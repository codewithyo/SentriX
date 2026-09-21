"""Message handler extension point for modular SentriX features."""

from .antispam import AntiSpamFeature, SpamDecision


class MessagePipeline:
    def __init__(self) -> None:
        self.antispam = AntiSpamFeature()

    async def inspect(self, chat_id: int, user_id: int, text: str) -> SpamDecision:
        return await self.antispam.inspect(chat_id, user_id, text)
