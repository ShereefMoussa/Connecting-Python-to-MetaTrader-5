from turtle import TPen
import MetaTrader5 as mt5
import pandas as pd
from datetime import timedelta


def get_server_time():
    return pd.to_datetime(mt5.symbol_info_tick('EURUSD-Z').time, unit='s')

def move_tp2_to_tp1(minutes_to_move):
    time_now = get_server_time()
    
    positions_get = mt5.positions_get()
    if len(positions_get):
        positions = pd.DataFrame(list(positions_get), columns=positions_get[0]._asdict().keys())
        positions['time'] = pd.to_datetime(positions['time'], unit='s')
        positions['time_msc'] = pd.to_datetime(positions['time'], unit='sm')
        positions['time_update'] = pd.to_datetime(positions['time_update'], unit='s')
        positions['time_update_msc'] = pd.to_datetime(positions['time_update_msc'], unit='ms')
        # check for open sell position not secured
        sell_position = positions[positions['type'] == 1] 
        for row in sell_position.itertuples():
            if time_now - row.time > timedelta(minutes = minutes_to_move):
                gap = row.sl - row.price_open
                tp = row.price_open - gap - mt5.symbol_info(row.symbol).trade_tick_size * 3
                result = modify_tp_position(row.ticket, row.symbol, tp)
        
        # check for open buy position not secured
        buy_position = positions[positions['type'] == 0] 
        for row in buy_position.itertuples():
            if time_now - row.time > timedelta(minutes = minutes_to_move):
                gap = row.price_open - row.sl
                tp = row.price_open + gap + mt5.symbol_info(row.symbol).trade_tick_size * 3
                result = modify_tp_position(row.ticket, row.symbol, tp)
                
    
    

def modify_tp_position(ticket, symbol, tp):
    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "tp": tp,
        "symbol": symbol,
        "position" : ticket,
    }
    result = mt5.order_send(request)
    return result


def modify_sl_position(ticket, symbol, sl):
    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "sl": sl,
        "symbol": symbol,
        "position" : ticket,
    }
    result = mt5.order_send(request)
    return result

def move_sl_to_entry():
    positions_get = mt5.positions_get()
    if len(positions_get):
        positions = pd.DataFrame(list(positions_get),columns=positions_get[0]._asdict().keys())
        # check for open sell position not secured
        sell_position = positions[positions['type'] == 1] 
        sell_position = sell_position[sell_position['price_open'] < sell_position['sl']]
        for row in sell_position.itertuples():
            if row.price_open - row.price_current   > row.sl - row.price_open :
                new_sl = row.price_open - mt5.symbol_info(row.symbol).trade_tick_size * 3
                modify_sl_position(row.ticket,row.symbol, new_sl)
                print(row.symbol, "order modified")
        
        # check for open buy position not secured
        buy_position = positions[positions['type'] == 0] 
        buy_position = buy_position[buy_position['price_open'] > buy_position['sl']]
        for row in buy_position.itertuples():
            if row.price_current - row.price_open   >  row.price_open - row.sl  :
                new_sl = row.price_open + mt5.symbol_info(row.symbol).trade_tick_size * 3
                modify_sl_position(row.ticket,row.symbol, new_sl)
                print(row.symbol, "order modified")
        positions_new = mt5.positions_get()
        positions_n = pd.DataFrame(list(positions_new),columns=positions_new[0]._asdict().keys())
        return positions, positions_n