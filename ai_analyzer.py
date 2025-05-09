import subprocess
import json

def build_prompt(ticker, price, indicators, headlines, sentiment_score):
    return f"""
Stock: {ticker}
Price: {price}
SMA: {indicators['SMA']}
EMA: {indicators['EMA']}
RSI: {indicators['RSI']}

News sentiment: {sentiment_score}
Headlines: {headlines}

Give a trade recommendation (buy/sell/hold), confidence %, and reasoning.
"""

def query_dolphin(prompt):
    result = subprocess.run(["ollama", "run", "dolphin3"], input=prompt.encode(), capture_output=True)
    return result.stdout.decode()