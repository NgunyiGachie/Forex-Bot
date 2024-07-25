import time
import pandas as pd
import numpy as np
import oandapyV20
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.orders as orders

from config.config import *
from strategies.fibonacci_retracement import calculate_fibonacci_levels
from strategies.market_structure import break_in_market_structure
from strategies.riskmanagement import calculate_stop_loss, calculate_take_profit


client = oandapyV20.API(access_token=ACCESS_TOKEN)

def get_realtime_data():
    params = {"instruments": INSTRUMENT}
    r = pricing.PricingInfo(accountID=ACCOUNT_ID, params=params)
    client.request(r)
    prices = r.response['prices']
    return prices

def calculate_fibonacci_levels(data):
    high_price = data['high'].max()
    low_price = data['low'].min()
    diff = high_price - low_price
    fib_50 = high_price - (diff * 0.5)
    return fib_50

def place_trade(units, side, stop_loss, take_profit):
    price = float(get_realtime_data()[0]['closeoutAsk'])
    sl_price = calculate_stop_loss(price, stop_loss) if side == 'buy' else calculate_take_profit(price, stop_loss)
    tp_price = calculate_take_profit(price, take_profit) if side == 'buy' else calculate_stop_loss(price, stop_loss)

    order = {
        "order": {
            "units": str(units),
            "instrument": INSTRUMENT,
            "side": side,
            "type": "market",
            "stopLossOnFill": {
                "price": str(sl_price)
            },
            "takeProfitOnFill": {
                "price": str(tp_price)
            }
        }
    }
    r = orders.OrderCreate(accountID=ACCOUNT_ID, data=order)
    client.request(r)
    return r.response

def break_in_market_structure(data):
    last_high = data['high'].iloc[-2]
    last_low = data['low'].iloc[-2]
    current_high = data['high'].iloc[-1]
    current_low = data['low'].iloc[-1]

    return current_high > last_high or current_low < last_low

def check_exit_conditions(data, entry_price, side):
    current_price = data['close'].iloc[-1]
    previous_day_high = data['high'].shift(1).resample('D').max().iloc[-1]
    previous_day_low = data['low'].shift(1).resample('D').min().iloc[-1]
    rr_ratio = 2

    if side == 'buy':
        return current_price >= previous_day_high or (current_price - entry_price) >= (entry_price - calculate_stop_loss(entry_price, STOP_LOSS_PIPS)) * rr_ratio
    else:
        return current_price <= previous_day_low or (entry_price - current_price) >= (calculate_stop_loss(entry_price, STOP_LOSS_PIPS) - entry_price) * rr_ratio

def collect_and_trade():
    data = []
    position = 0
    entry_price = None
    side = None
    while True:
        prices = get_realtime_data()
        close_price = float(prices[0]['closeoutAsk'])
        high_price = float(prices[0]['closeoutBid'])
        low_price = float(prices[0]['closeoutBid'])
        data.append({'close': close_price, 'high': high_price, 'low': low_price, 'time': prices[0]['time']})

        if len(df) >= 2:
            if break_in_market_structure(df):
                fib_50 = calculate_fibonacci_levels(df)
                if close_price <= fib_50 and position == 0:
                    place_trade(int(TRADE_SIZE_PERCENT * ACCOUNT_BALANCE), 'buy', STOP_LOSS_PIPS, TAKE_PROFIT_PIPS)
                    position = int(TRADE_SIZE_PERCENT * ACCOUNT_BALANCE)
                    entry_price = close_price
                    side = 'buy'
                elif close_price >= fib_50 and position == 0:
                    place_trade(int(TRADE_SIZE_PERCENT * ACCOUNT_BALANCE), 'sell', STOP_LOSS_PIPS, TAKE_PROFIT_PIPS)
                    position = int(TRADE_SIZE_PERCENT * ACCOUNT_BALANCE)
                    entry_price = close_price
                    side = 'sell'
            
            if position != 0 and check_exit_conditions(df, entry_price, side):
                place_trade(-position, 'sell' if side == 'buy' else 'buy', STOP_LOSS_PIPS, TAKE_PROFIT_PIPS)
                position = 0
                entry_price - None
                side = None

        time.sleep(60)
        
if __name__ == "__main__":
    collect_and_trade()
