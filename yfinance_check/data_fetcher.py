import pandas as pd
import numpy as np
import yfinance as yf
from backtest.backtest_check import backtester
import os

def read_file(file_path):
    with open(file_path, 'r') as file:
        contents = file.read()
    # Split contents into a list of tickers (assuming each ticker is on a new line)
    return contents.strip().split('\n')

# Path to the stocks_list.txt file
file_path = os.path.join('yfinance_check', 'stocks_list.txt')

# Read the list of tickers from the file
stocks_list = read_file(file_path)

# Initialize results dictionary
results_dict = {}
dataframes = {}

# Process each ticker
for ticker in stocks_list:
    # Download historical data for the ticker
    df = yf.download(tickers=ticker, period="max", interval="1d")
    dataframes[ticker] = df

    # Save DataFrame to a pickle file
    pickle_path = os.path.join('yfinance_check/stocks_datas', f'{ticker}_data.pkl')
    df.to_pickle(pickle_path)

    if df.empty:
        print(f"No data available for {ticker}")
        continue  # Skip processing if data is empty

    print(f"Download successful for {ticker}")

    # Apply backtesting strategy
    bt = backtester()
    bt_df = bt.strategy(df)  # Apply strategy to the dataframe
    total_gain, positive_count, negative_count, win_rate, total_trades, total_investment_collection = bt.backtest_stock(bt_df, unit=1)

    # Store results in dictionary
    results_dict[ticker] = {
        'Total Gain': total_gain,
        'Positive Gains': positive_count,
        'Negative Gains': negative_count,
        'Win %': win_rate,
        'Total Trades': total_trades,
        'Total Investment': total_investment_collection
    }

    # Print results for each ticker
    print(f"Ticker: {ticker}")
    print(f"Total Gain: {total_gain}")
    print(f"Positive Gains: {positive_count}")
    print(f"Negative Gains: {negative_count}")
    print(f"Win %: {win_rate}")
    print(f"Total Trades: {total_trades}")
    print(f"Total Investment: {total_investment_collection}\n")

# Optionally, save results to a file
results_df = pd.DataFrame(results_dict).T
results_df.to_csv(os.path.join('yfinance_check', 'backtest_results.csv'))
