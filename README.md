# Connecting Python to MetaTrader 5

> :warning: **Warning: I share the project to share my experience coding. not to give any investment advice and if you want to use any piece of my code, do it at your own risk.**

> :warning: **I found that Metatrader 5 can handle the processing data, backtest, visualization, and measure performance far better than Metatrader 4. So the project is deprecated because I don't need to use any python machine-learning modules for now.**


 This project is about connecting Python to MetaTrader 5, pulling data, processing the data, and trading order execution.


## The Goal of the project:

- Make a bridge between metatrader 5 and python script.
- pulling data & always checking if the connection is not lost. to pull the missing data from last raw.
- Processing data adding technical indicators like moving average and MACD.
- visualize the data to make sure everything is correct.
- Testing trading strategy to to measure it's performance.

## How it works:

- Change the variables you need in script/variables.py (username - password - server name - symbols you want to trade - timeframe - risk tolerance) 
- Create your strategy in script/strategies folder in a new file.
- Don't forget to change script/strategies/__init__.py based on what you did.
- Put your new function inside "strategies function" in script/indicators_and_strategies.py.
- Run the script/main.py file.
- the main.py file will run two functions. the first "chart_populate_fuc" for streaming data using dash module. the second "core" for pulling and processing data.
- 