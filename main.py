import time
import pandas as pd
import oandapyV20
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.orders as orders

from config.config import *
from strategies.moving_average import moving_average_strategy
from strategies.risk_management import calculate_stop_loss, calculate_take_profit

client = oandapyV20.API(access_token=ACCESS_TOKEN)

def get_realtime_data():
    params = {"instruments": INSTRUMENT}
    r = pricing.PricingInfo(accountID=ACCOUNT_ID, params=params)
    client.request(r)
    prices = r.response['prices']
    return prices

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

def collect_and_trade():
    data = []
    position = 0
    while True:
        prices = get_realtime_data()
        close_price = float(prices[0]['closeoutAsk'])
        data.append({'close': close_price, 'time': prices[0]['time']})
        df = pd.DataFrame(data)
        df = moving_average_strategy(df, SHORT_WINDOW, LONG_WINDOW)

        if len(df) >= LONG_WINDOW:
            if df['positions'].iloc[-1] == 1 and position == 0:
                place_trade(int(TRADE_SIZE_PERCENT * ACCOUNT_BALANCE), 'buy', STOP_LOSS_PIPS, TAKE_PROFIT_PIPS)
                position = int(TRADE_SIZE_PERCENT * ACCOUNT_BALANCE)
            elif df['positions'].iloc[-1] == -1 and position > 0:
                place_trade(int(TRADE_SIZE_PERCENT * ACCOUNT_BALANCE), 'sell', STOP_LOSS_PIPS, TAKE_PROFIT_PIPS)
                position = 0
        time.sleep(60)

if __name__ == "__main__":
    collect_and_trade()
