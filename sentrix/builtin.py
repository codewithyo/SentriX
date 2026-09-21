"""Built-in SentriX feature registry."""

from .admin import AdminFeature
from .context import FeatureContext
from .filters import FiltersFeature
from .help import HelpFeature
from .information import InformationFeature
from .connections import ConnectionsFeature
from .locks import LocksFeature
from .logging_commands import LoggingFeature
from .moderation import ModerationFeature
from .notes import NotesFeature
from .protection import ProtectionFeature
from .registry import FeatureRegistry
from .setup import SetupFeature
from .settings import SettingsFeature
from .start import StartFeature
from .verification import VerificationFeature
from .welcome import WelcomeFeature


def build_registry() -> FeatureRegistry:
    """Build a fresh registry so tests and workers do not share mutable state."""
    return FeatureRegistry(
        [
            StartFeature(),
            HelpFeature(),
            AdminFeature(),
            ModerationFeature(),
            FiltersFeature(),
            WelcomeFeature(),
            LocksFeature(),
            NotesFeature(),
            VerificationFeature(),
            SettingsFeature(),
            SetupFeature(),
            ProtectionFeature(),
            LoggingFeature(),
            ConnectionsFeature(),
            InformationFeature(),
        ]
    )
