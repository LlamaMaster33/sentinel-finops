import time, schedule
import pandas as pd
from config import TICKERS, INTERVAL, AI_WINDOW
from data_fetch import fetch_latest
from news_fetch import fetch_news_api, fetch_rss
from sentiment import analyze_sentiment
from strategy import SmaCross
from ai_analyzer import analyze_with_ai
from notifier import send_alert
import backtrader as bt

def job():
    for symbol in TICKERS:
        # 1) Fetch price data
        df = fetch_latest(symbol)
        print(f"Fetched data for {symbol}:\n{df.head()}")  # Debugging

        # Ensure the index is a datetime object
        df.index = pd.to_datetime(df.index, errors='coerce')

        # Flatten multi-level columns if necessary
        if isinstance(df.columns, pd.MultiIndex):
            try:
                df = df.xs(key=symbol, axis=1, level=1)  # Select data for the specific symbol
            except KeyError:
                print(f"Error: Symbol '{symbol}' not found in the data.")
                continue  # Skip this symbol

        # Check if 'Close' column exists
        if "Close" not in df.columns:
            print(f"Error: 'Close' column is missing for {symbol}")
            continue  # Skip this symbol

        # Drop rows with invalid datetime indices (if any)
        df = df.dropna(subset=["Close"])

        # 1) Take last N closes as a Series
        raw = df["Close"].tail(AI_WINDOW)

        # 2) Build a JSON‑friendly dict: key = ISO‑format string, value = float
        prices = {pd.Timestamp(ts).isoformat(): float(price) for ts, price in raw.items()}

        # 2) Fetch news & sentiment
        news = fetch_news_api(symbol) + fetch_rss()
        polarity, subjectivity = zip(*(analyze_sentiment(n) for n in news))

        # 3) AI analysis
        ai_result = analyze_with_ai(
            symbol, prices,
            {"polarity": sum(polarity) / len(polarity)},
            news
        )

        # 4) Rule‑based fallback
        cerebro = bt.Cerebro()
        cerebro.adddata(bt.feeds.PandasData(dataname=df))
        cerebro.addstrategy(SmaCross)
        cerebro.run()

        # 5) Send alert
        msg = (f"{symbol} ➔ {ai_result['action'].upper()} "
               f"(conf {ai_result['confidence']:.2f})\nReason: {ai_result['reason']}")
        send_alert(msg)

# Schedule
schedule.every(INTERVAL).minutes.do(job)
if __name__ == "__main__":
    job()
    while True:
        schedule.run_pending()
        time.sleep(1)
