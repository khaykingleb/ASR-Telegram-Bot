"""Configuration variables."""

import os
from pathlib import Path

from pyngrok import ngrok

BASE_DIR = Path(__file__).parent.parent.resolve()

NGROK_FORWARDING_URL = ngrok.connect(8000, bind_tls=True).public_url
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_BOT_URL = f"{NGROK_FORWARDING_URL}/bot/{TG_BOT_TOKEN}"
