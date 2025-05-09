import os
from dotenv import load_dotenv

load_dotenv()

TICKERS = os.getenv("TICKERS", "AAPL,GOOG").split(",")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
INTERVAL_MINUTES = int(os.getenv("INTERVAL_MINUTES", 30))
SMA_WINDOW = int(os.getenv("SMA_WINDOW", 20))
EMA_WINDOW = int(os.getenv("EMA_WINDOW", 20))
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
RSS_FEEDS = list(filter(None, os.getenv("RSS_FEEDS", "").split(",")))
