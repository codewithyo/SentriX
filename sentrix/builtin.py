"""Built-in SentriX feature registry."""

from .admin import AdminFeature
from .context import FeatureContext
from .filters import FiltersFeature
from .locks import LocksFeature
from .moderation import ModerationFeature
from .notes import NotesFeature
from .registry import FeatureRegistry
from .settings import SettingsFeature
from .start import StartFeature
from .verification import VerificationFeature
from .welcome import WelcomeFeature


def build_registry() -> FeatureRegistry:
    """Build a fresh registry so tests and workers do not share mutable state."""
    return FeatureRegistry(
        [
            StartFeature(),
            AdminFeature(),
            ModerationFeature(),
            FiltersFeature(),
            WelcomeFeature(),
            LocksFeature(),
            NotesFeature(),
            VerificationFeature(),
            SettingsFeature(),
        ]
    )
