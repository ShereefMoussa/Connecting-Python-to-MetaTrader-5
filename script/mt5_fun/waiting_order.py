# import modules
import pandas as pd
import numpy as np
import MetaTrader5 as mt5
import time
from mt5_fun.validation import *
from mt5_fun.market_order import *
from mt5_fun.orders import *
from log_fun import *

def waiting_order(order_type, symbol, lot, price, target_profit, stop_lose, deviation ,gap):
    while True:
        symbol_info = mt5.symbol_info_tick(symbol)
        if order_type == "buy" :
            if symbol_info.ask >= price:
                lot = is_not_risky_return_lot(symbol,gap,6)
                if lot:
                    re = place_market_order(order_type, symbol, lot, price,target_profit, stop_lose, deviation,"","")
                    print("nnn",re)
                    print(mt5.last_error())
                    break
            
        elif order_type == "sell" :
            if symbol_info.bid >= price:
                lot = is_not_risky_return_lot(symbol,gap,6)
                if lot:
                    re = place_market_order(order_type, symbol, lot, price,target_profit, stop_lose, deviation,"","")
                    print("nnn",re)
                    print(mt5.last_error())
                    break
        time.sleep(5)
        
        
def place_limit_or_market_order(type, symbol, lot,candle_p , tp, sl, deviation, expiration_in_minutes,price,row,old_gap):
    if type == "buy":
        trade_type = "buy_limit"
        result = pending_order(trade_type, symbol, lot, candle_p, tp, sl, deviation, expiration_in_minutes)
        # print("buy_limit",result)
        # logger.info(result)
        print(mt5.last_error())
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("order_send_limit failed, sending market order, retcode={}".format(result.retcode))
            if price - sl < row.atr_sma_5 *4:
                result = place_market_order('buy', symbol, lot, price, tp + old_gap, sl, deviation,"","")
                print("buy",result)
                print(mt5.last_error())
                if result.retcode != mt5.TRADE_RETCODE_DONE:
                    # logger.info(result)
                    print("market order failed, , retcode={}".format(result.retcode))
                    return result
            # logger.info(result)
        return result
        
    elif type == "sell":
        trade_type = "sell_limit"
        result = pending_order(trade_type, symbol, lot, candle_p, tp, sl, deviation, expiration_in_minutes)
        print("sell_limit",result)
        print(mt5.last_error())
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("order_send_limit failed, sending market order, retcode={}".format(result.retcode))
            # logger.info("market order failed, , retcode={}".format(result.retcode))
            if sl - price < row.atr_sma_5 *4:
                result = place_market_order('sell', symbol, lot, price, price - old_gap, sl, deviation,"","")
                print("sell",result)
                # logger.info(result)
                print(mt5.last_error())
                if result.retcode != mt5.TRADE_RETCODE_DONE:
                    # logger.info("market order failed, , retcode={}".format(result.retcode))
                    print("market order failed, , retcode={}".format(result.retcode))
                    return result
                # logger.info(result)
        return result