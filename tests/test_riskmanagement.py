from strategies.riskmanagement import calculate_stop_loss, calculate_take_profit

def test_calculate_stop_loss():
    price = 1.1000
    pips = 20
    stop_loss = calculate_stop_loss(price, pips)
    
    assert stop_loss == 1.0980  # Based on the price and pips

def test_calculate_take_profit():
    price = 1.1000
    pips = 20
    take_profit = calculate_take_profit(price, pips)
    
    assert take_profit == 1.1020  # Based on the price and pips
