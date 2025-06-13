import feedparser
import time
import logging
import telegram
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inisialisasi bot Telegram
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

# URL RSS Forex Factory
RSS_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"

# Fungsi untuk filter berita
def is_relevant(entry):
    currencies = ['USD', 'EUR', 'GBP']
    return 'High' in entry.summary and any(currency in entry.title for currency in currencies)

# Menyimpan ID item yang sudah dikirim agar tidak dikirim ulang
sent_items = set()

# Fungsi utama
def main():
    while True:
        try:
            feed = feedparser.parse(RSS_URL)
            for entry in feed.entries:
                uid = entry.id
                if uid not in sent_items and is_relevant(entry):
                    message = f"📌 <b>{entry.title}</b>

{entry.summary}

🔗 {entry.link}"
                    bot.send_message(chat_id=TELEGRAM_CHANNEL, text=message, parse_mode=telegram.constants.ParseMode.HTML)
                    sent_items.add(uid)
                    logger.info(f"Sent: {entry.title}")
            time.sleep(300)  # Cek setiap 5 menit
        except Exception as e:
            logger.error(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
