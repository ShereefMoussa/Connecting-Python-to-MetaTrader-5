# from modules import *
# from variables import *
# from utilities import *

# def chart_populate_fuc(data_loc):
#     symbols_dic ,time_frame_dic = get_symbols_and_tf('data_production')

#     app = Dash(__name__)

#     app.layout = html.Div([
#         # html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),
#         dcc.Dropdown(id="symbols",
#                     options=symbols_dic,
#                     multi=False,
#                     value='EURUSD-Z',
#                     style={'width': "40%"}
#                     ),
        
#         dcc.Dropdown(id="time_frame",
#                     options=time_frame_dic,
#                     multi=False,
#                     value='1M',
#                     style={'width': "40%"}
#                     ),
        
#         html.Div(id='output_container', children=[]),
#         html.Br(),
#         dcc.Graph(id='chart', figure={})
#     ])

#     @app.callback(
#         [
#         Output(component_id='output_container', component_property='children'),
#         Output(component_id='chart', component_property='figure')],
#         [Input(component_id='symbols', component_property='value'),
#         Input(component_id='time_frame', component_property='value')]
#     )
#     def update_graph(option_slctd_1,option_slctd_2):

#         container = "The year chosen by user was: {}".format(option_slctd_1)

#         df = pd.read_csv(f"./data_production/{option_slctd_1}_{option_slctd_2}.csv",index_col='time')
#         df.index = pd.to_datetime(df.index)

#         fig = make_subplots(vertical_spacing = 0, rows=3, cols=1,
#                             specs=[[{"secondary_y": True}],[{"secondary_y": True}],
#                                     [{"secondary_y": True}]],
#                             row_heights=[0.6, 0.03,0.13],shared_xaxes=True)
#         # Candlestick
#         fig.add_trace(go.Candlestick(x=df.index,
#                                     open=df['open'],
#                                     high=df['high'],
#                                     low=df['low'],
#                                     close=df['close'],
#                                     name='candle',
#                                     text=df.index,
#                                     # bgcolor = '#ff0000'
#                                     # gridcolor='Red'
#                                     ))
#         # fig.update_traces(gridcolor='lightyellow', selector=dict(type='candlestick'))
#         # volume
#         fig.add_trace(go.Bar(x=df.index, y = df['tick_volume'], name='volume'), row=2, col=1)
#         # macd
#         if 'macd' in df.columns:
#             fig.add_trace(go.Bar(x=df.index, y = df['macd'], name='macd'), row=3, col=1)
#         if 'rsi' in df.columns:
#             fig.add_trace(go.Scatter(x=df.index, y = df['rsi'], name='RSI'), row=3, col=1,secondary_y=True)
#         # ma
#         if 'ema_200' in df.columns:
#             fig.add_trace(go.Scatter(x=df.index, y=df['ema_200'],opacity=0.7, name='ema_200'))

#         # fig.add_trace(go.scatter(x=df.index, y = df['high'],opacity=0.7))
#         if 'zig_top' in df.columns:
#             x_zig , y_zig = populate_x_y(df,['zig_top','zig_bottom'])
#             fig.add_trace(go.Scatter(x = x_zig, 
#                                 y = y_zig,
#                                 mode='lines+markers',
#                                 connectgaps=True, name='zip'
#                                 ))
        
#         if 'sup_top' in df.columns:
#             x_sup , y_sup = populate_x_y(df,['sup_top','sup_bottom'])
#             fig.add_trace(go.Scatter(x = x_sup, 
#                                     y = y_sup,
#                                     mode='lines+markers',
#                                     connectgaps=True, name='sup'
#                                     ))

#         fig.update_layout(
#             # paper_bgcolor="#055000", # very back
#             title= f'{option_slctd_1} {option_slctd_2}',
#             margin=dict(
#             l=9,
#             r=3,
#             b=30,
#             t=30,
#             pad=0),
#             # yaxis_title='AAPL Stock',
#             # shapes = [dict(
#             #     x0='2022-5-06 22:00', x1='2022-5-06 22:00', y0=0, y1=1, xref='x', yref='paper',
#             #     line_width=1)]
#             )
#         fig.update_yaxes(gridcolor='darkgray')
#         fig.update_xaxes(
#             # showline=True, linewidth=2, linecolor='black',
#             gridcolor='darkgray',
#             rangeslider_visible=False,
#             rangebreaks=[
#                 # NOTE: Below values are bound (not single values), ie. hide x to y
#                 dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
#                 # dict(bounds=[16, 9.5], pattern="hour"),  # hide hours outside of 9.30am-4pm
#                 # dict(values=["2019-12-25", "2020-12-24"])  # hide holidays (Christmas and New Year's, etc)
#             ])

#         # fig.update_layout(xaxis_rangeslider_visible=False)
#         # fig.update_layout(xaxis_rangeslider_visible=False, 
#         #                 # xaxis4_rangeslider_visible=True, 
#         #                 xaxis_type="date")
#         # fig.show(auto_open=False)

#         return container, fig

#     # if __name__ == '__main__':
#     app.run_server(debug=True)
        
    
