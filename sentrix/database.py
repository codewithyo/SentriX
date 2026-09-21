"""Small async storage contract used by independent SentriX modules."""

from collections.abc import Callable
from typing import Any, Protocol
import asyncio


class AsyncStore(Protocol):
    async def get(self, namespace: str, default: Any = None) -> Any: ...
    async def set(self, namespace: str, value: Any) -> None: ...


class MappingStore:
    """Async adapter around the existing synchronous load/save functions."""

    def __init__(self, loader: Callable[[str], Any], saver: Callable[[str, Any], Any]):
        self._loader = loader
        self._saver = saver

    async def get(self, namespace: str, default: Any = None) -> Any:
        value = await asyncio.to_thread(self._loader, namespace)
        return default if value is None else value

    async def set(self, namespace: str, value: Any) -> None:
        await asyncio.to_thread(self._saver, namespace, value)


class MemoryStore:
    """Deterministic store for unit tests and local feature development."""

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}

    async def get(self, namespace: str, default: Any = None) -> Any:
        return self._data.get(namespace, default)

    async def set(self, namespace: str, value: Any) -> None:
        self._data[namespace] = value
