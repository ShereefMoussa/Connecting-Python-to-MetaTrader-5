from os.path import exists
from datetime import datetime, timedelta
import pandas as pd
import pytz
import MetaTrader5 as mt5
from variables import *
from indicators import *
# from chart import chart
from indcators_chart import indcators_and_chart
# from utilities import namestr

from data_u import *




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
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
    rates_frame = rates_frame.round({"open":5, "high":5, "low":5, "close":5})
    print(type(rates_frame))
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

def is_symbols_available():
    # get all symbols
    available_symbols=mt5.symbols_get()
    # print('Symbols: ', len(available_symbols))
    Symbols_names= list(map(lambda x: x.name, available_symbols)) 

    for s in symbols_to_trade:
        if s not in Symbols_names:
            print(f'error. {s} symbol in not available')

# prepar data fun
def pull_data(data_folder,candles):
    # what is time now?
    utc_now = datetime.now(timezone) +  timedelta(hours=4)
    # loop throw symbols_to_trade
    for symbol in symbols_to_trade:
        # loop throw timeframes
        for key, timeframe in  timeframes.items():
            # check if symbol exist
            if mt5.symbol_info(symbol) is not None:
                
                # check if data file exist
                if  not exists(f'{data_folder}/{symbol}_{key}.csv'):
                    # create ver to pull data
                    globals()[f'{symbol}_{key}'] = data_last(symbol, timeframe,candles)
                    
                    # indcators_and_chart(globals()[f'{symbol}_{key}'])
                    
                    print(globals()[f'{symbol}_{key}'].tail(1))
                    
                    # save dataframe
                    globals()[f'{symbol}_{key}'].to_csv(f'{data_folder}/{symbol}_{key}.csv',index=False)
                    
                    
                else:
                    
                    # create ver to read data
                    globals()[f'{symbol}_{key}'] = pd.read_csv(f'{data_folder}/{symbol}_{key}.csv')
                    
                    # get last time data updated
                    last_time = pd.to_datetime(globals()[f'{symbol}_{key}'].iloc[-1]['time'])+ timedelta(0.000001)
                    
                    
                    # last_time = datetime.strptime(globals()[f'{symbol}_{key}'].iloc[-1]['time'], "%Y-%m-%d %H:%M:%S")
                    
                    # localize time to commpare
                    t_last = timezone.localize(last_time)
                    # check if data up to date 
                    if t_last <= utc_now:
                        # drop last row to prevent duplication
                        globals()[f'{symbol}_{key}'].drop(index=globals()[f'{symbol}_{key}'].index[-1], axis=0, inplace=True)
                        # call new data
                        globals()[f'{symbol}_{key}_new'] = data_range(symbol,timeframe ,t_last,utc_now)
                        # concat old and new
                        globals()[f'{symbol}_{key}']=pd.concat([globals()[f'{symbol}_{key}'], globals()[f'{symbol}_{key}_new']])
                        
                        #if data_production
                        if data_folder == 'data_production':
                            globals()[f'{symbol}_{key}']=globals()[f'{symbol}_{key}'].tail(candles)
                        print(globals()[f'{symbol}_{key}'].tail(1))
                        # print(globals() [f'{symbol}_{key}'].dtypes())
                        # convert time columns type
                        globals()[f'{symbol}_{key}']['time']= pd.to_datetime(globals()[f'{symbol}_{key}']['time'])
                        globals()[f'{symbol}_{key}'].set_index('time',inplace=True)
                        #  indcators and chart
                        sy_tf= namestr(globals()[f'{symbol}_{key}'],globals())
                        indcators_and_chart(globals()[f'{symbol}_{key}'],sy_tf,key,data_folder,symbol)
                        # chart(globals()[f'{symbol}_{key}'])
                        # nnnn(globals()[f'{symbol}_{key}'])
                        # print('abcdef',namestr(globals()[f'{symbol}_{key}'],globals()))

                        # save dataframe
                        globals() [f'{symbol}_{key}'].to_csv(f'{data_folder}/{symbol}_{key}.csv')
                        # chart(globals()[f'{symbol}_{key}'])
                        # input("Press Enter to continue...")

