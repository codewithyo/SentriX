"""Structured logging boundary for SentriX features."""

import logging


LOGGER = logging.getLogger("sentrix")


def configure_logging(level: int = logging.INFO) -> None:
    if not LOGGER.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s sentrix: %(message)s"))
        LOGGER.addHandler(handler)
    LOGGER.setLevel(level)


def feature_error(feature: str, error: Exception) -> None:
    LOGGER.exception("%s feature failed: %s", feature, error)
