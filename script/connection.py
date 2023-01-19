# import modules
from modules import *

from variables import login,server,password

def initialize_mt5():
    # establish MetaTrader 5 connection to a specified trading account
    if not mt5.initialize(login=login, server=server,password=password):
        print("initialize() failed, error code =",mt5.last_error())
        quit() 
    
def pull_ter_info(property):
    return mt5.terminal_info()._asdict()[property]
    
def pull_account_info(property):
    return mt5.account_info()._asdict()[property]
    # return mt5.account_info().property

def pull_terminal_info():
    # display data on MetaTrader 5 version
    print("MetaTrader5 package author: ",mt5.__author__,"MetaTrader5 package version: ",mt5.__version__)
    terminal_info=pd.DataFrame(list(mt5.terminal_info()._asdict().items()),columns=['property','value'])
    terminal_info = terminal_info.set_index('property')  
    print("terminal_info() as dataframe:")
    print(terminal_info)

def pull_account_info():
    account_info=pd.DataFrame(list(mt5.account_info()._asdict().items()),columns=['property','value'])
    account_info = account_info.set_index('property')       
    print('account_info')
    print(account_info)

