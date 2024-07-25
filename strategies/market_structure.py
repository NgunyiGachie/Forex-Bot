def break_in_market_structure(data):
    # Ensure data is a DataFrame with 'high' and 'low' columns
    last_high = data['high'].iloc[-2]
    last_low = data['low'].iloc[-2]
    current_high = data['high'].iloc[-1]
    current_low = data['low'].iloc[-1]
    
    # Simple break detection: current high > last high or current low < last low
    return current_high > last_high or current_low < last_low
