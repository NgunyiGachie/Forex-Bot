def calculate_stop_loss(price, pips):
    return round(price - (pips * 0.0001), 5)

def calculate_take_profit(price, pips):
    return round(price + (pips * 0.0001), 5)
