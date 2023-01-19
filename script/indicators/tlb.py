import numpy as np
import pandas as pd
from tqdm import tqdm

def tlb(df, num_of_line, reset_indicators):
        
    def tlb_core(df, num_of_line):
        for row in tqdm(df.loc[df['tlb'].last_valid_index():].itertuples()):
            if df.loc[df.index[df.index.get_loc(row.Index)-1],'tlb'] == 1:
                if row.open > row.close:
                    if df.loc[row.Index, 'high'] > df.loc[df.index[df.index.get_loc(row.Index)-num_of_line]:df.index[df.index.get_loc(row.Index)-1], 'high'].max():
                        df.loc[row.Index, 'tlb'] = 1
                        
                    elif df.loc[row.Index, 'low'] < df.loc[df.index[df.index.get_loc(row.Index)-num_of_line]:df.index[df.index.get_loc(row.Index)-1], 'low'].min():
                        df.loc[row.Index, 'tlb'] = -1
                        
                    else: df.loc[row.Index, 'tlb'] = 1
                    
                else:
                    if df.loc[row.Index, 'low'] < df.loc[df.index[df.index.get_loc(row.Index)-num_of_line]:df.index[df.index.get_loc(row.Index)-1], 'low'].min():
                        df.loc[row.Index, 'tlb'] = -1
                    
                    elif df.loc[row.Index, 'high'] > df.loc[df.index[df.index.get_loc(row.Index)-num_of_line]:df.index[df.index.get_loc(row.Index)-1], 'high'].max():
                        df.loc[row.Index, 'tlb'] = 1
                        
                    else: df.loc[row.Index, 'tlb'] = 1
                    
            else:
                if row.open < row.close:
                    if df.loc[row.Index, 'low'] < df.loc[df.index[df.index.get_loc(row.Index)-num_of_line]:df.index[df.index.get_loc(row.Index)-1], 'low'].min():
                        df.loc[row.Index, 'tlb'] = -1
                    
                    elif df.loc[row.Index, 'high'] > df.loc[df.index[df.index.get_loc(row.Index)-num_of_line]:df.index[df.index.get_loc(row.Index)-1], 'high'].max():
                        df.loc[row.Index, 'tlb'] = 1
                        
                    else: df.loc[row.Index, 'tlb'] = -1
                
                else:
                    if df.loc[row.Index, 'high'] > df.loc[df.index[df.index.get_loc(row.Index)-num_of_line]:df.index[df.index.get_loc(row.Index)-1], 'high'].max():
                        df.loc[row.Index, 'tlb'] = 1
                        
                    elif df.loc[row.Index, 'low'] < df.loc[df.index[df.index.get_loc(row.Index)-num_of_line]:df.index[df.index.get_loc(row.Index)-1], 'low'].min():
                        df.loc[row.Index, 'tlb'] = -1
                        
                    else: df.loc[row.Index, 'tlb'] = -1
                        
    if reset_indicators or 'tlb' not in df.columns or pd.isnull(df.loc[df.index[0],'tlb']):
        
        if df.loc[df.index[num_of_line], 'high'] >= df.loc[df.index[0]: df.index[num_of_line -1], 'high'].max():
            df.loc[df.index[num_of_line], 'tlb'] = 1
            
        elif df.loc[df.index[num_of_line], 'low'] <= df.loc[df.index[0]: df.index[num_of_line -1], 'low'].min():
            df.loc[df.index[num_of_line], 'tlb'] = -1
            
        else: df.loc[df.index[num_of_line], 'tlb'] = 1
        
        tlb_core(df, num_of_line)
        
    else: tlb_core(df, num_of_line)
    
    
def tlb_2(df, reset_indicators):
        
    def tlb_core(df):
        for row, prow1, prow2, prow3 in tqdm(zip(df.loc[df['tlb'].last_valid_index():].itertuples(),
                                    df.loc[df.index[df.index.get_loc(df['tlb'].last_valid_index())-1]:].itertuples(),
                                    df.loc[df.index[df.index.get_loc(df['tlb'].last_valid_index())-2]:].itertuples(),
                                    df.loc[df.index[df.index.get_loc(df['tlb'].last_valid_index())-3]:].itertuples())):
            
            if df.loc[prow1.Index,'tlb'] == 1:
                if row.open > row.close:
                    if row.high > max(prow1.high, prow2.high, prow3.high):
                        df.loc[row.Index, 'tlb'] = 1
                        
                    elif row.low < min(prow1.low, prow2.low, prow3.low):
                        df.loc[row.Index, 'tlb'] = -1
                        
                    else: df.loc[row.Index, 'tlb'] = 1
                    
                else:
                    if row.low < min(prow1.low, prow2.low, prow3.low):
                        df.loc[row.Index, 'tlb'] = -1
                    
                    elif row.high > max(prow1.high, prow2.high, prow3.high):
                        df.loc[row.Index, 'tlb'] = 1
                        
                    else: df.loc[row.Index, 'tlb'] = 1
                    
            else:
                if row.open < row.close:
                    if row.low < min(prow1.low, prow2.low, prow3.low):
                        df.loc[row.Index, 'tlb'] = -1
                    
                    elif row.high > max(prow1.high, prow2.high, prow3.high):
                        df.loc[row.Index, 'tlb'] = 1
                        
                    else: df.loc[row.Index, 'tlb'] = -1
                
                else:
                    if row.high > max(prow1.high, prow2.high, prow3.high):
                        df.loc[row.Index, 'tlb'] = 1
                        
                    elif row.low < min(prow1.low, prow2.low, prow3.low):
                        df.loc[row.Index, 'tlb'] = -1
                        
                    else: df.loc[row.Index, 'tlb'] = -1
                        
    if reset_indicators or 'tlb' not in df.columns or pd.isnull(df.loc[df.index[0],'tlb']):
        
        if df.loc[df.index[3], 'high'] >= df.loc[df.index[0]: df.index[2], 'high'].max():
            df.loc[df.index[3], 'tlb'] = 1
            
        elif df.loc[df.index[3], 'low'] <= df.loc[df.index[0]: df.index[2], 'low'].min():
            df.loc[df.index[3], 'tlb'] = -1
            
        else: df.loc[df.index[3], 'tlb'] = 1
        
        tlb_core(df)
        
    else: tlb_core(df)