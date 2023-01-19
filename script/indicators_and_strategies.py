from modules import *
from variables import *

def indicators(df,key,data_folder,symbol):
    # df['ema_200'] = ema_ind(df,200)
    # df['ema_117'] = ema_ind(df,117)
    # df['ema_50'] = ema_ind(df,50)
    df['kama_20'] = kama(df,20)
    df['kama_50'] = kama(df,50)
    df['kama_200'] = kama(df,200)
    atr_ind(df,14,5,200)
    # df['adx'], df['di_p'], df['di_n'] = adx_wilder(df,6) 
    # df['adx_smma'] = smma(df,'adx',4)
    heikin_ashi(df,1,reset_indicators)
    # tlb(df,3,reset_indicators)
    tlb_2(df, reset_indicators)
    price_density(df,24)
    efficiency_ratio(df,24)
    # df['heikin_close_s'], df['heikin_open_s'], df['heikin_high_s'], df['heikin_low_s'] = heikin_ashi_period(df,7)
    # df['ema_270'] = ema_ind(df,270)
    # df['sma_200'] = sma_ind(df,80)
    # rsi_ind(df,9)
    # macd_ind(df)
    # zig_ind(df,3,reset_indcators) #0.00035
    # sup_res(df,reset_indcators)     
    # vpfr_ind(df,reset_indcators)
    # time_frame(df,key,data_folder,symbol)
    return df

def strategies(df, key, data_folder, symbol, e_point):
    
    if key == '1M':
        # vvvv = s_heikin_em_v1(df,tf,key,data_folder,symbol, production)
        # vvvv = s_heikin_em_v2(df,tf,key,data_folder,symbol, production,7,18)
        result_strategy, strategy_name = adx_tlb_ema_atr(df,tf,key,data_folder,symbol, production,7,18 ,e_point)
        if production == 'build' or production == 'p_build':
            result_strategy.to_csv(f'reports/{symbol}_{key}_{strategy_name}_{production}.csv')
            
    # if key == '1M':
    #     xxx = sss(df,tf,key,data_folder,symbol, production,7,18)
    #     # print(vvvv.head(2))
    #     if production == 'build': 
    #         xxx.to_csv(f'{symbol}_{key}_xxx.csv')
