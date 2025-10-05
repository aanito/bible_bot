import json
from datetime import datetime
import pytz
from telegram import Bot
from telegram.error import TelegramError
import schedule
import time
import os

# --- CONFIGURATION ---
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Set via environment variable
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")   # Set via environment variable
JSON_FILE = "readings/G1_Sequential_Bible_Reading_2025-10-05_to_2026-10-09.json"
TIMEZONE = "Africa/Addis_Ababa"
POST_TIME = "06:00"  # 24h format HH:MM

# Load reading plan
with open(JSON_FILE, "r", encoding="utf-8") as f:
    reading_plan = json.load(f)

def send_daily_reading():
    tz = pytz.timezone(TIMEZONE)
    today = datetime.now(tz).date().isoformat()

    reading = reading_plan.get(today)
    if reading:
        message = f"📖 Good morning, beloved!\n\n"
        message += f"**G1 Bible Reading for {today}:**\n"
        message += f"Old Testament: {reading['G1']['old_testament']}\n"
        message += f"New Testament: {reading['G1']['new_testament']}\n\n"
        message += "Blessings!! 🙏"
    else:
        message = f"No reading found for {today}."

    bot = Bot(token=BOT_TOKEN)
    try:
        bot.send_message(chat_id=GROUP_CHAT_ID, text=message, parse_mode="Markdown")
        print(f"Message sent for {today}")
    except TelegramError as e:
        print(f"Failed to send message: {e}")

# Schedule daily post
schedule.every().day.at(POST_TIME).do(send_daily_reading)

print(f"Bot started. Daily readings will be sent at {POST_TIME} {TIMEZONE} time.")

while True:
    schedule.run_pending()
    time.sleep(60)
