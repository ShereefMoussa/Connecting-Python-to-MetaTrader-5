import multiprocessing as multi
import concurrent.futures as conf
import time
from datetime import datetime, timedelta
import pytz
import sys
import glob, os
from os.path import exists
import threading
import winsound


import numpy as np
import pandas as pd
import MetaTrader5 as mt5
import talib 

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# import cufflinks as cf
import dash
from dash import Dash, html, dcc
from dash.dependencies import Input ,Output

from indicators import *
from strategies import *
from log_fun import *
# set data frame view
pd.set_option('display.max_columns', 500) # number of columns to be displayed
pd.set_option('display.width', 1600)      # max table width to display
