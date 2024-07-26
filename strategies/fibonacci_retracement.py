import pandas as pd
import backtrader as bt

def calculate_fibonacci_levels(df):
    high_price = df['High'].max()
    low_price = df['Low'].min()
    diff = high_price - low_price
    fib_levels = {
        '38.2%': high_price - (diff * 0.382),
        '50%': high_price - (diff * 0.5),
        '61.8%': high_price - (diff * 0.618)
    }
    return fib_levels

class CombinedSMARetracementStrategy(bt.SignalStrategy):
    params = (
        ('sma_short_period', 2),
        ('sma_long_period', 4),
        ('stop_loss', 0.01),
        ('take_profit', 0.02),
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
            current_close = self.data_close[0]
            prev_close = self.data_close[-1]
            fib_level_50 = self.params.fib_levels['50%']
            fib_level_38_2 = self.params.fib_levels['38.2%']
            
            print(f"Buy Signal - Current Close: {current_close}, Previous Close: {prev_close}, Fib Levels: {self.params.fib_levels}")

            pullback_to_fib = (current_close <= fib_level_50 and prev_close > fib_level_50) or \
                            (current_close <= fib_level_38_2 and prev_close > fib_level_38_2)
            return in_uptrend and pullback_to_fib
        except IndexError as e:
            print(f"IndexError in buy signal condition: {e}")
        return False

    def sell_signal_condition(self):
        try:
            in_downtrend = self.sma_short[0] < self.sma_long[0]
            current_close = self.data_close[0]
            prev_close = self.data_close[-1]
            fib_level_50 = self.params.fib_levels['50%']
            fib_level_38_2 = self.params.fib_levels['38.2%']
            
            print(f"Sell Signal - Current Close: {current_close}, Previous Close: {prev_close}, Fib Levels: {self.params.fib_levels}")

            pullback_to_fib = (current_close >= fib_level_50 and prev_close < fib_level_50) or \
                            (current_close >= fib_level_38_2 and prev_close < fib_level_38_2)
            return in_downtrend and pullback_to_fib
        except IndexError as e:
            print(f"IndexError in sell signal condition: {e}")
        return False

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

def main():
    df = pd.read_csv('data/fixed_EUR_USD_Historical_Data.csv')
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df.set_index('Date', inplace=True)
    df.dropna(inplace=True)

    fib_levels = calculate_fibonacci_levels(df)
    print(f"Initial Fibonacci Levels: {fib_levels}")

    cerebro = bt.Cerebro()
    cerebro.addstrategy(CombinedSMARetracementStrategy, fib_levels=fib_levels)

    data = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data)

    cerebro.broker.set_cash(10000)
    cerebro.broker.setcommission(commission=0.001)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())

if __name__ == '__main__':
    main()
