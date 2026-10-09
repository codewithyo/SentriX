#!/usr/bin/env python3
"""
Local development server for the SentriX runtime.

Usage:
    python run_local.py

Telegram updates are received through long polling; no public URL is needed.
"""

import os

import uvicorn
from api.index import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
  
