import pandas as pd
import numpy as np
import backtrader as bt

def calculate_fibonacci_levels(df):
    # Check if the required columns exist
    if not all(col in df.columns for col in ['High', 'Low']):
        raise KeyError("Required columns are missing from the DataFrame")
    
    high_price = df['High'].max()
    low_price = df['Low'].min()
    
    if pd.isna(high_price) or pd.isna(low_price):
        return np.nan

    diff = high_price - low_price
    fib_50 = high_price - (diff * 0.5)
    return fib_50

class FibonacciStrategy(bt.SignalStrategy):
    params = (
        ('stop_loss', 0.01),
        ('take_profit', 0.02)
    )

    def __init__(self):
        self.order = None
        self.last_signal_date = None
        self.data_close = self.datas[0].close
        self.data_high = self.datas[0].high
        self.data_low = self.datas[0].low
        
        # Load and set Fibonacci level
        self.df = self.load_and_check_data('data/fixed_EUR_USD_Historical_Data.csv')
        self.params.fib_level = calculate_fibonacci_levels(self.df)
        print(f"Initial Fibonacci Level: {self.params.fib_level}")

    def load_and_check_data(self, file_path):
        try:
            df = pd.read_csv(file_path)
            print("Data Loaded Successfully")
            print("Initial DataFrame:")
            print(df.head())
            print(df.columns)
            print(df.info())

            # Convert and clean DataFrame
            df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
            df.set_index('Date', inplace=True)
            df.dropna(axis=1, how='all', inplace=True)  # Drop columns with all NaN values

            print("Data after processing:")
            print(df.head())
            print(df.info())

            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return pd.DataFrame()

    def next(self):
        if self.order:
            return

        print("Checking trading signals...")
        print(f"Current Price: {self.data_close[0]}")
        print(f"Fibonacci Level: {self.params.fib_level}")

        # Ensure enough data is available before checking conditions
        if len(self.data_close) > 1:
            buy_condition = self.buy_signal_condition()
            sell_condition = self.sell_signal_condition()
            
            print(f"Buy Signal Condition Met: {buy_condition}")
            print(f"Sell Signal Condition Met: {sell_condition}")

            if buy_condition:
                print("Executing Buy Order")
                self.buy(size=1)
                self.order = self.buy()
                print(f"Buy Order Executed at: {self.data_close[0]}")

            elif sell_condition:
                print("Executing Sell Order")
                self.sell(size=1)
                self.order = self.sell()
                print(f"Sell Order Executed at: {self.data_close[0]}")

    def buy_signal_condition(self):
        current_price = self.data_close[0]
        if pd.isna(self.params.fib_level):
            print("Fibonacci level is not set or is NaN")
            return False

        print(f"Buy Signal Condition Check: {current_price} vs {self.params.fib_level}")
        return abs(current_price - self.params.fib_level) < (0.0001 * current_price)

    def sell_signal_condition(self):
        current_price = self.data_close[0]
        
        # Ensure there are enough data points
        if len(self.data_high) < 2:
            return False

        # Get previous day high and low values
        try:
            previous_day_high = self.data_high.get(size=1)[-2]
            previous_day_low = self.data_low.get(size=1)[-2]
        except IndexError:
            return False

        print(f"Sell Signal Condition Check: Current Price: {current_price}, Previous Day High: {previous_day_high}, Previous Day Low: {previous_day_low}")
        
        return current_price > previous_day_high or current_price < previous_day_low

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

        self.order = None
