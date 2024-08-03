import pandas as pd 
from backtest.backtest_check import backtester
import os 

folder_path = r"C:\Users\sachi\OneDrive\Documents\BOTS\nnfx_bot\nepse\nepse_pickles"

list_of_stats = []

for file in os.listdir(folder_path):
    if file.endswith(".pkl"):
        path = os.path.join(folder_path, file)
        try:
            df = pd.read_pickle(path)  # Use the variable path without raw string
            df.rename(columns={"Date": "Time", "Ltp": "Close"}, inplace=True)
            df['Open'] = df['Open'].str.replace(',', '').astype(float)
            df['High'] = df['High'].str.replace(',', '').astype(float)
            df['Low'] = df['Low'].str.replace(',', '').astype(float)
            df['Close'] = df['Close'].str.replace(',', '').astype(float)
            stocks_df = backtester().strategy(df)
            name = file.split('_')[0]
            stats = backtester().stock_backtesting(df=df,name=name)
            list_of_stats.append(stats)
        except Exception as e:
            print(f"Error reading {file}: {e}")

stats_df = pd.DataFrame(list_of_stats)

stats_df.to_csv('nepse_stats.csv')