import pandas as pd
import backtrader as bt
import numpy as np

def calculate_fibonacci_levels(df):
    high_price = df['High'].max()
    low_price = df['Low'].min()
    diff = high_price - low_price
    fib_levels = {
        '50%': high_price - (diff * 0.5),
        '61.8%': high_price - (diff * 0.618),
        '38.2%': high_price - (diff * 0.382)
    }
    return fib_levels

class CombinedSMARetracementStrategy(bt.SignalStrategy):
    params = (
        ('sma_short_period', 20),
        ('sma_long_period', 30),
        ('stop_loss', 0.02),
        ('take_profit', 0.04),
        ('fib_levels', None)  
    )

    def __init__(self):
        self.order = None
        self.data_close = self.datas[0].close
        self.data_high = self.datas[0].high
        self.data_low = self.datas[0].low

        self.sma_short = bt.indicators.SimpleMovingAverage(self.data_close, period=self.params.sma_short_period)
        self.sma_long = bt.indicators.SimpleMovingAverage(self.data_close, period=self.params.sma_long_period)
        
        if self.params.fib_levels is None:
            raise ValueError("Fibonacci levels must be provided")
        
        print(f"Initial Fibonacci Levels: {self.params.fib_levels}")

    def next(self):
        if self.order:
            return

        if self.buy_signal_condition():
            self.order = self.buy()
            self.sell_bracket() 
            print(f"Buy Order Executed at: {self.data_close[0]}")

        elif self.sell_signal_condition():
            self.order = self.sell()
            self.sell_bracket() 
            print(f"Sell Order Executed at: {self.data_close[0]}")

    def buy_signal_condition(self):
        try:
            in_uptrend = self.sma_short[0] > self.sma_long[0]
            pullback_to_fib = self.data_close[0] <= self.params.fib_levels['50%'] and self.data_close[-1] > self.params.fib_levels['50%']
            return in_uptrend and pullback_to_fib
        except IndexError as e:
            print(f"IndexError in buy signal condition: {e}")
        return False
        
    def sell_signal_condition(self):
        try:
            in_downtrend = self.sma_short[0] < self.sma_long[0]
            pullback_to_fib = self.data_close[0] >= self.params.fib_levels['50%'] and self.data_close[-1] < self.params.fib_levels['50%']
            return in_downtrend and pullback_to_fib
        except IndexError as e:
            print(f"IndexError in sell signal condition: {e}")
        return False

    def sell_bracket(self):
        if self.order:
            stop_price = self.data_close[0] * (1 - self.params.stop_loss) if self.order.isbuy() else self.data_close[0] * (1 + self.params.stop_loss)
            take_profit_price = self.data_close[0] * (1 + self.params.take_profit) if self.order.isbuy() else self.data_close[0] * (1 - self.params.take_profit)

            if self.order.isbuy():
                print(f"Placing Sell Stop Order at: {stop_price}")
                print(f"Placing Sell Limit Order at: {take_profit_price}")
            else:
                print(f"Placing Buy Stop Order at: {stop_price}")
                print(f"Placing Buy Limit Order at: {take_profit_price}")

            self.sell(
                exectype=bt.Order.Stop, price=stop_price, parent=self.order
            )
            self.sell(
                exectype=bt.Order.Limit, price=take_profit_price, parent=self.order
            )

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            print(f"Order {order.ref} Submitted or Accepted")
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                print(f"Buy Order Completed: {order.executed.price}")
            elif order.issell():
                print(f"Sell Order Completed: {order.executed.price}")

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            print(f"Order {order.ref} Canceled/Margin/Rejected")
            if order.status == order.Canceled:
                print(f"Order {order.ref} Canceled")
            elif order.status == order.Margin:
                print(f"Order {order.ref} Margin Call")
            elif order.status == order.Rejected:
                print(f"Order {order.ref} Rejected")

        self.order = None
