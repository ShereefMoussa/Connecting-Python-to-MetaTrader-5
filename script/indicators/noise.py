import numpy as np
import pandas as pd
from finta import TA


def price_density(df,period):
    
    if 'price_density' not in df.columns:
        df['price_density'] = np.nan
        
    for row in df.loc[df.index[period]: ].loc[df['price_density'].last_valid_index(): ].itertuples():
        df_period = df.iloc[df.index.get_loc(row.Index)-period :df.index.get_loc(row.Index)]
        deff = df_period['high'] - df_period['low']
        bast = deff.sum()
        pmax = df_period['high'].max()
        pmin = df_period['low'].min()
        # print('bast',bast)
        # print('pmax',pmax)
        # print('pmin',pmin)
        df.loc[row.Index,'price_density'] = bast/(pmax - pmin)
            
            
            
        # if row.Index != df.index[-1]:
        
        #     df_period = df.iloc[df.index.get_loc(row.Index)-period+1 :df.index.get_loc(row.Index)+1]
        #     deff = df_period['high'] - df_period['low']
        #     bast = deff.sum()    
        #     pmax = df_period['high'].max()
        #     pmin = df_period['low'].min()
        #     # print('bast',bast)
        #     # print('pmax',pmax)
        #     # print('pmin',pmin)
        #     df.loc[row.Index,'price_density'] = bast/(pmax - pmin)
            
        # else:
        #     df_period = df.loc[df.index[df.index.get_loc(row.Index)-period+1]:]
        #     deff = df_period['high'] - df_period['low']
        #     bast = deff.sum()    
        #     pmax = df_period['high'].max()
        #     pmin = df_period['low'].min()
        #     # print('bast',bast)
        #     # print('pmax',pmax)
        #     # print('pmin',pmin)
        #     df.loc[row.Index,'price_density'] = bast/(pmax - pmin)
        
        
def efficiency_ratio(df,period):
    
    return TA.ER(df, period)
    # direction = df['close'].diff(period).abs()
    # # volatility = pd.rolling_sum(df['close'].diff().abs(), period)
    # volatility =  df['close'].diff().abs().rolling(period).sum()  #pd.rolling_sum(df['close'].diff().abs(), period)
    
    # df['efficiency_ratio'] = direction / volatility
    
    
    
    # if 'efficiency_ratio' not in df.coloumes:
    #     df['efficiency_ratio'] = np.nan
        
    # for row in df.loc[df.index[period]: ].loc[df['efficiency_ratio'].last_valid_index(): ].itertuples():
        
        # if row.Index != df.index[-1]:
        
        #     df_period = df.iloc[df.index.get_loc(row.Index)-period+1 :df.index.get_loc(row.Index)+1]
        #     deff = df_period['high'] - df_period['low']
        #     bast = deff.sum()    
        #     pmax = df_period['high'].max()
        #     pmin = df_period['low'].min()
        #     # print('bast',bast)
        #     # print('pmax',pmax)
        #     # print('pmin',pmin)
        #     df.loc[row.Index,'price_density'] = bast/(pmax - pmin)
            
        # else:
        #     df_period = df.loc[df.index[df.index.get_loc(row.Index)-period+1]:]
        #     deff = df_period['high'] - df_period['low']
        #     bast = deff.sum()    
        #     pmax = df_period['high'].max()
        #     pmin = df_period['low'].min()
        #     # print('bast',bast)
        #     # print('pmax',pmax)
        #     # print('pmin',pmin)
        #     df.loc[row.Index,'price_density'] = bast/(pmax - pmin)