from src.data import ForexData
from src.Technicals import Indicator
from src.Trademanager import Trademanager
import pandas as pd

df = pd.read_csv(r"C:\Users\sachi\OneDrive\Documents\SELENIUM\data_check\ACLBSL_data.csv")
df['Open'] = df['Open'].str.replace(',', '').astype(float)
df['High'] = df['High'].str.replace(',', '').astype(float)
df['Low'] = df['Low'].str.replace(',', '').astype(float)
df['Close'] = df['Close'].str.replace(',', '').astype(float)
                 
def strategy(df):
    baseline_df = Indicator().Baseline(data=df, period=10)
    ssl_df = Indicator().SSL(data=baseline_df, period=10)
    atr_df = Indicator().ATR(data=ssl_df,timeperiod=14)
    wae_df=Indicator().WAE(df=atr_df)
    def final_signal(row):
        long_conditon = row['Close'] > row['baseline'] and row['SSL_BUY'] and row['trendUp']>row['e1']
        short_conditon = row['Close'] < row['baseline'] and row['SSL_SELL'] and row['trendDown']>row['e1']

        if long_conditon:
            return "BUY"
        elif short_conditon:
            return "SELL"
        else:
            return None
    wae_df['FINAL_SIGNAL'] = wae_df.apply(final_signal,axis = 1)
    return wae_df        

def backtest_func(df):
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



if __name__ == "__main__":
   check_df  = strategy(df)
   print(backtest_func(check_df))