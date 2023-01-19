import os 


def populate_x_y(df,co):
    co_up = co[0]
    co_down = co[1]
    
    x = []
    y = []
    
    up = True
    for i,row in df.iterrows():
        if up:
            if row[co_down] > 0:
                x.append(i)
                y.append(row[co_down])
                up = False
                
            if row[co_up] > 0:
                x.append(i)
                y.append(row[co_up])
                up = True
                
        else:
            if row[co_up] > 0:
                x.append(i)
                y.append(row[co_up])
                up = True
            
            if row[co_down] > 0:
                x.append(i)
                y.append(row[co_down])
                up = False
    
    return x,y


def get_symbols_and_tf(path):
    symbols = []
    time_f = []
    for file in os.listdir(f"./{path}"):
        file = file[:-4]
        split_f = file.split('_')
        symbols.append(split_f[0]) 
        time_f.append(split_f[1])
    symbols = drop_duplicates(symbols)
    time_f = drop_duplicates(time_f)
    symbols = options_dic(symbols)
    time_f = options_dic(time_f)
    return symbols,time_f

def drop_duplicates(list):
        result = [] 
        for i in list: 
            if i not in result: 
                result.append(i)
        list = result
        return list
            
def options_dic(list):
    dic_list = []
    for ls in list:
        x = {"label": f"{ls}", "value": ls}
        dic_list.append(x)
    return dic_list
