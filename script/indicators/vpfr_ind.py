import numpy as np
from indicators.utilities import *

def vpfr_ind(df, reset_indcators):

    if reset_indcators :
        df['vpfr'] = np.nan
        

    if df['real_volume'][-20:-1].max():volume = 'real_volume'
    else: volume = 'tick_volume'
    df.loc[df.index[0],'vpfr'] = 0
    for i,row in df.loc[df.index[df.index.get_loc(df['vpfr'].last_valid_index())+1]:,].iterrows():
        
        if df.loc[i,'sup_top'] > 0 :
            
            # ser = df.loc[df[df['sup'].notna()].loc[df.index[0]:i].index[-2]:i,volume]
            ser = get_v_betwen(df,'sup_bottom',-1,i,volume,0)
            x =  ser.size
            a =x // 2
            if ser[ :a].sum() > ser[a: ].sum(): df.loc[i,'vpfr'] = 1
            else : df.loc[i,'vpfr'] = 0
            
        if df.loc[i,'sup_bottom'] > 0 :
            
            # ser = df.loc[df[df['sup'].notna()].loc[df.index[0]:i].index[-2]:i,volume]
            ser = get_v_betwen(df,'sup_top',-1,i,volume,0)
            x =  ser.size
            a =x // 2
            if ser[ :a].sum() > ser[a: ].sum(): df.loc[i,'vpfr'] = 1
            else : df.loc[i,'vpfr'] = 0