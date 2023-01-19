import talib 
from finta import TA
import ta
import pandas as pd 

def ema_ind(df,period):
        return talib.EMA(df['close'],period).round(5)

def sma_ind(df,period):
        return talib.SMA(df['ema_200'],period).round(5)

def macd_ind(df):
        macd_ind ,d,d2 = talib.MACD(df['close'])
        macd_ind = macd_ind.round(6)*1000000
        df['macd'] = macd_ind.fillna(0).astype(int)

def rsi_ind(df,timeperiod):
        df['rsi'] = talib.RSI(df['close'],timeperiod).round(1).fillna(0).astype(int)

def atr_ind(df,timeperiod,sma_fast_period,sma_slow_period):
        df['atr'] = talib.ATR(df['high'],df['low'],df['close'],timeperiod).round(5).fillna(0)
        df[f'atr_smma_fast'] = TA.SMA(df, sma_fast_period, 'atr').round(5)
        df[f'atr_smma_slow'] = TA.SMMA(df, sma_slow_period, 'atr').round(5)
        
def kama(df,period):
        return talib.KAMA(df['close'], period)

def stc(column, window_slow, window_fast, cycle, smooth1, smooth2, fillna):
        return ta.trend.stc(column, window_slow, window_fast, cycle, smooth1, smooth2, fillna)









def bolinger_kama(df,ma_p,kama_p):

        bb = TA.BBANDS(df,ma_p, TA.KAMA(df, kama_p))
        try:
                del df['BB_UPPER']
        except:
                pass
        try:
                del df['BB_MIDDLE']
        except:
                pass
        try:
                del df['BB_LOWER']
        except:
                pass
        df = pd.concat([df,bb], axis=1)