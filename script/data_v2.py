from datetime import datetime, timedelta
from variables import *
from data_u import data_last, data_range
from indicators_and_strategies import *


# data first fun
def first_data(data_folder,symbol,key,time_frame,candles):
    if mt5.symbol_info(symbol) is not None:
        # check if data file exist
        if not exists(f'{data_folder}/{symbol}_{key}.csv'):
            # create ver to pull data
            globals()[f'{symbol}_{key}'] = data_last(symbol, time_frame, candles)
            globals()[f'{symbol}_{key}']['time']= pd.to_datetime(globals()[f'{symbol}_{key}']['time'])
            globals()[f'{symbol}_{key}'].set_index('time',inplace=True)
            indicators(globals()[f'{symbol}_{key}'],key,data_folder,symbol)
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
                globals()[f'{symbol}_{key}'] = globals()[f'{symbol}_{key}'].tail(candles)
                # indicators(globals()[f'{symbol}_{key}'],key,data_folder,symbol)                    
                # convert time columns type
                globals()[f'{symbol}_{key}']['time']= pd.to_datetime(globals()[f'{symbol}_{key}']['time'])
                globals()[f'{symbol}_{key}'].set_index('time',inplace=True)
                # print(globals()[f'{symbol}_{key}'].tail(1))
                indicators(globals()[f'{symbol}_{key}'],key,data_folder,symbol)
                # save dataframe
                globals() [f'{symbol}_{key}'].to_csv(f'{data_folder}/{symbol}_{key}.csv')

# data first fun
def second_data(data_folder,symbol,key,time_frame,candles):
    if mt5.symbol_info(symbol) is not None:
        # check if data file exist
        if not exists(f'{data_folder}/{symbol}_{key}.csv'):
            # create ver to pull data
            globals()[f'{symbol}_{key}'] = data_last(symbol, time_frame, candles)
            globals()[f'{symbol}_{key}']['time']= pd.to_datetime(globals()[f'{symbol}_{key}']['time'])
            globals()[f'{symbol}_{key}'].set_index('time',inplace=True)
            indicators(globals()[f'{symbol}_{key}'],key,data_folder,symbol)
            # save dataframe
            globals()[f'{symbol}_{key}'].to_csv(f'{data_folder}/{symbol}_{key}.csv',index=False)
        else:
            try:
                # create ver to read data
                globals()[f'{symbol}_{key}'] = pd.read_csv(f'{data_folder}/{symbol}_{key}.csv')
            except:
                os.remove(f'{data_folder}/{symbol}_{key}.csv')
                first_data(data_folder,symbol,key,time_frame,candles)
                globals()[f'{symbol}_{key}'] = pd.read_csv(f'{data_folder}/{symbol}_{key}.csv')
                
            # get last time data updated
            utc_now = datetime.now(timezone) +  timedelta(hours=4)
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
                globals()[f'{symbol}_{key}'] = globals()[f'{symbol}_{key}'].tail(candles)
                # print(globals()[f'{symbol}_{key}'].tail(1))
                globals()[f'{symbol}_{key}']['time']= pd.to_datetime(globals()[f'{symbol}_{key}']['time'])
                globals()[f'{symbol}_{key}'].set_index('time',inplace=True)
                indicators(globals()[f'{symbol}_{key}'],key,data_folder,symbol)
                strategies(globals()[f'{symbol}_{key}'],key,data_folder,symbol)                    
                # convert time columns type
                # save dataframe
                globals() [f'{symbol}_{key}'].to_csv(f'{data_folder}/{symbol}_{key}.csv')

# 1st data fun
def pull_first_data(data_folder,candles,symbols_to_trade,timeframes):
    processes = []
    # loop throw symbols_to_trade
    for symbol in symbols_to_trade:
        # loop throw time frames
        for key, time_frame in  timeframes.items():
            first_data(data_folder,symbol,key,time_frame,candles)
    #         p = multi.Process(target=first_data, args=[data_folder,symbol,key,time_frame,candles])
    #         p.start()
    #         processes.append(p)
    # for process in processes:
    #     process.join()

# 2nd data fun
def pull_second_data(data_folder,candles,symbols_to_trade,timeframes):
    processes = []
    # loop throw symbols_to_trade
    for symbol in symbols_to_trade:
        # loop throw timeframes
        for key, time_frame in  timeframes.items():
            second_data(data_folder,symbol,key,time_frame,candles)
    #         p = multi.Process(target= second_data, args=[data_folder,symbol,key,time_frame,candles])
    #         p.start()
    #         processes.append(p)
    # for process in processes:
    #     process.join()


