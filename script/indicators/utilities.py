# from modules import *
import os
#  convert dynamic variable name to string
def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj][0]
#  convert dataframe column to list with index
def data_to_list_tuple(df,column):
    list = []
    for i,row in df.iterrows():
        if 0 < row[column] :
            tuple = (i,row[column])
            list.append(tuple)
    return list

# get int index
def get_v_index(df,co,ind):
    return df[df[co].notna()].index[ind]

# get int value
def get_v_value(df,co,ind):
    return df.loc[df[df[co].notna()].index[ind],co]

#  get last cell had a valid value in an other cell
def get_v_c_value(df,co,ind,target_column):
    return df.loc[df[df[co].notna()].index[ind],target_column]

def get_v_betwen(df,co,index_start,index_end,target_co,step):
    return df.loc[df.index[df.index.get_loc(df[df[co].notna()].index[index_start] )+step]:index_end,target_co][df[target_co].notna()]

def get_v_back_betwen(df,co,ind_end):
    return df.loc[ :ind_end,co][df[co].notna()]
