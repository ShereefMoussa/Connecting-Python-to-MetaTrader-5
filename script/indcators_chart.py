import sys
from modules import *
from indicators import *
# sys.path.append('script/indicators')
# from ind_main import *
# from chart import *
# from zigzag_in import *
from plotly_chart import *
from TimeFrame import *
# from plot_data import *


def indcators_and_chart(df,sy_tf,key,data_folder,symbol):
    df['ema_200'] = ema_ind(df,200)
    df['ema_117'] = ema_ind(df,117)
    df['ema_50'] = ema_ind(df,50)
    # rsi_ind(df,9)
    # macd_ind(df)
    atr_ind(df,14,5,100)
    # zig_ind(df,3,reset_indcators) #0.00035
    # sup_res(df,reset_indcators)     
    # vpfr_ind(df,reset_indcators)
    heikin_ashi(df,1,reset_indcators)
    vvvv = s_heikin_em_v1(df,tf,key,data_folder,symbol, production)
    vvvv.to_csv('vvvv.csv')
    # print(symbol)
    # print(sy_tf)
    sys.exit()
    # heikin_ashi_test(df,6,reset_indcators)
    # heikin_ashi_test(df,7,reset_indcators)
    # heikin_ashi_test(df,8,reset_indcators)

    # time_frame(df,key,data_folder,symbol)
    # plotly(df,sy_tf)
    # chart(df,sy_tf)
    return df