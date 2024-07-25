import pandas as pd
from strategies.moving_average import moving_average_strategy

def test_moving_average_strategy():
    data = {
        'close': [1.1000, 1.1020, 1.1040, 1.1060, 1.1080]
    }
    df = pd.DataFrame(data)
    short_window = 2
    long_window = 3
    df = moving_average_strategy(df, short_window, long_window)
    
    assert 'short_mavg' in df.columns
    assert 'long_mavg' in df.columns
    assert 'signal' in df.columns
    assert 'positions' in df.columns

    assert df['short_mavg'].iloc[-1] > 0
    assert df['long_mavg'].iloc[-1] > 0
