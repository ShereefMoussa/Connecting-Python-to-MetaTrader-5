# import modules
import pandas as pd
import numpy as np
import MetaTrader5 as mt5

def orders_count():
    return mt5.orders_total()

def positions_count():
    return mt5.positions_total()

def balance():
    return mt5.account_info().balance

def risk_amount(risk):
    return mt5.account_info().balance * risk

def is_no_exposure(symbol, gap, volume, comm):
    symbol_info = mt5.symbol_info(symbol)
    order_risk = gap / symbol_info.trade_tick_size * symbol_info.trade_tick_value * volume + comm * volume
    return order_risk

def orders_risk(comm):
    orders_get = mt5.orders_get()
    if len(orders_get):
        positions = pd.DataFrame(list(orders_get),columns=orders_get[0]._asdict().keys())
        
        positions['gap'] = np.abs(positions['price_open'] - positions['sl'])
        risk_positions_list = []
        risky_symbol = []
        for row in positions.itertuples():
            r = is_no_exposure(row.symbol,row.gap, row.volume_current,comm)
            risk_positions_list.append(r)
            risky_symbol.append(row.symbol)
        return sum(risk_positions_list), risky_symbol 
    else:
        return 0, 'None'

def positions_risk(comm):
    positions_get = mt5.positions_get()
    if len(positions_get):
        positions_get = pd.DataFrame(list(positions_get),columns=positions_get[0]._asdict().keys())
        # check for open sell positions_get not secured
        sell_positions_get = positions_get[positions_get['type'] == 1] 
        sell_positions_get = sell_positions_get[sell_positions_get['price_open'] < sell_positions_get['sl']]
        
        # check for open buy positions_get not secured
        buy_positions_get = positions_get[positions_get['type'] == 0] 
        # buy_positions_get = buy_positions_get[buy_positions_get['price_open'] > buy_positions_get['sl']]
        # return num of not Break-Even positions_get
        
        risky_positions_get = pd.concat([sell_positions_get, buy_positions_get])
        
        risky_positions_get['gap'] = np.abs(risky_positions_get['price_open'] - risky_positions_get['sl'])
        risky_symbol = []
        risky_positions_list = []
        for row in risky_positions_get.itertuples():
            r = is_no_exposure(row.symbol,row.gap, row.volume,comm)
            risky_positions_list.append(r)
            risky_symbol.append(row.symbol)
            
        return sum(risky_positions_list) , risky_symbol
    else:
        return 0 ,'None'
    
def is_not_risky_return_lot(symbol,gap,comm):
    symbol_info = mt5.symbol_info(symbol)
    pos_risk , risky_symbol_p = positions_risk(comm)
    ord_risk , risky_symbol_o = orders_risk(comm)
    if symbol not in risky_symbol_p and symbol not in risky_symbol_o:
        av_risk = risk_amount(1/100) - pos_risk - ord_risk
        volume = av_risk/(gap / symbol_info.trade_tick_size * symbol_info.trade_tick_value + comm)
        if volume >= symbol_info.volume_min:
            f = str(symbol_info.volume_min)
            print(mt5.last_error())
            decimal =  f[::-1].find('.')
            lot = round(volume,decimal)
            if symbol_info.volume_max > lot:
                return lot
            else:
                # return symbol_info.volume_max
                return 0.01
    return None