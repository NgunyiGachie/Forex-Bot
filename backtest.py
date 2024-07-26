import pandas as pd
import backtrader as bt
from strategies.fibonacci_retracement import CombinedSMARetracementStrategy

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

def main():
    
    df = pd.read_csv('data/fixed_EUR_USD_Historical_Data.csv')
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df.set_index('Date', inplace=True)
    df.dropna(inplace=True)

    fib_levels = calculate_fibonacci_levels(df)
    
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
