from dotenv import load_dotenv
import os

load_dotenv()

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Stocks
TICKERS = os.getenv("TICKERS", "").split(",")
INTERVAL = int(os.getenv("INTERVAL_MINUTES", 5))
SMA_FAST = int(os.getenv("SMA_FAST", 10))
SMA_SLOW = int(os.getenv("SMA_SLOW", 30))

# News
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
NEWS_SOURCES = os.getenv("NEWS_SOURCES", "").split(",")
RSS_FEEDS = os.getenv("RSS_FEEDS", "").split(",")

# AI
USE_AI = os.getenv("USE_AI", "false").lower() == "true"
AI_WINDOW = int(os.getenv("AI_WINDOW", 30))
