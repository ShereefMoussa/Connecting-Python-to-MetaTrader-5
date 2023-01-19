from modules import *
from variables import *
from Data import data_from, data_last,data_range,is_symbols_available,pull_data
from data_v2 import *
from p_build import p_build


def authorized():
    mt5.initialize()
    authorized_user = mt5.login(login=login, server=server, password=password,timeout=10000)  # the terminal database password is applied if connection data is set to be remembered
    if not authorized_user:
        print("initialize() failed, error code =", mt5.last_error())
        if mt5.last_error()[0] == -10004:
            connection_lost = True
            print('connection lost =', connection_lost)
        elif mt5.last_error()[0] == -2:
            print('invalid password or user or server')
        return False
    else:
        # print('you are authorized')
        return True


def core():
    
    connection_lost = True
    while True:
        
        while authorized():
            is_symbols_available()
            
            if production == 'raw':
                pull_raw_data('data_ai', data_build_count,symbols_to_trade,timeframes)
                sys.exit()
                
            elif production == 'p_build':
                p_build('p_raw_data', 'p_processed_data',data_build_count, symbols_to_build,timeframes)
                sys.exit()
                
            elif production == 'build':
                b_build_data('clean_data', 'data_ai',symbols_to_build,timeframes)
                winsound.Beep(800, 500)
                time.sleep(.5)
                winsound.Beep(800, 500)
                time.sleep(.5)
                winsound.Beep(freq, duration)
                sys.exit()
                
            elif production == 'production':
                # symbols_get()
                # positions()
                move_tp2_to_tp1(30)
                # move_sl_to_entry()
                if connection_lost:
                    pull_first_data('data_production', data_production_count,symbols_to_trade,timeframes)
                    connection_lost = False
                    print('connection lost =', connection_lost)
                    # sys.exit()
                pull_second_data('data_production', data_production_count,symbols_to_trade,timeframes)
                # if not production:
                    
                #     break
                # print(mt5.last_error())
                time.sleep(5)
