import MetaTrader5 as mt5


def place_market_order(trade_type, symbol, lot, price, tp, sl, deviation,magic,comment):
    # tick = mt5.symbol_info_tick("EURUSD-Z")
    if trade_type == 'buy':
        trade_type = mt5.ORDER_TYPE_BUY
    elif trade_type == 'sell':
        trade_type = mt5.ORDER_TYPE_SELL
        
    # sy5 = mt5.symbol_info("EURUSD-Z").trade_tick_size
    # v= str(sy5)
    # decimal =  v[::-1].find('.')
    # sl =  round(sl,decimal)
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": trade_type,
        "price": price,
        "sl" : sl,
        "tp" : tp,
        # "deviation": deviation,
        # "magic": magic,
        # "comment": comment,
        # "type_time": mt5.ORDER_TIME_GTC,
        # "type_filling": mt5.ORDER_FILLING_IOC
    }
    result = mt5.order_send(request)
    # print(price,tp,sl )

    return result