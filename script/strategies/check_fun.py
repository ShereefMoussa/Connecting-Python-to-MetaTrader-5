def check_tf_heikin_candle(row):
        if row.heikin_close > row.heikin_open:
            return 'bull'
        else:
            return 'bear'
        
def check_heikin_candle(row):
    if (row.heikin_close > row.heikin_open) and (
        (row.heikin_low - row.heikin_open)*2 < (row.heikin_close - row.heikin_open)) and(
            (row.heikin_close - row.heikin_open) > (row.heikin_high - row.heikin_close)):
        return 'bull'
    elif (row.heikin_close < row.heikin_open) and (
            (row.heikin_high - row.heikin_open)*2 < (row.heikin_open - row.heikin_close)) and(
                (row.heikin_open - row.heikin_close) > (row.heikin_close - row.heikin_low)):
        return 'bear'
    else:
        return 'not valid candle'
    
def check_volatility_v(row):
    if row.atr > row.atr_sma:
        return True
    else:
        return False
    
def check_low_ema125_bull(df,row):
    if row.ema_117 >= df.loc[df.index[df.index.get_loc(row.Index)-4]:row.Index,'low'].min():
        return True
    else:
        return False
    
def check_low_ema125_bear(df,row):
    if row.ema_117 <= df.loc[df.index[df.index.get_loc(row.Index)-4]:row.Index,'high'].max():
        return True
    else:
        return False
    
def check_ema270_bull(df,row,back_candle):
    if row.ema_270 < df.loc[df.index[df.index.get_loc(row.Index)-back_candle]:row.Index,'low'].min():
        return True
    else:
        return False
    
def check_ema270_bear(df,row,back_candle):
    if row.ema_270 > df.loc[df.index[df.index.get_loc(row.Index)-back_candle]:row.Index,'high'].max():
        return True
    else:
        return False

def check_column_bull(df, row, column, back_candle, p):
    for i in range(back_candle + 1):
        if df.loc[df.index[df.index.get_loc(row.Index)-i], column]+p*4 >= df.loc[df.index[df.index.get_loc(row.Index)-i],'low']:
            return True
    return False

def check_column_bear(df, row, column, back_candle, p):
    for i in range(back_candle + 1):
        if df.loc[df.index[df.index.get_loc(row.Index)-i], column]-p*4 <= df.loc[df.index[df.index.get_loc(row.Index)-i],'high']:
            return True
    return False

def round_dismal(num_to_be_rounded, round_dismal):
    f = str(round_dismal)
    decimal =  f[::-1].find('.')
    return round(num_to_be_rounded, decimal)
    
def get_stop_lose(directions, df, candle_begin, tick, back_candle,num_of_tick):
    if directions == "up":
        return df.loc[df.index[df.index.get_loc(candle_begin)- back_candle]:candle_begin , 'low'].min() - num_of_tick
    elif directions == "down":
        return df.loc[df.index[df.index.get_loc(candle_begin)- back_candle]:candle_begin , 'high'].max() + num_of_tick
    else:
        print("wrong stop lose")