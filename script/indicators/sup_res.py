# import modules
# from modules import *
import numpy as np
from indicators.utilities import get_v_index ,get_v_betwen ,get_v_value ,get_v_c_value
# from variables import *

def sup_res(df,reset_indcators):
    if reset_indcators :
        
        df['sup_top'] = np.nan
        df['sup_bottom'] = np.nan
        df['trend'] = np.nan
    
    top_index = df.loc[df.zig_top.notna()].loc[df.zig_bottom.isna()].index[0] 
    bottom_index = df.loc[df.zig_bottom.notna()].loc[df.zig_top.isna()].index[0]
    
    df.loc[top_index,'sup_top'] = df.loc[top_index,'zig_top']
    df.loc[bottom_index,'sup_bottom'] = df.loc[bottom_index,'zig_bottom']
    
    if top_index > bottom_index :
        if df.loc[top_index,'zig_top'] > df.loc[bottom_index,'zig_bottom']:
            
            df.loc[top_index,'trend'] = 'top verified looking for bottom'
        else: df.loc[top_index,'trend'] = 'bottom verified looking for top'
    else:
        if df.loc[top_index,'zig_top'] > df.loc[bottom_index,'zig_bottom']:
            
            df.loc[bottom_index,'trend'] = 'bottom verified looking for top'
        else: df.loc[bottom_index,'trend'] = 'top verified looking for bottom'
        
    # print(df.loc[top_index,'zig_top'])
    # print(df.loc[bottom_index,'zig_bottom'])

    # print(df.loc[top_index,'sup_top'])
    # print(df.loc[bottom_index,'sup_bottom'] )
    # print('ggggg',df.loc[top_index,'trend'])
    
    for i,row in df.loc[df.trend.last_valid_index(): ,].iterrows():
    # for i,row in df.loc[df['trend'].last_valid_index():,].iterrows():
        # break up looking for top
        
        if get_v_value(df,'trend',-1) == 'break up looking for top': 
            if len(get_v_betwen(df,'trend',-1,i,'zig_top',0)):
                
                df.loc[get_v_betwen(df,'trend',-1,i,'high',0).idxmax(),'sup_top'] = get_v_betwen(df,'trend',-1,i,'high',0).max()
                df.loc[i,'trend'] = 'top verified looking for bottom'
                
        # top verified looking for bottom
        elif get_v_value(df,'trend',-1) == 'top verified looking for bottom': 
            
            # break up
            if df.loc[i,'high'] > get_v_value(df,'sup_top',-1) :
            # and len(get_v_betwen(df,'trend',-1,i,'zig_bottom',0)):
                # print('vvv',get_v_index(df,'sup_top',-1),get_v_value(df,'sup_top',-1))
                # print('trend',get_v_index(df,'trend',-1),df.loc[get_v_index(df,'trend',-1)])
                # print('##################################')
                # print(get_v_betwen(df,'trend',-1,i,'low',0))
                # print('##################################')

                # print('ffff',i,row)
                df.loc[get_v_betwen(df,'sup_top',-1,i,'low',0).idxmin(),'sup_bottom'] = get_v_betwen(df,'sup_top',-1,i,'low',0).min()
                df.loc[i,'trend']= 'break up looking for top'
                
            # low bottom than ref point
            elif df.loc[i,'low'] < get_v_value(df,'sup_bottom',-1):
                df.loc[i,'trend'] = 'looking for bottom lower than ref'
                
        # looking for bottom lower than ref
        elif get_v_value(df,'trend',-1) == 'looking for bottom lower than ref':
            if len(get_v_betwen(df,'trend',-1,i,'zig_bottom',0)):
                df.loc[get_v_betwen(df,'trend',-1,i,'low',0).idxmin(),'sup_bottom'] = get_v_betwen(df,'trend',-1,i,'low',0).min()
                df.loc[i,'trend'] = 'break down or up'
                
        # break down or up
        elif get_v_value(df,'trend',-1) == 'break down or up':
            
            if df.loc[i,'high'] > get_v_value(df,'sup_top',-1):
                df.loc[i,'trend']= 'break up looking for top'
                
            elif df.loc[i,'low'] < get_v_value(df,'sup_bottom',-1):
                df.loc[get_v_betwen(df,'sup_bottom',-1,i,'high',0).idxmax(),'sup_top'] = get_v_betwen(df,'sup_bottom',-1,i,'high',0).max()
                df.loc[i,'trend'] = 'break down looking for bottom'
                
        ################################################################################
        # break down looking for bottom
        elif get_v_value(df,'trend',-1) == 'break down looking for bottom':
            
            if len(get_v_betwen(df,'sup_top',-1,i,'zig_bottom',0)) > 0:
                df.loc[get_v_betwen(df,'sup_top',-1,i,'low',0).idxmin(),'sup_bottom'] = get_v_betwen(df,'sup_top',-1,i,'low',0).min()
                df.loc[i,'trend'] = 'bottom verified looking for top'
                
        # bottom verified looking for top
        elif get_v_value(df,'trend',-1) == 'bottom verified looking for top':
        
            # break down
            if df.loc[i,'low'] < get_v_value(df,'sup_bottom',-1):
                
                # print('sup_bottom',get_v_index(df,'sup_bottom',-1),get_v_value(df,'sup_bottom',-1))
                # print('trend',get_v_index(df,'trend',-1),get_v_value(df,'trend',-1))
                # print('##################################')
                # print('iiiiii',i,row)
                # print('##################################')
                # print(get_v_betwen(df,'sup_bottom',-1,i,'high',0))
                
                df.loc[get_v_betwen(df,'sup_bottom',-1,i,'high',0).idxmax(),'sup_top'] = get_v_betwen(df,'sup_bottom',-1,i,'high',0).max()
                df.loc[i,'trend'] = 'break down looking for bottom'
                ###############################
                # higher top than ref point
            elif df.loc[i,'high'] > df.loc[get_v_index(df,'sup_top',-1),'sup_top']:
                df.loc[i,'trend'] = 'looking for top higher than ref'
                
        # looking for top higher than ref
        elif get_v_value(df,'trend',-1) == 'looking for top higher than ref':
            
            if len(get_v_betwen(df,'trend',-1,i,'zig_top',0)) :
                df.loc[get_v_betwen(df,'trend',-1,i,'high',0).idxmax(),'sup_top'] = get_v_betwen(df,'trend',-1,i,'high',0).max()
                df.loc[i,'trend'] = 'break up or down'
                
        # break up or down
        elif get_v_value(df,'trend',-1) == 'break up or down':
        
            if df.loc[i,'low'] < df.loc[get_v_index(df,'sup_bottom',-1),'sup_bottom']:
                
                df.loc[i,'trend']= 'break down looking for bottom'
                
            elif df.loc[i,'high'] > df.loc[get_v_index(df,'sup_top',-1),'sup_top']:
                
                df.loc[get_v_betwen(df,'trend',-1,i,'low',0).idxmin(),'sup_bottom'] =get_v_betwen(df,'trend',-1,i,'low',0).min()
                df.loc[i,'trend']= 'break up looking for top'
        df.to_csv('df_sup.csv')
    # df.set_index('time',inplace=True)

    return df