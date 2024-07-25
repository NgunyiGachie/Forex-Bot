def calculate_fibonacci_levels(data):
    high_price = data['high'].max()
    low_price = data['low'].min()
    diff = high_price - low_price
    fib_50 = high_price - (diff * 0.5)
    return fib_50
