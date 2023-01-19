from modules import*
from variables import *
from data_u import *


utc_now = datetime.now(timezone) +  timedelta(hours=4)
symbols_to_trade = ["EURUSD-Z"]
timeframes = {'1M':mt5.TIMEFRAME_M1, '30M':mt5.TIMEFRAME_M30}
utc_from = datetime(2022, 6, 9, tzinfo=timezone)

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
                    globals()[f'{symbol}_{key}'] = data_range(symbol,timeframe,utc_from,utc_now)
                    
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
                        
                        print(globals()[f'{symbol}_{key}'].tail(1))
                        # convert time columns type
                        globals()[f'{symbol}_{key}']['time']= pd.to_datetime(globals()[f'{symbol}_{key}']['time'])
                        globals()[f'{symbol}_{key}'].set_index('time',inplace=True)
                        #  indcators and chart
                        # sy_tf= namestr(globals()[f'{symbol}_{key}'],globals())
                        # save dataframe
                        globals() [f'{symbol}_{key}'].to_csv(f'{data_folder}/{symbol}_{key}.csv')
      




def core():
    while True:
        
        mt5.initialize()
        authorized=mt5.login(login=login, server=server, password=password,timeout=86400000)  # the terminal database password is applied if connection data is set to be remembered
        if not authorized:
            print("initialize() failed, error code =", mt5.last_error())
        else: print('you are authorized')

        while authorized:
            pull_data('data_ai',11)
            sys.exit()
core()