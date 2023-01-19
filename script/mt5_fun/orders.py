import pandas as pd
import numpy as np
import MetaTrader5 as mt5
from datetime import datetime, timedelta

def expiration_time(minutes):
    # timezone = pytz.timezone("Etc/UTC")
    expire1 = datetime.now() + timedelta(hours=3,minutes=minutes)
    expire = expire1.replace(second=0, microsecond=0)
    expire = int(expire.timestamp())
    # print(expire1)
    return expire

def pending_order(trade_type, symbol, lot, price, tp, sl, deviation, expiration_in_minutes):
    if trade_type == 'buy_stop':
        trade_type = mt5.ORDER_TYPE_BUY_STOP
    elif trade_type == 'sell_stop':
        trade_type = mt5.ORDER_TYPE_SELL_STOP
    elif trade_type == 'buy_limit':
        trade_type = mt5.ORDER_TYPE_BUY_LIMIT
    elif trade_type == 'sell_limit':
        trade_type = mt5.ORDER_TYPE_SELL_LIMIT
    else: print('order type not found in the fun. please  add it in the mt5_fun folder')
    
    expiration = expiration_time(expiration_in_minutes)
    
    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY_LIMIT,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": deviation,
        "magic": 225522,
        "comment": "rrrrr",
        "type_filling": mt5.ORDER_FILLING_RETURN,
        "type_time": mt5.ORDER_TIME_SPECIFIED,
        # "type_time": mt5.ORDER_TIME_GTC,
        "expiration" : expiration
    }
    result = mt5.order_send(request)
    
    return result