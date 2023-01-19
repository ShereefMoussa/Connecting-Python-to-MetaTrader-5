import pandas as pd
from tqdm import tqdm
import inspect
import types
from typing import cast
from strategies.strategies_utilities import *
from strategies.check_fun import *
from mt5_fun import *
from log_fun import *


def adx_heikin_ema_atr(df,tf,key,data_folder,symbol, production, from_hour, to_hour):
    
    # strategy_name = adx_heikin_ema_atr.__name__
    strategy_name = cast(types.FrameType, inspect.currentframe()).f_code.co_name
    # print(strategy_name)
    upper_frame_1 = pd.read_csv(f'{data_folder}/{symbol}_{tf[key][1]}.csv',index_col='time')
    upper_frame_1.index = pd.to_datetime(upper_frame_1.index)
    # print(upper_frame_1.tail(3))
    result = pd.DataFrame()
    index_end = pd.Timestamp(0)
    # if build
    if production == 'build' or production == 'p_build':
        logger.info(f"start {data_folder}_ {symbol}")
        for row in tqdm(df.iloc[200: -33].itertuples()):
            # check if order active
            # print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk', row.Index, index_end)
            if index_end > row.Index:
                continue
            # check hour
            hour = row.Index.hour
            if hour > from_hour and hour < to_hour:

                result, index_end = adx_heikin_ema_atr_core(df,row,upper_frame_1,strategy_name, result, index_end, production, symbol)

        return result, strategy_name
    
    elif production == 'production':
        for row in df.iloc[-2:-1].itertuples():
            # check hour
            hour = row.Index.hour
            if hour > from_hour and hour < from_hour:
                
                adx_heikin_ema_atr_core(df,row,upper_frame_1,strategy_name,result,index_end, production, symbol)

