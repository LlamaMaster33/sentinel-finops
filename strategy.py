import ta

def compute_signals(df, sma_window, ema_window):
    if df.empty or len(df) < max(sma_window, ema_window, 14):
        return {"price": 0, "SMA": 0, "EMA": 0, "RSI": 0}

    close = df['Close']
    if hasattr(close, "values") and close.values.ndim > 1:
        close = close.squeeze()

    df['SMA'] = close.rolling(window=sma_window).mean()
    df['EMA'] = close.ewm(span=ema_window).mean()
    df['RSI'] = ta.momentum.RSIIndicator(close=close, window=14).rsi()

    latest = df.iloc[-1]
    return {
        "price": latest.get("Close", 0),
        "SMA": latest.get("SMA", 0),
        "EMA": latest.get("EMA", 0),
        "RSI": latest.get("RSI", 0)
    }
