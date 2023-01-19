# import modules
from modules import *


def orders():
    orders_total=mt5.orders_total()
    print(orders_total)
    # get the list of orders on symbols whose names contain
    orders=mt5.orders_get()
    if orders is None:
        print("No orders with group=\"*GBP*\", error code={}".format(mt5.last_error()))
    else:
        print("orders_get={}".format(len(orders)))
        # display these orders as a table using pandas.DataFrame
        df=pd.DataFrame(list(orders),columns=orders[0]._asdict().keys())
        df.drop(['time_done', 'time_done_msc', 'position_id', 'position_by_id', 'reason', 'volume_initial', 'price_stoplimit'], axis=1, inplace=True)
        df['time_setup'] = pd.to_datetime(df['time_setup'], unit='s')
        print(df)

def positions():
    positions_total=mt5.positions_total()
    print(positions_total)
    # get the list of positions on symbols whose names contain 
    positions=mt5.positions_get()
    if positions==None:
        print("No positions with group=\"*USD*\", error code={}".format(mt5.last_error()))
    elif len(positions)>0:
        print("positions_get(group=\"*USD*\")={}".format(len(positions)))
        # display these positions as a table using pandas.DataFrame
        df=pd.DataFrame(list(positions),columns=positions[0]._asdict().keys())
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
        print(df)

def order_valid(symbol,action,volume,price):
    # check for other order in the financial instrument
    # check for positions
    if False:
        print(7)
    # check for orders