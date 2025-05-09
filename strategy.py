import pandas as pd
import talib

def compute_signals(df, sma_window, ema_window):
    df['SMA'] = df['Close'].rolling(window=sma_window).mean()
    df['EMA'] = df['Close'].ewm(span=ema_window).mean()
    df['RSI'] = talib.RSI(df['Close'])

    latest = df.iloc[-1]
    signals = {
        "price": latest["Close"],
        "SMA": latest["SMA"],
        "EMA": latest["EMA"],
        "RSI": latest["RSI"]
    }
    return signals