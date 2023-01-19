# import modules
# from matplotlib.pyplot import plot
from symtable import Symbol
from modules import *
# import threading
# import files
# from orders import orders,positions
# from variables import *
# from connection import initialize_mt5 ,pull_terminal_info ,pull_account_info,pull_ter_info
# from Data import data_from, data_last,data_range,is_symbols_available,pull_data
# from symbols import symbols_get
from plotly_chart import * 
from core import *
from plot_data.app import app
print('start')
logger.info(f"start {login}")


def chart_populate_fuc():
    if __name__ == '__main__':
        app.run_server(debug=True)

# chart_populate_fuc()
t1 = threading.Thread(target= chart_populate_fuc)
t1.start()
# core()
t2 = threading.Thread(target= core)
t2.start()



# if __name__ == '__main__':
#     # chart_process = multi.Process(target=chart_populate_fuc)
#     main_process = multi.Process(target=core)
#     main_process.start()
#     # chart_process.start()
#     # chart_process.join()
#     main_process.join()
    
    
    
# def pull_second_data(data_folder,candles,symbols_to_trade,timeframes):
#     processes = []
#     # loop throw symbols_to_trade
#     for symbol in symbols_to_trade:
#         # loop throw timeframes
#         for key, time_frame in  timeframes.items():
#             second_data(data_folder,symbol,key,time_frame,candles)
#             p = multi.Process(target= second_data, args=[data_folder,symbol,key,time_frame,candles])
#             p.start()
#             processes.append(p)
#     for process in processes:
#         process.join()