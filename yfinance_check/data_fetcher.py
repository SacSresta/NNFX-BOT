import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import yfinance as yf
import talib
from backtest import backtest_check

df = yf.download(tickers="AAPL", period = "max",interval = "1d")


class backtest():
  def strategy(df):
      baseline_df = Indicator().Baseline(data=df, period=10)
      ssl_df = Indicator().SSL(data=baseline_df, period=10)
      atr_df = Indicator().ATR(data=ssl_df,timeperiod=14)
      wae_df=Indicator().WAE(df=atr_df)
      return wae_df


  def backtest_forex(df):
    entry_price = None
    trade_type = None
    pips_gained = []
    for index, row in df.iterrows():
      if row['FINAL_SIGNAL'] == 'SELL' or row['FINAL_SIGNAL'] == 'BUY':
        if entry_price is None:
          entry_price = row['Close']
          trade_type = row['FINAL_SIGNAL']
          print(entry_price,trade_type)
        elif entry_price is not None:

          exit_price = row['Close']
          pips = exit_price - entry_price if trade_type == "SELL" else entry_price - exit_price
          pips_gained.append(abs(pips))
          print(exit_price,entry_price,abs(pips))

          entry_price = row['Close']
          trade_type = row['FINAL_SIGNAL']
          print(entry_price,trade_type)

    return sum(pips_gained)



  def backtest_stock(df):
      collection = []           # Define inside the function to keep the state within the function scope
      collection_units = []     # Define inside the function to keep the state within the function scope
      gain_amount = []
      positive_count = 0        # Initialize the positive count
      negative_count = 0        # Initialize the negative count

      unit = 10
      for index, row in df.iterrows():
          if row['FINAL_SIGNAL'] == "BUY":
              investment = unit * row['Close']
              collection_units.append(unit)
              collection.append(investment)
          elif row['FINAL_SIGNAL'] == "SELL":
              if collection:
                  total_investment = sum(collection)
                  total_units = sum(collection_units)
                  total_selling_price = row['Close'] * total_units
                  gain = total_selling_price - total_investment
                  gain_amount.append(gain)
                  print(f"Sold Units: {total_units}")
                  print(f"Total investment: {total_investment}")
                  print(f"Total Selling Price: {total_selling_price}")
                  print(f"Gain from stock: {gain}")
                  collection = []  # Reset collection after selling
                  collection_units = []  # Reset units after selling
                  if gain > 0:
                      positive_count += 1
                  elif gain < 0:
                      negative_count += 1

      total_gain = sum(gain_amount)
      total_trades = positive_count + negative_count
      win_rate = (positive_count / total_trades * 100) if total_trades > 0 else 0

      print(f"Total Gain: {total_gain}")
      print(f"Positive Gains: {positive_count}")
      print(f"Negative Gains: {negative_count}")
      print(f"Win %: {win_rate}")

  # Example usage:
  # Assuming df is your DataFrame with the necessary columns
  # stock_bt(df)


backtest = backtest_check.strategy(df=df)
print(backtest)