def adx_heikin_ema_atr_core(df,row,upper_frame_1,strategy_name,result,index_end, production, symbol):
    
    if row.close > row.ema_200 and row.ema_117 > row.ema_200 and row.ema_50 > row.ema_117 :
        if check_heikin_candle(row) == 'bull' and check_low_ema125_bull(df,row):
            # get higher tf
            tf_candle_tuple_1 = get_tf_candle(row.Index,upper_frame_1)
            # print(row.Index)
            # print("cccccc", tf_candle_tuple_1)
            if tf_candle_tuple_1.close > tf_candle_tuple_1.ema_200 and tf_candle_tuple_1.atr > tf_candle_tuple_1.atr_smma_fast:
                if tf_candle_tuple_1.heikin_close > tf_candle_tuple_1.heikin_open and tf_candle_tuple_1.adx > tf_candle_tuple_1.adx_smma and tf_candle_tuple_1.di_p > tf_candle_tuple_1.di_n:
                    # print('start buy')
                    logger.info(f'start buy {symbol}')
                    symbol_info = mt5.symbol_info(symbol)
                    tick = symbol_info.trade_tick_size
                    buy_candle = row.Index
                    buy_stop = row.high + 3* tick
                    stop_lose = get_stop_lose('up', df, buy_candle, tick, 30, round_dismal(row.atr,tick)/3)
                    order_buy = strategy_name + '_buy'
                    gap = buy_stop - stop_lose
                    if gap < 150* tick :
                        t_p1 = buy_stop + gap
                        t_p2 = buy_stop + 2*gap
                        t_p3 = buy_stop + 2.5*gap
                        if production == 'build' or production == 'p_build':
                            index_end = active_buy_stop(df,buy_candle,buy_stop,stop_lose,t_p1,t_p2,t_p3,order_buy,gap,15)
                            df.loc[buy_candle,f'{order_buy}_end'] = index_end
                            df.loc[buy_candle,f'{order_buy}_enter'] = buy_stop
                            df.loc[buy_candle,f'{order_buy}_stop'] = stop_lose
                            
                        elif production == 'production':
                            print('start buy production')
                            logger.info(f"place_market_order {symbol}")
                            lot = is_not_risky_return_lot(symbol,gap,6)
                            if lot:
                                if symbol_info.ask < buy_stop + 10*tick:
                                    result = place_market_order('buy', symbol, lot, symbol_info.ask, t_p2, stop_lose, 20,"","")
                                    print("buy",result)
                                    print(mt5.last_error())
                    else: 
                        new_gap = gap / 2
                        new_buy_stop = stop_lose + new_gap 
                        n_t_p1 = new_buy_stop + new_gap
                        n_t_p2 = new_buy_stop + 2*new_gap
                        n_t_p3 = new_buy_stop + 2.5*new_gap
                        if production == 'build' or production == 'p_build':
                            index_end = active_buy_stop(df,buy_candle,new_buy_stop,stop_lose,n_t_p1,n_t_p2,n_t_p3,order_buy,gap,15)
                            # print(70)
                            df.loc[buy_candle,f'{order_buy}_end'] = index_end
                            df.loc[buy_candle,f'{order_buy}_enter'] = new_buy_stop
                            df.loc[buy_candle,f'{order_buy}_stop'] = stop_lose
                            
                        elif production == 'production':
                            lot = is_not_risky_return_lot(symbol,gap,6)
                            if lot:
                                if symbol_info.ask < buy_stop + 10*tick:
                                    logger.info(f"place_limit_or_market_order {symbol}")
                                    result = place_limit_or_market_order('buy', symbol, lot, new_buy_stop, n_t_p2,
                                                                    stop_lose, 20, 10,symbol_info.ask,row, gap)
                                    

                    if production == 'build' or production == 'p_build':
                        row_df = df.loc[buy_candle,].to_frame().transpose()
                        result = pd.concat([result, row_df],axis=0)
    # check down 
    elif row.close < row.ema_200 and row.ema_117 < row.ema_200 and row.ema_50 < row.ema_117 :
        if check_heikin_candle(row) == 'bear' and check_low_ema125_bear(df,row):
            
            tf_candle_tuple_1 = get_tf_candle(row.Index,upper_frame_1)
            
            if tf_candle_tuple_1.close < tf_candle_tuple_1.ema_200 and tf_candle_tuple_1.atr > tf_candle_tuple_1.atr_smma_fast:
                if tf_candle_tuple_1.heikin_close < tf_candle_tuple_1.heikin_open and tf_candle_tuple_1.adx > tf_candle_tuple_1.adx_smma and tf_candle_tuple_1.di_p < tf_candle_tuple_1.di_n:
                    logger.info(f'start sell{symbol}')
                    symbol_info = mt5.symbol_info(symbol)
                    tick = symbol_info.trade_tick_size
                    order_sell = strategy_name + '_sell'
                    sell_candle = row.Index
                    sell_stop = row.low - 3* tick 
                    stop_lose = get_stop_lose('down', df, sell_candle, tick, 30, round_dismal(row.atr,tick)/3)
                    gap = stop_lose - sell_stop
                    
                    if gap < 150* tick :
                        t_p1 = sell_stop - gap
                        t_p2 = sell_stop - 2*gap
                        t_p3 = sell_stop - 2.5*gap
                        if production == 'build' or production == 'p_build':
                            index_end = active_sell_stop(df,sell_candle,sell_stop,stop_lose,t_p1,t_p2,t_p3,order_sell,gap,15)
                            df.loc[sell_candle,f'{order_sell}_end'] = index_end
                            df.loc[sell_candle,f'{order_sell}_enter'] = sell_stop
                            df.loc[sell_candle,f'{order_sell}_stop'] = stop_lose
                        
                        elif production == 'production':
                            lot = is_not_risky_return_lot(symbol,gap,6)
                            if lot:
                                if symbol_info.bid < sell_stop + 10*tick:
                                    result = place_market_order('sell', symbol, lot, symbol_info.bid,t_p2, stop_lose, 20,"","")
                                    print("sell",result)
                                    print(mt5.last_error())

                    else:
                        new_gap = gap / 2
                        new_sell_stop = stop_lose - new_gap 
                        n_t_p1 = new_sell_stop - new_gap
                        n_t_p2 = new_sell_stop - 2*new_gap
                        n_t_p3 = new_sell_stop - 2.5*new_gap
                        
                        if production == 'build' or production == 'p_build':
                            index_end = active_sell_stop(df,sell_candle,new_sell_stop,stop_lose,n_t_p1,n_t_p2,n_t_p3,order_sell,gap,15)
                            df.loc[sell_candle,f'{order_sell}_end'] = index_end
                            df.loc[sell_candle,f'{order_sell}_enter'] = new_sell_stop
                            df.loc[sell_candle,f'{order_sell}_stop'] = stop_lose
                            
                        elif production == 'production':
                            lot = is_not_risky_return_lot(symbol,gap,6)
                            if lot:
                                result = place_limit_or_market_order('sell', symbol, lot, new_sell_stop, n_t_p2,
                                                                    stop_lose, 20, 10,symbol_info.bid,row, gap)
                                
                        
                    if production == 'build' or production == 'p_build':
                        row_df = df.loc[sell_candle,].to_frame().transpose()
                        result = pd.concat([result, row_df],axis=0)
    if production == 'build' or production == 'p_build':
        return result, index_end
    else: 
        return None, None
