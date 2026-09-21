"""Small async storage contract used by independent SentriX modules."""

from collections.abc import Callable
from typing import Any, Protocol
import asyncio


class AsyncStore(Protocol):
    async def get(self, namespace: str, default: Any = None) -> Any: ...
    async def set(self, namespace: str, value: Any) -> None: ...


class MappingStore:
    """Async adapter around the existing synchronous load/save functions."""

    def __init__(self, loader: Callable[[str], Any], saver: Callable[[str, Any], Any], backing_file: str):
        self._loader = loader
        self._saver = saver
        self._backing_file = backing_file

    async def get(self, namespace: str, default: Any = None) -> Any:
        values = await asyncio.to_thread(self._loader, self._backing_file)
        if not isinstance(values, dict):
            return default
        return values.get(namespace, default)

    async def set(self, namespace: str, value: Any) -> None:
        values = await asyncio.to_thread(self._loader, self._backing_file)
        if not isinstance(values, dict):
            values = {}
        values[namespace] = value
        await asyncio.to_thread(self._saver, self._backing_file, values)


class MemoryStore:
    """Deterministic store for unit tests and local feature development."""

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}

    async def get(self, namespace: str, default: Any = None) -> Any:
        return self._data.get(namespace, default)

    async def set(self, namespace: str, value: Any) -> None:
        self._data[namespace] = value
