# import modules
from modules import *

from variables import *
# from utilities import *

def time_frame(df,key,data_folder,symbol):
    
    def timef_data(df,i,tframe,key):
        
        top_index = tframe.loc[tframe.sup_top.notna()].index[-1] 
        bottom_index = tframe.loc[tframe.sup_bottom.notna()].index[-1]

        if top_index > bottom_index :
            if tframe.loc[top_index,'sup_top'] > tframe.loc[bottom_index,'sup_bottom']:
                # trend up
                df.loc[i,f'{tframe}_up'] = 1
                
                df.loc[i,f'{tframe}_swing_top'] = tframe.loc[top_index,'sup_top']
                df.loc[i,f'{tframe}_swing_bottom'] = tframe.loc[bottom_index,'sup_bottom']
                
                if tframe.loc[top_index,'macd'] > tframe.loc[tframe.loc[tframe.sup_top.notna()].index[-2] ,'macd']:
                    df.loc[i,f'{tframe}_up_macd'] = 1
                else: df.loc[i,f'{tframe}_up_macd'] = 0
                
                if tframe.loc[top_index,'rsi'] > tframe.loc[tframe.loc[tframe.sup_top.notna()].index[-2] ,'rsi']:
                    df.loc[i,f'{tframe}_up_rsi'] = 1
                else: df.loc[i,f'{tframe}_up_rsi'] = 0
                
            # down
            else:
                df.loc[i,f'{tframe}_down'] = 1
                
                df.loc[i,f'{tframe}_swing_top'] = tframe.loc[top_index,'sup_top']
                df.loc[i,f'{tframe}_swing_bottom'] = tframe.loc[bottom_index,'sup_bottom']
                
                if tframe.loc[bottom_index,'macd'] < tframe.loc[tframe.loc[tframe.sup_bottom.notna()].index[-2] ,'macd']:
                    df.loc[i,f'{tframe}_down_macd'] = 1
                else: df.loc[i,f'{tframe}_down_macd'] = 0
                
                if tframe.loc[bottom_index,'rsi'] > tframe.loc[tframe.loc[tframe.sup_bottom.notna()].index[-2] ,'rsi']:
                    df.loc[i,f'{tframe}_down_rsi'] = 1
                else: df.loc[i,f'{tframe}_down_rsi'] = 0
        else:
            if tframe.loc[top_index,'sup_top'] < tframe.loc[bottom_index,'sup_bottom']:
                #  trend down
                df.loc[i,f'{tframe}_down'] = 1
                
                df.loc[i,f'{tframe}_down'] = 1
                
                df.loc[i,f'{tframe}_swing_top'] = tframe.loc[top_index,'sup_top']
                df.loc[i,f'{tframe}_swing_bottom'] = tframe.loc[bottom_index,'sup_bottom']
                
                if tframe.loc[bottom_index,'macd'] < tframe.loc[tframe.loc[tframe.sup_bottom.notna()].index[-2] ,'macd']:
                    df.loc[i,f'{tframe}_down_macd'] = 1
                else: df.loc[i,f'{tframe}_down_macd'] = 0
                
                if tframe.loc[bottom_index,'rsi'] < tframe.loc[tframe.loc[tframe.sup_bottom.notna()].index[-2] ,'rsi']:
                    df.loc[i,f'{tframe}_down_rsi'] = 1
                else: df.loc[i,f'{tframe}_down_rsi'] = 0
                # up
            else:
                df.loc[i,f'{tframe}_up'] = 1
                
                df.loc[i,'swing_top'] = tframe.loc[top_index,'sup_top']
                df.loc[i,'swing_bottom'] = tframe.loc[bottom_index,'sup_bottom']
                
                
    
                if tframe.loc[top_index,'macd'] > tframe.loc[tframe.loc[tframe.sup_top.notna()].index[-2] ,'macd']:
                    df.loc[i,f'{tframe}_up_macd'] = 1
                else: df.loc[i,f'{tframe}_up_macd'] = 0
                
                if tframe.loc[top_index,'rsi'] > tframe.loc[tframe.loc[tframe.sup_top.notna()].index[-2] ,'rsi']:
                    df.loc[i,f'{tframe}_up_rsi'] = 1
                else: df.loc[i,f'{tframe}_up_rsi'] = 0
        
        
        closeP = df.loc[i,'close']
        s_t_u = tframe.loc[tframe['sup_top'] > closeP,'sup_top'].sort_values(ascending=True)
        sup_top_up =  s_t_u[0] if len(s_t_u) else np.nan
        
        s_t_d = tframe.loc[tframe['sup_bottom'] > closeP,'sup_bottom'].sort_values(ascending=True)
        sup_top_down =  s_t_d[0] if len(s_t_d) else np.nan
        
        if sup_top_up is not np.nan or sup_top_down is not np.nan:
            df.loc[i,f'{tframe}_res'] = sup_top_up if sup_top_up < sup_top_down else sup_top_down
        elif sup_top_up is not np.nan:
            df.loc[i,f'{tframe}_res'] = sup_top_up
        else: df.loc[i,f'{tframe}_res'] = sup_top_down
        
        s_b_u = tframe.loc[tframe['sup_top'] < closeP,'sup_top'].sort_values(ascending=False)
        sup_bottom_up =  s_b_u[0] if len(s_b_u) else np.nan
        s_b_d = tframe.loc[tframe['sup_bottom'] < closeP,'sup_bottom'].sort_values(ascending=False)
        sup_bottom_down =  s_b_d[0] if len(s_b_d) else np.nan
        
        if sup_bottom_up is not np.nan or sup_bottom_down is not np.nan:
            df.loc[i,f'{tframe}_sup'] = sup_bottom_up if sup_bottom_up > sup_bottom_down else sup_bottom_down
        elif sup_bottom_up is not np.nan:
            df.loc[i,f'{tframe}_res'] = sup_bottom_up
        else: df.loc[i,f'{tframe}_res'] = sup_bottom_up
        
        
        df.loc[i,f'{tframe}']= 1

    
    # read csv
    upper_frame_1 = pd.read_csv(f'{data_folder}/{symbol}_{tf[key][0]}.csv',index_col='time')
    upper_frame_1.index = pd.to_datetime(upper_frame_1.index)
    upper_frame_2 = pd.read_csv(f'{data_folder}/{symbol}_{tf[key][1]}.csv',index_col='time')
    upper_frame_2.index = pd.to_datetime(upper_frame_2.index)


    
    if production:
        
        for i,row in df.iloc[:-2:-1].iterrows():
            tframe_1 = upper_frame_1.loc[upper_frame_1.index < i]
            timef_data(df,i,tframe_1,key)

        
        for i,row in df.iloc[:-2:-1].iterrows():
            tframe_2 = upper_frame_2.loc[upper_frame_2.index < i]
            timef_data(df,i,tframe_2,key)
    
    else:
        if f'{tf[key][0]}' not in df.columns:
            df.loc[df.index[0] ,f'{tf[key][0]}'] = 1
            # print(df.head(4))
            
        for i,row in df.loc[ df[f'{tf[key][0]}'].last_valid_index():,].iterrows():
            tframe_1 = upper_frame_1.loc[upper_frame_1.index<i]
            timef_data(df,i,tframe_1,key)

        if f'{tf[key][1]}' not in df.columns:
            df.loc[df.index[1] ,df[f'{tf[key][1]}']] = 1
        for i,row in df.loc[ df[f'{tf[key][1]}'].last_valid_index():,].iterrows():
            tframe_2 = upper_frame_2.loc[upper_frame_2.index<i]
            timef_data(df,i,tframe_2,key)
    
    
    