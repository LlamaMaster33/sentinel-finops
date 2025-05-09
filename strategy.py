import ta

def compute_signals(df, sma_window, ema_window):
    if df.empty or len(df) < max(sma_window, ema_window, 14):
        return {"price": 0, "SMA": 0, "EMA": 0, "RSI": 0}

    # Extract clean Series
    close = df['Close']
    if hasattr(close, "values") and close.values.ndim > 1:
        close = close.squeeze()

    df['SMA'] = close.rolling(window=sma_window).mean()
    df['EMA'] = close.ewm(span=ema_window).mean()
    df['RSI'] = ta.momentum.RSIIndicator(close=close, window=14).rsi()

    latest = df.iloc[-1]
    return {
        "price": latest["Close"],
        "SMA": latest["SMA"],
        "EMA": latest["EMA"],
        "RSI": latest["RSI"]
    }