##########################################################################################
# data first fun
def raw_data(data_folder,symbol,key,time_frame,candles):
    if mt5.symbol_info(symbol) is not None:
        # check if data file exist
        if not exists(f'{data_folder}/{symbol}_{key}.csv'):
            # create ver to pull data
            globals()[f'{symbol}_{key}'] = data_last(symbol, time_frame, candles)
            # save dataframe
            globals()[f'{symbol}_{key}'].to_csv(f'{data_folder}/{symbol}_{key}.csv',index=False)
        else:
            try:
                # create ver to read data
                globals()[f'{symbol}_{key}'] = pd.read_csv(f'{data_folder}/{symbol}_{key}.csv')
            except:
                os.remove(f'{data_folder}/{symbol}_{key}.csv')
                first_data(data_folder,symbol,key,time_frame,candles)
                globals()[f'{symbol}_{key}'] = pd.read_csv(f'{data_folder}/{symbol}_{key}.csv')
            # get last time data updated
            utc_now = datetime.now(timezone) +  timedelta(hours=4)
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
                globals()[f'{symbol}_{key}'] = globals()[f'{symbol}_{key}'].tail(candles)
                # indicators(globals()[f'{symbol}_{key}'],key,data_folder,symbol)                    
                # convert time columns type
                globals()[f'{symbol}_{key}']['time']= pd.to_datetime(globals()[f'{symbol}_{key}']['time'])
                globals()[f'{symbol}_{key}'].set_index('time',inplace=True)
                print(globals()[f'{symbol}_{key}'].tail(1))
                # save dataframe
                globals() [f'{symbol}_{key}'].to_csv(f'{data_folder}/{symbol}_{key}.csv')
                
                
def pull_raw_data(data_folder,candles,symbols_to_trade,timeframes):
    processes = []
    # loop throw symbols_to_trade
    for symbol in symbols_to_trade:
        # loop throw timeframes
        for key, time_frame in  timeframes.items():
            
            # raw_candle = datetime.now().date() - datetime(raw_year, 1,1).date()
            # print('raw',raw_candle)
            # if key == '1M':
            #     raw_candle = raw_candle.days * 24 * 60
            # elif key == '5M':
            #     raw_candle = raw_candle.days * 24 * 60 /5 +250
            # elif key == '15M':
            #     raw_candle = raw_candle.days * 24 * 60 /15 +250
            # elif key == '30M':
            #     raw_candle = raw_candle.days * 24 * 60 /30 +250
            # elif key == '1H':
            #     raw_candle = raw_candle.days * 24 +250
            # elif key == '4H':
            #     raw_candle = raw_candle.days * 24 /4 +250
            # elif key == '1D':
            #     raw_candle = raw_candle.days +250
            # print('new_raw',raw_candle)
            
            if key == '1M':
                raw_candle = minute_bars
            elif key == '5M':
                raw_candle = minute_bars / 5 +250
            elif key == '15M':
                raw_candle = minute_bars / 15 +250
            elif key == '30M':
                raw_candle = minute_bars / 30 +250
            elif key == '1H':
                raw_candle = minute_bars / 60 +250
            elif key == '4H':
                raw_candle = minute_bars / (4*60) +250
            elif key == '1D':
                raw_candle = minute_bars / (4*60*24) +250
            
            
            raw_data(data_folder,symbol,key,time_frame,raw_candle)
    #         p = multi.Process(target= second_data, args=[data_folder,symbol,key,time_frame,candles])
    #         p.start()
    #         processes.append(p)
    # for process in processes:
    #     process.join()
    
    
############################################################################
def build_data_1(data_folder,build_folder,symbol,key,time_frame):

        # try:
            # create ver to read data
    globals()[f'{symbol}_{key}'] = pd.read_csv(f'{data_folder}/{symbol}_{key}.csv')
    globals()[f'{symbol}_{key}']['time']= pd.to_datetime(globals()[f'{symbol}_{key}']['time'])
    globals()[f'{symbol}_{key}'].set_index('time',inplace=True)
    indicators(globals()[f'{symbol}_{key}'],key,data_folder,symbol)
    globals() [f'{symbol}_{key}'].to_csv(f'{build_folder}/{symbol}_{key}.csv')
        # except:
        #     print('error data fail',f'{symbol}_{key}')
        

def build_data_2(data_folder,build_folder,symbol,key,time_frame):
    if key == '1M':
        print(symbol)
        # try:
            # create ver to read data
        globals()[f'{symbol}_{key}'] = pd.read_csv(f'{build_folder}/{symbol}_{key}.csv')
        globals()[f'{symbol}_{key}']['time']= pd.to_datetime(globals()[f'{symbol}_{key}']['time'])
        globals()[f'{symbol}_{key}'].set_index('time',inplace=True)
        strategies(globals()[f'{symbol}_{key}'],key,build_folder,symbol)
        globals()[f'{symbol}_{key}'].to_csv(f'{build_folder}/{symbol}_{key}.csv')

        # except:
        #     print('error data fail',f'{symbol}_{key}')


def b_build_data(data_folder, build_folder,symbols_to_trade,timeframes):
    processes = []
    # loop throw symbols_to_trade
    print("start build 1")
    for symbol in symbols_to_build:
        # loop throw time frames
        for key, time_frame in  timeframes.items():
            build_data_1(data_folder, build_folder,symbol,key,time_frame)
    #         p = multi.Process(target=first_data, args=[data_folder,symbol,key,time_frame])
    #         p.start()
    #         processes.append(p)
    # for process in processes:
    #     process.join()
    print("start build 2")
    for symbol in symbols_to_build:
        # loop throw time frames
        for key, time_frame in  timeframes.items():
            build_data_2(build_folder, build_folder, symbol,key,time_frame)
    #         p = multi.Process(target=first_data, args=[data_folder,symbol,key,time_frame])
    #         p.start()
    #         processes.append(p)
    # for process in processes:
    #     process.join()
    