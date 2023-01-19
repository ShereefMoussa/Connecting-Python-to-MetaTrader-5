from flask import Flask
# from dash import Dash
from dash import Dash, html
# dcc,  Input, Output, callback


server = Flask('myproject')
app = Dash(server=server
           ,external_stylesheets=['external_stylesheets.css'] 
        )

app.head = [html.Link(rel='stylesheet', href='./static/stylesheet.css'),
    ('''
    <style type="text/css">
    .user-select-none.svg-container {
    height: 750px;
    }
    </style>
    ''')]