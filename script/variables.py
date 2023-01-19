# import modules
from modules import *

# raw, build, production, p_build
production = 'production'
reset_indicators = False
data_build_count = 3000
data_production_count = 500

login = 41649154
server = "AdmiralMarkets-Demo"
password = "LuQ0gT4Tu4bE"

symbols_to_trade = ["EURUSD-Z"]
# ,"GBPUSD-Z", "USDCAD-Z","USDJPY-Z","USDCHF-Z" ,"AUDUSD-Z",
#                     "BRENT-Z", "WTI-Z", "EURGBP-Z", "CRUDOIL-Z", "EURJPY-Z",
#                     "USDBGN-Z", "USDJOD-Z", "USDVND-Z" ]
symbols_to_build = ["EURUSD-Z"]
# , "GBPUSD-Z", "USDCAD-Z","USDJPY-Z"]
minimum_candles = 2190
forex_symbols = ["EURUSD-Z"]
# timeframes = {'1M':mt5.TIMEFRAME_M1,'5M':mt5.TIMEFRAME_M5,'15M':mt5.TIMEFRAME_M15,'30M':mt5.TIMEFRAME_M30,'1H':mt5.TIMEFRAME_H1,'4H':mt5.TIMEFRAME_H4,'1D':mt5.TIMEFRAME_D1}
# timeframes = {'1M':mt5.TIMEFRAME_M1,
            #   '5M':mt5.TIMEFRAME_M5,
            #   '15M':mt5.TIMEFRAME_M15,
            #   '30M':mt5.TIMEFRAME_M30,
            #   '1H':mt5.TIMEFRAME_H1,
            #   '4H':mt5.TIMEFRAME_H4,
            #   '1D':mt5.TIMEFRAME_D1}

e_point = {
    'EURUSD-Z', 0.00001
}


tf = {'1M':['5M','30M','T10'],
    '5M':['30M','4H','1M'],
    '15M':['4H','1D','5M'],
    '30M':['4H','1D','5M'],
    '1H':['4H','1D','5M'],
    '4H':['1D','W1','30M'],
    '1D':['W1','MO','4H']}
timeframes = {'1M':mt5.TIMEFRAME_M1, '30M':mt5.TIMEFRAME_M30}

timezone = pytz.timezone("Etc/UTC")
raw_year = 2022 
minute_bars = 1000

all_risk = 1/100
risk_per_trade = 0.5/100
commission = 6



duration = 2000  # milliseconds
freq = 1000  # Hz