import pandas as pd

df = pd.read_csv(f"./data_production/EURUSD-Z_1D.csv",index_col='time')
print(df)
import os
cwd = os.getcwd()
print(cwd)