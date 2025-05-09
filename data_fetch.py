import yfinance as yf
import pandas as pd

import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, period="1mo", interval="1h"):
    try:
        data = yf.download(ticker, period=period, interval=interval)
        print(f"Fetched data for {ticker}:\n{data.head()}")  # Debugging
        return data.dropna()
    except Exception as e:
        print(f"[ERROR] Failed to fetch stock data for {ticker}: {e}")
        return pd.DataFrame()