import backtrader as bt
from config import SMA_FAST, SMA_SLOW

class SmaCross(bt.Strategy):
    params = dict(fast=SMA_FAST, slow=SMA_SLOW)

    def __init__(self):
        # Initialize two SMAs and crossover detector
        self.fast_sma = bt.ind.SMA(period=self.p.fast)
        self.slow_sma = bt.ind.SMA(period=self.p.slow)
        self.cross = bt.ind.CrossOver(self.fast_sma, self.slow_sma)

    def next(self):
        # Buy when fast crosses above slow
        if not self.position and self.cross > 0:
            self.buy()
        # Sell when fast crosses below slow
        elif self.position and self.cross < 0:
            self.sell()
