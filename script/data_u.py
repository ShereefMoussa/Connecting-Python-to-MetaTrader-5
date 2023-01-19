from modules import *
from variables import *

# def get_server_time():
#     return pd.to_datetime(mt5.symbol_info_tick('EURUSD-Z').time, unit='s')

def data_from(symbol,TF,year,month,day,hour,candles):
    # set time zone to UTC
    # create 'datetime' object in UTC time zone to avoid the implementation of a local time zone offset
    utc_from = datetime(year,month,day,hour, tzinfo=timezone)
    rates = mt5.copy_rates_from(symbol, TF, utc_from, candles)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
    rates_frame = rates_frame.round({"open":5, "high":5, "low":5, "close":5})
    return rates_frame

def data_last(symbol,TF,candles):
    rates = mt5.copy_rates_from_pos(symbol,TF, 0, candles)
    rates_frame = pd.DataFrame(rates)
    print('cccccc',rates_frame)
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
    rates_frame = rates_frame.round({"open":5, "high":5, "low":5, "close":5})
    return rates_frame

def data_range(symbol,TF,date_from,date_to):
    rates = mt5.copy_rates_range(symbol,TF,date_from,date_to)
    # print(rates)
    # if rates == 
    rates_frame = pd.DataFrame(rates,columns=['time','open','high','low','close','tick_volume','spread','real_volume'])
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
    rates_frame = rates_frame.round({"open":5, "high":5, "low":5, "close":5})
    rates_frame.set_index('time')
    # print(rates_frame)
    return rates_frame