"""Plug-and-play feature registry with isolated error handling."""

from collections.abc import Iterable
from typing import Protocol

from .context import FeatureContext, FeatureResult
from .logging import feature_error


class Feature(Protocol):
    commands: frozenset[str]

    async def handle(self, command: str, args: list[str], context: FeatureContext) -> FeatureResult: ...


class FeatureRegistry:
    def __init__(self, features: Iterable[Feature] = ()) -> None:
        self._features = list(features)
        self._by_command = {
            command: feature for feature in self._features for command in feature.commands
        }

    def add(self, feature: Feature) -> None:
        self._features.append(feature)
        for command in feature.commands:
            self._by_command[command] = feature

    async def dispatch(self, command: str, args: list[str], context: FeatureContext) -> FeatureResult:
        feature = self._by_command.get(command.lower())
        if feature is None:
            return FeatureResult()
        try:
            return await feature.handle(command.lower(), args, context)
        except Exception as error:
            feature_error(feature.__class__.__name__, error)
            return FeatureResult(handled=True, text="❌ SentriX could not complete that action.")
