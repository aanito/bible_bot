#!/usr/bin/env python3
import os, json, requests
from datetime import datetime
import pytz
from pathlib import Path
from dotenv import load_dotenv

# Load .env for local dev; harmless in Actions (no .env present)
ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
READING_FILE = os.getenv("READING_FILE", str(ROOT / "readings" / "G1_Sequential_Bible_Reading_2025-10-05_to_2026-09-10.json"))
TIMEZONE = os.getenv("TIMEZONE", "Africa/Addis_Ababa")

if not BOT_TOKEN or not GROUP_CHAT_ID:
    raise SystemExit("Missing TELEGRAM_BOT_TOKEN or GROUP_CHAT_ID environment variables")

# Determine date to send (Ethiopia timezone)
tz = pytz.timezone(TIMEZONE)
today = datetime.now(tz).date().isoformat()

# Load readings
with open(READING_FILE, "r", encoding="utf-8") as f:
    plan = json.load(f)

reading = plan.get(today)
if not reading or "G1" not in reading:
    print(f"No reading for {today}. Exiting.")
    exit(0)

ot = reading["G1"].get("old_testament", "N/A")
nt = reading["G1"].get("new_testament", "N/A")

message = (
    "📖 Good morning, beloveds!\n\n"
    f"<b>Our Bible Reading for {today}:</b>\n\n"
    f"Old Testament: {ot}\n"
    f"New Testament: {nt}\n\n"
    "Blessings!! 🙏"
)

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": GROUP_CHAT_ID,
    "text": message,
    "parse_mode": "HTML",
    "disable_web_page_preview": True
}

resp = requests.post(url, json=payload, timeout=15)
try:
    resp.raise_for_status()
    print("Message sent:", resp.json())
except Exception as e:
    print("Failed to send:", e, "response:", resp.text)
    raise
