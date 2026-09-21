#!/usr/bin/env python3
"""
Local development server for the Koyeb runtime.

Usage:
    python run_local.py

Then expose with ngrok:
    ngrok http 8000

Set webhook manually:
    curl https://<ngrok-url>/api/setup_webhook
"""

import os

import uvicorn
from api.index import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
  
