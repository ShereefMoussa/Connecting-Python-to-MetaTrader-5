# # import modules
# from modules import *


# # from utilities import *
# # import talib 
# # import pandas as pd 
# # import numpy as np
# # from datetime import datetime, timedelta
# # import seaborn as sns


# def plotly(df,sy_tf):
#     df = df[-350:]
#     fig = make_subplots(vertical_spacing=0, rows=3, cols=1,
#                          specs=[[{"secondary_y": True}],[{"secondary_y": True}],
#                                 [{"secondary_y": True}]],
#                         row_heights=[0.6, 0.03,0.13],shared_xaxes=True)
#     # Candlestick
#     fig.add_trace(go.Candlestick(x=df.index,
#                                 open=df['open'],
#                                 high=df['high'],
#                                 low=df['low'],
#                                 close=df['close'],
#                                 name='candle',
#                                 text=df.index,
#                                 # bgcolor = '#ff0000'
#                                 # gridcolor='Red'
#                                 ))
#     # fig.update_traces(gridcolor='lightyellow', selector=dict(type='candlestick'))
#     # volume
#     fig.add_trace(go.Bar(x=df.index, y = df['tick_volume'], name='volume'), row=2, col=1)
#     # macd
#     fig.add_trace(go.Bar(x=df.index, y = df['macd'], name='macd'), row=3, col=1)
#     fig.add_trace(go.Scatter(x=df.index, y = df['rsi'], name='RSI'), row=3, col=1,secondary_y=True)

#     # ma
#     if 'ema_200' in df.columns:
#         fig.add_trace(go.Scatter(x=df.index, y=df['ema_200'],opacity=0.7, name='ema_200'))


#     # fig.add_trace(go.scatter(x=df.index, y = df['high'],opacity=0.7))
#     if 'zig_top' in df.columns:
#         x_zig , y_zig = populate_x_y(df,['zig_top','zig_bottom'])
#         fig.add_trace(go.Scatter(x = x_zig, 
#                             y = y_zig,
#                             mode='lines+markers',
#                             connectgaps=True, name='zip'
#                             ))
    
#     if 'sup_top' in df.columns:
#         x_sup , y_sup = populate_x_y(df,['sup_top','sup_bottom'])
#         fig.add_trace(go.Scatter(x = x_sup, 
#                                 y = y_sup,
#                                 mode='lines+markers',
#                                 connectgaps=True, name='sup'
#                                 ))

#     fig.update_layout(
#         # paper_bgcolor="#055000", # very back
#         title= sy_tf,
#         margin=dict(
#         l=9,
#         r=3,
#         b=30,
#         t=30,
#         pad=0),
#         # yaxis_title='AAPL Stock',
#         # shapes = [dict(
#         #     x0='2022-5-06 22:00', x1='2022-5-06 22:00', y0=0, y1=1, xref='x', yref='paper',
#         #     line_width=1)]
#         )
#     fig.update_yaxes(gridcolor='darkgray')
#     fig.update_xaxes(
#         # showline=True, linewidth=2, linecolor='black',
#         gridcolor='darkgray',

#         rangeslider_visible=False,
#         rangebreaks=[
#             # NOTE: Below values are bound (not single values), ie. hide x to y
#             dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
#             # dict(bounds=[16, 9.5], pattern="hour"),  # hide hours outside of 9.30am-4pm
#             # dict(values=["2019-12-25", "2020-12-24"])  # hide holidays (Christmas and New Year's, etc)
#         ])
    
    
    
#     # fig.update_layout(xaxis_rangeslider_visible=False)
#     # fig.update_layout(xaxis_rangeslider_visible=False, 
#     #                 # xaxis4_rangeslider_visible=True, 
#     #                 xaxis_type="date")
#     fig.show(auto_open=False)
    
    
#     # aliceblue, antiquewhite, aqua, aquamarine, azure,
#     #         beige, bisque, black, blanchedalmond, blue,
#     #         blueviolet, brown, burlywood, cadetblue,
#     #         chartreuse, chocolate, coral, cornflowerblue,
#     #         cornsilk, crimson, cyan, darkblue, darkcyan,
#     #         darkgoldenrod, darkgray, darkgrey, darkgreen,
#     #         darkkhaki, darkmagenta, darkolivegreen, darkorange,
#     #         darkorchid, darkred, darksalmon, darkseagreen,
#     #         darkslateblue, darkslategray, darkslategrey,
#     #         darkturquoise, darkviolet, deeppink, deepskyblue,
#     #         dimgray, dimgrey, dodgerblue, firebrick,
#     #         floralwhite, forestgreen, fuchsia, gainsboro,
#     #         ghostwhite, gold, goldenrod, gray, grey, green,
#     #         greenyellow, honeydew, hotpink, indianred, indigo,
#     #         ivory, khaki, lavender, lavenderblush, lawngreen,
#     #         lemonchiffon, lightblue, lightcoral, lightcyan,
#     #         lightgoldenrodyellow, lightgray, lightgrey,
#     #         lightgreen, lightpink, lightsalmon, lightseagreen,
#     #         lightskyblue, lightslategray, lightslategrey,
#     #         lightsteelblue, lightyellow, lime, limegreen,
#     #         linen, magenta, maroon, mediumaquamarine,
#     #         mediumblue, mediumorchid, mediumpurple,
#     #         mediumseagreen, mediumslateblue, mediumspringgreen,
#     #         mediumturquoise, mediumvioletred, midnightblue,
#     #         mintcream, mistyrose, moccasin, navajowhite, navy,
#     #         oldlace, olive, olivedrab, orange, orangered,
#     #         orchid, palegoldenrod, palegreen, paleturquoise,
#     #         palevioletred, papayawhip, peachpuff, peru, pink,
#     #         plum, powderblue, purple, red, rosybrown,
#     #         royalblue, rebeccapurple, saddlebrown, salmon,
#     #         sandybrown, seagreen, seashell, sienna, silver,
#     #         skyblue, slateblue, slategray, slategrey, snow,
#     #         springgreen, steelblue, tan, teal, thistle, tomato,
#     #         turquoise, violet, wheat, white, whitesmoke,
#     #         yellow, yellowgreen