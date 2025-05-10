import schedule
import time
import requests
from config import TICKERS, INTERVAL_MINUTES, SMA_WINDOW, EMA_WINDOW, TELEGRAM_TOKEN
from data_fetch import fetch_stock_data
from news_fetch import fetch_rss_news, fetch_newsapi_headlines
from sentiment import analyze_sentiment
from strategy import compute_signals
from ai_analyzer import build_prompt, query_dolphin
from notifier import send_telegram_message
from history import load_recent_logs, write_log
from threading import Thread
import os
import sys

LOCKFILE = "/tmp/sentinel.lock"

if os.path.exists(LOCKFILE):
    print("❌ Sentinel is already running.")
    sys.exit(0)

with open(LOCKFILE, "w") as f:
    f.write("locked")

def parse_ai_output(result_text):
    """Naive parser - you can improve this with regex or LLM self-reflection"""
    lines = result_text.strip().splitlines()
    decision = next((l for l in lines if any(k in l.upper() for k in ["BUY", "SELL", "HOLD"])), "UNKNOWN")
    confidence = next((l for l in lines if "%" in l), "0%")
    reasoning = result_text.strip()
    return decision, confidence, reasoning

def analyze_ticker(ticker):
    try:
        print(f"\n🔍 Analyzing {ticker}...")
        df = fetch_stock_data(ticker)
        print("📊 Price data pulled")

        signals = compute_signals(df, SMA_WINDOW, EMA_WINDOW)
        print(f"📈 Signals: {signals}")

        headlines = fetch_rss_news() + fetch_newsapi_headlines(ticker)
        headlines = list(filter(None, headlines))[:5]
        print(f"📰 Headlines: {headlines}")

        sentiment_score = (
            sum(analyze_sentiment(h) for h in headlines) / len(headlines)
            if headlines else 0
        )
        print(f"💬 Sentiment score: {sentiment_score}")

        history_logs = load_recent_logs(ticker)
        prompt = build_prompt(ticker, signals["price"], signals, headlines, sentiment_score, history_logs)
        print(f"🧠 Prompt ready. Prompting Dolphin3...")

        result = query_dolphin(prompt)
        print("📤 AI Response:\n", result[:400])

        decision, confidence, reasoning = parse_ai_output(result)
        write_log(ticker, signals, sentiment_score, decision, confidence, reasoning)

        message = f"[{ticker}] Recommendation:\n{result.strip()}"
        print("📲 Sending Telegram...")
        send_telegram_message(message)
        print("✅ Message sent.")
    except Exception as e:
        print(f"[ERROR] Analysis failed for {ticker}: {e}")

def run_analysis():
    for ticker in TICKERS:
        analyze_ticker(ticker)

def telegram_command_listener():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    latest_update_id = None
    while True:
        try:
            res = requests.get(url).json()
            for result in res["result"]:
                if latest_update_id is not None and result["update_id"] <= latest_update_id:
                    continue
                message = result.get("message", {}).get("text", "")
                chat_id = result.get("message", {}).get("chat", {}).get("id")
                if message.lower().startswith("analyze"):
                    ticker = message.split(" ")[1].upper()
                    analyze_ticker(ticker)
                latest_update_id = result["update_id"]
        except Exception as e:
            print(f"[ERROR] Telegram command listener: {e}")
        time.sleep(10)

schedule.every(INTERVAL_MINUTES).minutes.do(run_analysis)

if __name__ == "__main__":
    Thread(target=telegram_command_listener, daemon=True).start()
    run_analysis()
    while True:
        schedule.run_pending()
        time.sleep(1)

import atexit
atexit.register(lambda: os.remove(LOCKFILE) if os.path.exists(LOCKFILE) else None)
