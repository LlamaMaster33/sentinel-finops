import schedule
import time
from config import TICKERS, INTERVAL_MINUTES, SMA_WINDOW, EMA_WINDOW
from data_fetch import fetch_stock_data
from news_fetch import fetch_rss_news, fetch_newsapi_headlines
from sentiment import analyze_sentiment
from strategy import compute_signals
from ai_analyzer import build_prompt, query_dolphin
from notifier import send_telegram_message

def run_analysis():
    for ticker in TICKERS:
        df = fetch_stock_data(ticker)
        signals = compute_signals(df, SMA_WINDOW, EMA_WINDOW)

        headlines = fetch_rss_news() + fetch_newsapi_headlines(ticker)
        sentiment_score = sum(analyze_sentiment(h) for h in headlines) / len(headlines)

        prompt = build_prompt(ticker, signals["price"], signals, headlines[:5], sentiment_score)
        result = query_dolphin(prompt)

        message = f"""
[{ticker}] Recommendation:
{result.strip()}
"""
        send_telegram_message(message)

schedule.every(INTERVAL_MINUTES).minutes.do(run_analysis)

if __name__ == "__main__":
    run_analysis()
    while True:
        schedule.run_pending()
        time.sleep(1)