import json
from datetime import datetime
import pytz
from telegram import Bot
from telegram.error import TelegramError
import schedule
import time
from dotenv import load_dotenv
import os
import asyncio  # for async

# --- LOAD ENVIRONMENT VARIABLES ---
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID"))
JSON_FILE = "readings/G1_Sequential_Bible_Reading_2025-10-05_to_2026-10-09.json"
TIMEZONE = "Africa/Addis_Ababa"
POST_TIME = "06:00"  # 10:00 AM local time

# Load reading plan
with open(JSON_FILE, "r", encoding="utf-8") as f:
    reading_plan = json.load(f)

bot = Bot(token=BOT_TOKEN)

async def send_daily_reading():
    tz = pytz.timezone(TIMEZONE)
    today = datetime.now(tz).strftime("%Y-%m-%d")

    reading = reading_plan.get(today)
    if reading and "G1" in reading:
        ot_text = reading["G1"].get("old_testament", "No OT reading")
        nt_text = reading["G1"].get("new_testament", "No NT reading")
        message = (
            f"📖 Good morning, beloveds!\n\n"
            f"**Our Bible Reading for {today}:**\n"
            f"Old Testament: {ot_text}\n"
            f"New Testament: {nt_text}\n\n"
            "Blessings!! 🙏"
        )
    else:
        message = f"No reading found for {today}."

    try:
        await bot.send_message(chat_id=GROUP_CHAT_ID, text=message, parse_mode="Markdown")
        print(f"Message sent for {today}")
    except TelegramError as e:
        print(f"Failed to send message: {e}")

# Schedule daily post
def job():
    asyncio.run(send_daily_reading())

schedule.every().day.at(POST_TIME).do(job)

print(f"Bot started. Daily readings will be sent at {POST_TIME} {TIMEZONE} time.")

while True:
    schedule.run_pending()
    time.sleep(60)
