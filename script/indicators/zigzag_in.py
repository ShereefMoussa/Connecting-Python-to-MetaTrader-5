# import modules
from modules import *

# from sup_res import sup_res
from indicators.utilities import *
# from variables import *


def zig_ind(df,atr_multiplier,reset_indcators):
    
    if reset_indcators :
        df['zig_top'] = np.nan
        df['zig_bottom'] = np.nan
        df['up'] = np.nan
        
    df.loc[df.index[0],'zig_top']= df.loc[df.index[0],'high']
    df.loc[df.index[0],'zig_bottom']=df.loc[df.index[0],'low']

    # up = True
    df.loc[df.index[0],'up'] = 1
    
    # for i,row in df.iterrows():
    for i,row in df.loc[df['up'].last_valid_index(): ].iterrows():
        
        if df.loc[df['up'].last_valid_index(),'up'] == 1:
            if df.loc[df.index[df.index.get_loc(i)-1],'low'] >= df.loc[i,'low']:
                
                # if row['close'] <= row['open']:
                    last_zig_bottom = get_v_betwen(df,'zig_bottom',-1,i,'high',1).max()
                    relative_difference = np.abs(df.loc[i,'low'] - last_zig_bottom)/last_zig_bottom
                    percentage = row['atr'] / row['open'] * atr_multiplier
                    if relative_difference >= percentage:
                        df.loc[i,'up'] = False
                        df.loc[get_v_betwen(df,'zig_bottom',-1,i,'high',1).idxmax(),'zig_top']=     last_zig_bottom
                # else:
                #     last_zig_bottom = get_v_betwen(df,'zig_bottom',-1,i,'high',0).max()
                #     relative_difference = np.abs(df.loc[i,'low'] - last_zig_bottom)/last_zig_bottom
                #     percentage = row['atr'] / row['open'] * atr_multiplier
                #     if relative_difference >= percentage:
                #         up = False
                #         df.loc[get_v_betwen(df,'zig_bottom',-1,i,'high',0).idxmax(),'zig_top']=     last_zig_bottom
            # if df.loc[df.index[df.index.get_loc(i)-1],'high'] <= df.loc[i,'high'] and row['open'] > row['close']:
                
            #     last_zig_top = get_v_betwen(df,'zig_top',-1,i,'low',0).min()
            #     relative_difference = np.abs(df.loc[i,'high'] - last_zig_top)/last_zig_top
            #     percentage = row['atr'] / row['open'] * atr_multiplier
            #     if relative_difference >= percentage:
            #         up = True
                    
            #         df.loc[get_v_betwen(df,'zig_top',-1,i,'low',0).idxmin(),'zig_bottom'] = last_zig_top
                    
        elif df.loc[df['up'].last_valid_index(),'up'] == 0 :             
            
            if df.loc[df.index[df.index.get_loc(i)-1],'high'] <= df.loc[i,'high']:
                
                # if row['open'] >= row['close']:

                    last_zig_top = get_v_betwen(df,'zig_top',-1,i,'low',1).min()
                    relative_difference = np.abs(df.loc[i,'high'] - last_zig_top)/last_zig_top
                    percentage = row['atr'] / row['open'] * atr_multiplier
                    if relative_difference >= percentage:
                        df.loc[i,'up'] = True
                        
                        df.loc[get_v_betwen(df,'zig_top',-1,i,'low',1).idxmin(),'zig_bottom'] = last_zig_top
                    
                # else:
                #     last_zig_top = get_v_betwen(df,'zig_top',-1,i,'low',0).min()
                #     relative_difference = np.abs(df.loc[i,'high'] - last_zig_top)/last_zig_top
                #     percentage = row['atr'] / row['open'] * atr_multiplier
                #     if relative_difference >= percentage:
                #         up = True
                        
                #         df.loc[get_v_betwen(df,'zig_top',-1,i,'low',0).idxmin(),'zig_bottom'] = last_zig_top
            
            

    # df['zig']=df['zig'].replace(0,np.nan)
    # zig_df = zig_df.dropna()
    # zig_ser.to_csv('zig_ser.csv')
    df.to_csv('df.csv')
    # zig_df.to_csv('zig_df.csv')s               
        # return zig_df
