from modules import *
from variables import *
from indcators_chart import *
print('start_fake')

def pull_data(data_folder,candles):
    # loop throw symbols_to_trade
    for symbol in symbols_to_trade:
        # loop throw timeframes
        for key, timeframe in  timeframes.items():
            # check if symbol exist
            # if mt5.symbol_info(symbol) is not None:
                
                # check if data file exist
                if  not exists(f'{data_folder}/{symbol}_{key}.csv'):
                    pass
                    
                else:
                    
                    # create ver to read data
                    globals()[f'{symbol}_{key}'] = pd.read_csv(f'{data_folder}/{symbol}_{key}.csv')
                    
                    # get last time data updated
                    last_time = pd.to_datetime(globals()[f'{symbol}_{key}'].iloc[-1]['time'])+ timedelta(0.000001)
                    
                    
                    # last_time = datetime.strptime(globals()[f'{symbol}_{key}'].iloc[-1]['time'], "%Y-%m-%d %H:%M:%S")
                    
                        #if data_production
                        
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
                    # globals() [f'{symbol}_{key}'].to_csv(f'{data_folder}/{symbol}_{key}.csv')
                    # chart(globals()[f'{symbol}_{key}'])
                    # input("Press Enter to continue...")

pull_data('data_production', data_build_count)