import pandas as pd
from strategies.market_structure import break_in_market_structure

def test_break_in_market_structure():
    data = {
        'high': [1.1000, 1.1050, 1.1100],
        'low': [1.0900, 1.0950, 1.1000]
    }
    df = pd.DataFrame(data)
    
    result = break_in_market_structure(df)
    
    assert result is True  # Expecting a True value indicating a market structure break
