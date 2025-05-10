import subprocess

def build_prompt(ticker, price, indicators, headlines, sentiment_score, history_logs):
    history_section = "\n".join([
        f"- {log['timestamp'][:10]}: {log['decision']}, RSI={log['RSI']}, Sentiment={log['sentiment']}"
        for log in history_logs
    ]) or "- No past decisions"

    return f"""
Stock: {ticker}

Historical decisions:
{history_section}

Current Price: {price}
SMA: {indicators['SMA']}
EMA: {indicators['EMA']}
RSI: {indicators['RSI']}

News sentiment: {sentiment_score}
Headlines: {headlines}

Give a trade recommendation (buy/sell/hold), confidence %, and reasoning.
"""


def query_dolphin(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "dolphin3"],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120
        )
        if result.returncode != 0:
            print(f"[ERROR] Dolphin3 error: {result.stderr.decode()}")
            return "Error from AI"
        return result.stdout.decode("utf-8")
    except Exception as e:
        return f"[ERROR] Failed to run Dolphin3: {e}"
