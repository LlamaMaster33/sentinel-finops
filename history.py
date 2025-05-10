import os
import csv
from datetime import datetime

def ensure_log_dir():
    os.makedirs("logs", exist_ok=True)

def write_log(ticker, signals, sentiment, decision, confidence, reasoning):
    ensure_log_dir()
    file_path = f"logs/{ticker}.csv"
    file_exists = os.path.exists(file_path)

    with open(file_path, "a", newline="") as csvfile:
        fieldnames = ["timestamp", "price", "SMA", "EMA", "RSI", "sentiment", "decision", "confidence", "reasoning"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.utcnow().isoformat(),
            "price": signals.get("price"),
            "SMA": signals.get("SMA"),
            "EMA": signals.get("EMA"),
            "RSI": signals.get("RSI"),
            "sentiment": sentiment,
            "decision": decision,
            "confidence": confidence,
            "reasoning": reasoning
        })

def load_recent_logs(ticker, count=5):
    file_path = f"logs/{ticker}.csv"
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        reader = list(csv.DictReader(f))
        return reader[-count:]
