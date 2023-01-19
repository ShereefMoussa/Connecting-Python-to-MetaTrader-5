# import modules
from modules import *

from variables import *

def three_line(df):
    # check if order open
    if df.loc[df.order.last_valid_index(),'order_3lb_buy'] == 1:
        return None
    
    # check candle
    def operation_buy(df,i):
        
        # check if order open
        if df.loc[df.order.last_valid_index(),'order_3lb_buy'] == 1:
            return None

        # main condition
        if df.loc[i,'trend'] == 'break up looking for top':
            
            # candle condition
            if df.loc[df.index[df.index.get_loc(i)-5],'open'] <= get_v_betwen(df,'sup_top',0,i,'sup_top',0)[-1] <= df.loc[i,'close'] and len(get_v_betwen(df,'zig',df.index.get_loc(i)-5,i,'zig',0)):
                
                # candle count
                v_candles = []
                for x ,xrow in df.loc[i-5:i,].iterrows():
                    if xrow['close'] - xrow['open'] > xrow['atr'] and xrow['high'] - xrow['low'] < (xrow['close'] - xrow['open']) * 1.27 :
                        v_candles.append(1)
                        
                if len(v_candles) > 3:
                    # buy stop, stop lose ,target profit 
                    buy_stop = df.loc[i,'high'] + 0.00009
                    s_l = get_v_betwen(df,'sup',0,i,'sup',0)[-1] + df.loc[i,'atr']
                    t_p =  buy_stop + 2* (buy_stop- s_l)
                    
                    if production:
                        pass
                        # retarn True 
                        
                        ################################
                    else:
                        # if df.loc[df['3lb_buy'].last_valid_index(),'3lb_buy'] != 1:
                        #     df.loc[i,'3lb_buy'] = 1
                            
                            
                            three_line_buy_order(df,i,buy_stop,s_l,t_p)
    
    if production: 
        for i,row in df.loc[df.trend.last_valid_index():,'trend'].iterrows():
            if operation_buy(df,i):
                break
            
    else:
        for i,row in df.iterrows():
            operation_buy(df,i)
                
def three_line_buy_order(df,buy_candle,buy_stop,s_l,t_p):

    for i,row in df.loc[buy_candle:df.index[df.index.get_loc(buy_candle)+7],].iterrows():
        if df.loc[i,'close'] > buy_stop:
            
            # active order func
            df.loc[buy_candle,'order_3lb_buy'] = 1
            check_process(df,buy_candle,buy_stop,s_l,t_p)
            break
    
    
def check_process(df,buy_candle,buy_stop,s_l,t_p):
    # looking for result
    for i,row in df.loc[buy_candle:,].iterrows():
        # break even
        if df.loc[buy_candle,'3lb_buy_result'] == 'buy break even':
            if df.loc[i,'low'] <= buy_stop:
                df.loc[i,'order_3lb_buy'] = 0
        # loss
        if df.loc[i,'low'] <= s_l:
            df.loc[i,'order_3lb_buy'] = 0
            df.loc[buy_candle,'3lb_buy_result'] = 'buy lose'
            break
        
        # win
        elif df.loc[i,'high'] >= t_p:
            df.loc[i,'order_3lb_buy'] = 0
            df.loc[buy_candle,'3lb_buy_result'] = 'buy win'
            break
        
        # 
        if len(get_v_betwen(df,'zig',buy_candle,i,'zig',0)) >= 2:
            
            if get_v_betwen(df,'zig',buy_candle,i,'macd',0)[-1] > get_v_betwen(df,'zig',buy_candle,-1,'macd',0)[-2]:
                # good
                if  df.loc[i,'close'] == buy_stop + (buy_stop - s_l) :
                # امن الصفقة
                    df.loc[buy_candle,'3lb_buy_result'] = 'buy break even'
                    df.loc[i,'order_3lb_buy'] = 2
                    
            else:
                # check امن الصفقة
                if df.loc[i,'close'] > buy_stop:
                    # امن الصفقة
                    df.loc[buy_candle,'3lb_buy_result'] = 'buy break even'
                    df.loc[i,'order_3lb_buy'] = 2
                
                
    
    