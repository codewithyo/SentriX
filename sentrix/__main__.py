"""Development entrypoint for the SentriX feature package."""

from .config import SentriXConfig


if __name__ == "__main__":
    config = SentriXConfig.from_env()
    errors = config.validate()
    print("SentriX configuration OK" if not errors else "\n".join(errors))
