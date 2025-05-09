import yfinance as yf
from datetime import datetime, timedelta

def fetch_latest(ticker: str, period="1d", interval="1m"):
    """
    Download intraday bars for the past day.
    """
    end = datetime.now()
    start = end - timedelta(days=1)
    df = yf.download(
        tickers=ticker,
        start=start, end=end,
        interval=interval, progress=False
    )
    return df  # DataFrame with Open/High/Low/Close/Volume