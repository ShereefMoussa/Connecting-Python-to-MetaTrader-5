import numpy as np
import pandas as pd

def heikin_ashi(df,smoothing,reset_indcators):
    if reset_indcators or 'heikin_open' not in df.columns or pd.isnull(df.loc[df.index[0],'heikin_open']):
        # heikin_close
        df['heikin_close'] = ((df['open'].to_numpy() + df['high'].to_numpy() + df['low'].to_numpy() + df['close'].to_numpy())/4).round(5)
        # heikin_open
        df.loc[df.index[0],'heikin_open'] = (df.loc[df.index[0],'open'] + df.loc[df.index[0],'close'])/2
        for prow, row in zip(df.iloc[:-1].itertuples(), df.iloc[1:].itertuples()):
            df.loc[row.Index,'heikin_open'] = ((prow.heikin_open * smoothing) + prow.heikin_close)/(smoothing +1)
        # heikin_high
        df['heikin_high']=df[['heikin_open','heikin_close','high']].max(axis=1)
        # heikin_low
        df['heikin_low']=df[['heikin_open','heikin_close','low']].min(axis=1)
    else:
        for prow, row in zip(df.loc[df.heikin_low.last_valid_index():].iloc[:-1].itertuples(), df.loc[df.heikin_low.last_valid_index():].iloc[1:].itertuples()):
            i = row.Index
            # heikin_close
            df.loc[i,'heikin_close'] = round((row.open + row.high + row.low + row.close)/4, 5)
            # heikin_open
            df.loc[i,'heikin_open'] = ((prow.heikin_open * smoothing) + prow.heikin_close)/(smoothing +1)
            # heikin_high
            df.loc[i,'heikin_high'] = max(row.heikin_open, row.heikin_close, row.high)
            # heikin_low
            df.loc[i,'heikin_low'] = min(row.heikin_open, row.heikin_close, row.low)
            
            
# def heikin_ashi_test(df,smoothing,reset_indcators):
#     # heikin_close
#     df[f'heikin_close_{smoothing}'] = ((df['open'].to_numpy() + df['high'].to_numpy() + df['low'].to_numpy() + df['close'].to_numpy())/4).round(5)
#     # heikin_open
#     df.loc[df.index[0],f'heikin_open_{smoothing}'] = (df.loc[df.index[0],'open'] + df.loc[df.index[0],'close'])/2
#     for i, row in df.iloc[1:].iterrows():
#         df.loc[i,f'heikin_open_{smoothing}'] = (
#             (df.loc[i,f'heikin_open_{smoothing}'] * smoothing) + 
#             df.loc[df.index[df.index.get_loc(i)-1],f'heikin_close_{smoothing}'])/(smoothing +1)
#     # heikin_high
#     df[f'heikin_high_{smoothing}']=df[[f'heikin_open_{smoothing}',f'heikin_close_{smoothing}','high']].max(axis=1)
#     # heikin_low
#     df[f'heikin_low_{smoothing}']=df[[f'heikin_open_{smoothing}',f'heikin_close_{smoothing}','low']].min(axis=1)


def heikin_ashi_period(df,smoothing):
    
    # heikin_close
    heikin_close = ((df['open'].to_numpy() + df['high'].to_numpy() + df['low'].to_numpy() + df['close'].to_numpy())/4).round(5)
    # heikin_open
    heikin_open = (df.loc[df.index[0],'open'] + df.loc[df.index[0],'close'])/2
    for prow, row in zip(df.iloc[:-1].itertuples(), df.iloc[1:].itertuples()):
        heikin_open = np.append(heikin_open,[  ((prow.heikin_open * smoothing) + prow.heikin_close)/(smoothing +1)  ])
        
    # heikin_high
    heikin_high = df[['heikin_open','heikin_close','high']].max(axis=1)
    # heikin_low
    heikin_low = df[['heikin_open','heikin_close','low']].min(axis=1)
    
    return heikin_close, heikin_open, heikin_high, heikin_low