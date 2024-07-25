import pandas as pd
import backtrader as bt
from strategies.fibonacci_retracement import FibonacciStrategy


def main():
    cerebro = bt.Cerebro()
    cerebro.addstrategy(FibonacciStrategy)

    df = pd.read_csv('data/fixed_EUR_USD_Historical_Data.csv')

    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df.set_index('Date', inplace=True)
    df.dropna(inplace=True)

    data = bt.feeds.PandasData(
        dataname=df,
        datetime=None,  
        open='Open',
        high='High',
        low='Low',
        close='Close',
        volume='Volume',
        openinterest=None
    )

    cerebro.adddata(data)
    cerebro.broker.set_cash(10000)  # Initial cash
    cerebro.broker.setcommission(commission=0.001)  # Commission

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())

if __name__ == '__main__':
    main()
