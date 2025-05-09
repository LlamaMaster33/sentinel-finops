import yfinance as yf

def fetch_stock_data(ticker, period="1mo", interval="1h"):
    data = yf.download(ticker, period=period, interval=interval)
    return data.dropna()