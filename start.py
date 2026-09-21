#!/usr/bin/env python3
"""Koyeb runtime entrypoint."""

import uvicorn

from api.index import app
from sentrix.config import get_config


if __name__ == "__main__":
    port = get_config().port
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
