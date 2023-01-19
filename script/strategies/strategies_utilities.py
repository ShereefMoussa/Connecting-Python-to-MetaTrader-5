import pandas as pd 
import numpy as np
from datetime import datetime
# def get_tf_candle(i,up_tf):
#     # print(333333333333333333333,i)
#     period = (up_tf.index[-1]- up_tf.index[-2])
#     period_start = i- period
#     st1 = up_tf.loc[up_tf.index <= i]
#     # print('kkkkk', st1.tail())
#     st2 = st1.loc[st1.index >= period_start].iloc[-1:]
#     # print('mmmmmmmmmm', st1.tail())
#     for row in st2.itertuples():
#         return row
def get_tf_candle(i,up_tf):
    period = (up_tf.index[-1]- up_tf.index[-2])
    period_start = i- period
    st1 = up_tf.loc[up_tf.index >= period_start].iloc[0:1]
    for row in st1.itertuples():
        return row


# (df,buy_candle,buy_stop,stop_lose,t_p1,t_p2,order_buy,gap)
def active_buy_stop(df,buy_candle,buy_stop,stop_lose,t_p1,t_p2,t_p3,order_buy,gap,candle_stop):
    for row in df.loc[buy_candle:df.index[df.index.get_loc(buy_candle)+candle_stop],].itertuples():
        
        if row.high >= buy_stop:
            # print(99999999999999999999999999999999999999999999999999999999999)
            # active order func
            df.loc[buy_candle,order_buy] = 1
            # print('hhhhhhhh', df.loc[buy_candle,order_buy])
            index_end =  check_process_buy_scalping(df,buy_candle,buy_stop,stop_lose,t_p1,t_p2,t_p3,order_buy,gap)
            return index_end 
    # if buy_candle == datetime(2022,6,8,12,30,00):
        # print(111111111111111111111111111111111111111111111 , df.loc[buy_candle,])
    if order_buy not in df.columns:
        df[order_buy] = np.nan
    if pd.isna(df.loc[buy_candle,order_buy]):
        df.loc[buy_candle,order_buy] = 2
        # print(22222,df.loc[buy_candle,order_buy])
    index_end = pd.Timestamp(0)
    return index_end
        
def active_sell_stop(df,sell_candle,sell_stop,stop_lose,t_p1,t_p2,t_p3,order_sell,gap,candle_stop):
    for row in df.loc[sell_candle:df.index[df.index.get_loc(sell_candle)+candle_stop],].itertuples():
        
        if row.low <= sell_stop:
            # active order func
            df.loc[sell_candle,order_sell] = 1
            # print('hhhhhhhh', row.Index)
            # print('11111',sell_candle)
            # print('2222', df.loc[sell_candle,order_sell])
            # print('33333', df.loc[sell_candle,order_sell])
            index_end =  check_process_sell_scalping(df,sell_candle,sell_stop,stop_lose,t_p1,t_p2,t_p3,order_sell,gap)
            return index_end 
    
    
    if order_sell not in df.columns:
        df[order_sell] = np.nan
    if pd.isna(df.loc[sell_candle,order_sell]):
        df.loc[sell_candle,order_sell] = 2
    index_end = pd.Timestamp(0)
    return index_end
    

def check_process_sell_scalping(df,sell_candle,sell_stop,stop_lose,t_p1,t_p2,t_p3,order_sell,gap):
    # looking for result
    
    # trailing_stop = gap + 
    win_2 = False
    break_even = False
    one_to_one = False
    # global end_of_order_index
    for row in df.loc[sell_candle:,].itertuples():
        
        if len(df.loc[sell_candle:row.Index]) == 20:
            one_to_one = True
        
        # loss      
        if row.high >= stop_lose:
            df.loc[row.Index, order_sell] = 0
            df.loc[sell_candle, f'{order_sell}_results'] = 'sell lose'
            row_end = row
            end_of_order_index = row.Index
            break
        # break even
        if row.low <= t_p1:
            break_even = True
            if one_to_one:
                df.loc[sell_candle, f'{order_sell}_results'] = 'sell tp1'
                end_of_order_index = row.Index
                break
            
        # if break_even is True or win_2 == True:
        #     if row.high >= sell_stop:
        #         df.loc[row.Index, order_sell] = 0
        #         df.loc[sell_candle, f'{order_sell}_results'] = 'sell break even'
        #         row_end = row
        #         end_of_order_index = row.Index
        #         break
        
        # win
        if row.low <= t_p2:
            df.loc[row.Index, order_sell] = 0 #0
            df.loc[sell_candle, f'{order_sell}_results'] = 'sell win_2'
            row_end = row
            end_of_order_index = row.Index
            win_2 = True
            # break
        
        if row.low <= t_p3:
            # print()
            df.loc[row.Index, order_sell] = 0 #0
            df.loc[sell_candle, f'{order_sell}_results'] = 'sell win_3'
            row_end = row
            end_of_order_index = row.Index
            break
        
        
    
    if row.Index == df.index[-1]:
        end_of_order_index = row.Index
    return end_of_order_index

def check_process_buy_scalping(df,buy_candle,buy_stop,stop_lose,t_p1,t_p2,t_p3,order_buy,gap):
    # looking for result
    
    # trailing_stop = gap + 
    
    break_even = False
    global end_of_order_index
    one_to_one = False

    for row in df.loc[buy_candle:,].itertuples():
        if len(df.loc[buy_candle:row.Index]) == 20:
            one_to_one = True
                
        # loss     
        if row.low <= stop_lose:
            df.loc[row.Index, order_buy] = 0
            df.loc[buy_candle, f'{order_buy}_results'] = 'buy lose'
            row_end = row
            end_of_order_index = row.Index
            break
        
        # break even
        if row.high >= t_p1:
            break_even = True
            if one_to_one:
                df.loc[buy_candle, f'{order_buy}_results'] = 'buy tp1'
                end_of_order_index = row.Index
                break
            
        # if break_even is True:
        #     if row.low <= buy_stop:
        #         df.loc[row.Index, order_buy] = 0
        #         df.loc[buy_candle, f'{order_buy}_results'] = 'buy break even'
        #         row_end = row
        #         end_of_order_index = row.Index
        #         break
        
        # win
        if row.high >= t_p2:
            df.loc[row.Index, order_buy] = 0 #0
            df.loc[buy_candle, f'{order_buy}_results'] = 'buy win_2'
            row_end = row
            end_of_order_index = row.Index
            # breaks
            
        if row.high >= t_p3:
            df.loc[row.Index, order_buy] = 0 #0
            df.loc[buy_candle, f'{order_buy}_results'] = 'buy win_3'
            row_end = row
            end_of_order_index = row.Index
            break
        
        
    return end_of_order_index