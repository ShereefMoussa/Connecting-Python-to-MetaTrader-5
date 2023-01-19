import talib
import ta
from finta import TA


def adx_wilder(df,period):
    adx_w = ta.trend.ADXIndicator(df.high,df.low,df.close,period)
    return adx_w.adx(), adx_w.adx_pos(), adx_w.adx_neg() 

def smma(df,column,period):
    return TA.SMMA(df, period, column).round(5)











# def adx_wilder(df):
    
#     def adx_wilder_core(df,row):
#         p_high = df.loc[df.index[df.index.get_loc(row.Index)-1],'high']
#         p_low = df.loc[df.index[df.index.get_loc(row.Index)-1],'low']
#         df.loc[row.Index,'dm+'] = row.high - p_high if row.high - p_high > p_low - row.low  else 0 
#         df.loc[row.Index,'dm-'] = p_low - row.low   if p_low - row.low  > row.high - p_high  else 0 
        
#     df['tr'] = talib.TRANGE(df.high,df.low,df.close)
#     df['str'] = talib.SMA(df['tr'],14)
    
#     for row in df.iloc[1:].itertuples():
#         adx_wilder_core(df,row)
    
#     # Plus_D(i) = SMMA(dm_plus, Period_ADX,i)/ATR(i)*100
#     df['di+'] = talib.SMA(df['dm+'],14)/df['str']*100
#     # Minus_D(i) = SMMA(dm_minus, Period_ADX,i)/ATR(i)*100
#     df['di-'] = talib.SMA(df['dm-'],14)/df['str']*100
#     # DX(i) = ABS(Plus_D(i) - Minus_D(i))/(Plus_D(i) + Minus_D(i)) * 100
#     df['dx'] = abs(df['di+'] - df['di-'])/(df['di+'] + df['di-'])*100
#     # ADX(i) = SMMA(DX, Period_ADX, i)
#     df['adx'] = talib.SMA(df['dx'],14)