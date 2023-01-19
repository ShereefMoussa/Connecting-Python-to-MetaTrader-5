from datetime import datetime, timedelta
from variables import *
from data_u import *
from indicators_and_strategies import *
import MetaTrader5 as mt5
from os.path import exists
import os
import pandas as pd




# 1st data fun
def p_build(data_folder, build_folder, candles, symbols_to_trade,timeframes):
    # candles = mt5.terminal_info().maxbars 
        # data first fun
    def first_data(data_folder, build_folder, symbol,key,time_frame,candles):
        if mt5.symbol_info(symbol) is not None:
            # check if data file exist
            if not exists(f'{data_folder}/{symbol}_{key}.csv'):
                # create ver to pull data
                globals()[f'{symbol}_{key}'] = data_last(symbol, time_frame, candles)
                globals()[f'{symbol}_{key}']['time']= pd.to_datetime(globals()[f'{symbol}_{key}']['time'])
                globals()[f'{symbol}_{key}'].set_index('time',inplace=True)
                # indicators(globals()[f'{symbol}_{key}'],key,data_folder,symbol)
                # print(globals()[f'{symbol}_{key}'].tail(1))
                # save dataframe
                globals()[f'{symbol}_{key}'].to_csv(f'{data_folder}/{symbol}_{key}.csv')
            else:
                try:
                    # create ver to read data
                    globals()[f'{symbol}_{key}'] = pd.read_csv(f'{data_folder}/{symbol}_{key}.csv')
                except:
                    os.remove(f'{data_folder}/{symbol}_{key}.csv')
                    first_data(data_folder,symbol,key,time_frame,candles)
                    globals()[f'{symbol}_{key}'] = pd.read_csv(f'{data_folder}/{symbol}_{key}.csv')
                if len(globals()[f'{symbol}_{key}']) < candles:
                    os.remove(f'{data_folder}/{symbol}_{key}.csv')
                    first_data(data_folder,symbol,key,time_frame,candles)
                    globals()[f'{symbol}_{key}'] = pd.read_csv(f'{data_folder}/{symbol}_{key}.csv')
                # get last time data updated
                utc_now = datetime.now(timezone) +  timedelta(hours=4)
                # print("ttttt",globals()[f'{symbol}_{key}'].iloc[-1])
                last_time = pd.to_datetime(globals()[f'{symbol}_{key}'].iloc[-1]['time'])+ timedelta(0.000001)                    
                # localize time to commpare
                t_last = timezone.localize(last_time)
                # check if data up to date 
                if t_last <= utc_now:
                    # drop last row to prevent duplication
                    globals()[f'{symbol}_{key}'].drop(index=globals()[f'{symbol}_{key}'].index[-1], axis=0, inplace=True)
                    # call new data
                    globals()[f'{symbol}_{key}_new'] = data_range(symbol,time_frame, t_last,utc_now)
                    # print(globals()[f'{symbol}_{key}_new'].tail(1))
                    # concat old and new
                    globals()[f'{symbol}_{key}']=pd.concat([globals()[f'{symbol}_{key}'], globals()[f'{symbol}_{key}_new']])
                    # globals()[f'{symbol}_{key}'] = globals()[f'{symbol}_{key}'].tail(candles)
                    # indicators(globals()[f'{symbol}_{key}'],key,data_folder,symbol)                    
                    # convert time columns type
                    globals()[f'{symbol}_{key}']['time']= pd.to_datetime(globals()[f'{symbol}_{key}']['time'])
                    globals()[f'{symbol}_{key}'].set_index('time',inplace=True)
                    # print(globals()[f'{symbol}_{key}'].tail(1))
                    # indicators(globals()[f'{symbol}_{key}'],key,data_folder,symbol)
                    # save dataframe
                    globals() [f'{symbol}_{key}'].to_csv(f'{data_folder}/{symbol}_{key}.csv')

    # data first fun
    def second_data(data_folder, build_folder, symbol,key,time_frame,candles):
        
                globals()[f'{symbol}_{key}'] = pd.read_csv(f'{data_folder}/{symbol}_{key}.csv')
                # get last time data updated
                globals()[f'{symbol}_{key}']['time']= pd.to_datetime(globals()[f'{symbol}_{key}']['time'])
                globals()[f'{symbol}_{key}'].set_index('time',inplace=True)
                strategies(globals()[f'{symbol}_{key}'],key,data_folder,symbol) 
                indicators(globals()[f'{symbol}_{key}'],key,data_folder,symbol)                   
                # convert time columns type
                # save dataframe
                globals() [f'{symbol}_{key}'].to_csv(f'{build_folder}/{symbol}_{key}.csv')
                    
                    
    def third_data(data_folder, build_folder, symbol,key,time_frame,candles):

                globals()[f'{symbol}_{key}'] = pd.read_csv(f'{build_folder}/{symbol}_{key}.csv')
                # get last time data updated
                globals()[f'{symbol}_{key}']['time']= pd.to_datetime(globals()[f'{symbol}_{key}']['time'])
                globals()[f'{symbol}_{key}'].set_index('time',inplace=True)
                strategies(globals()[f'{symbol}_{key}'],key,build_folder,symbol)                    
                # convert time columns type
                # save dataframe
                globals() [f'{symbol}_{key}'].to_csv(f'{build_folder}/{symbol}_{key}.csv')
    
    
    
    
    
    processes = []
    # loop throw symbols_to_trade
    for symbol in symbols_to_trade:
        # loop throw time frames
        for key, time_frame in  timeframes.items():
            first_data(data_folder, build_folder, symbol,key,time_frame,candles)
    #         p = multi.Process(target=first_data, args=[data_folder,symbol,key,time_frame,candles])
    #         p.start()
    #         processes.append(p)
    # for process in processes:
    #     process.join()



    for symbol in symbols_to_trade:
        # loop throw time frames
        for key, time_frame in  timeframes.items():
            second_data(data_folder, build_folder, symbol,key,time_frame,candles)
    #         p = multi.Process(target=first_data, args=[data_folder,symbol,key,time_frame,candles])
    #         p.start()
    #         processes.append(p)
    # for process in processes:
    #     process.join()



    for symbol in symbols_to_trade:
        # loop throw time frames
        for key, time_frame in  timeframes.items():
            third_data(data_folder, build_folder, symbol,key,time_frame,candles)
    #         p = multi.Process(target=first_data, args=[data_folder,symbol,key,time_frame,candles])
    #         p.start()
    #         processes.append(p)
    # for process in processes:
    #     process.join()


    