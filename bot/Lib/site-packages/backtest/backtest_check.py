from src.data import ForexData
from src.Technicals import Indicator
from src.Trademanager import Trademanager
import pandas as pd

# Load and preprocess data

df = pd.read_csv(r"C:\Users\sachi\OneDrive\Documents\BOTS\SELENIUM\data_check\ACLBSL_data.csv")



# Rest of your code
def strategy(df):
    # Apply technical indicators
    baseline_df = Indicator().Baseline(data=df, period=10)
    ssl_df = Indicator().SSL(data=baseline_df, period=10)
    atr_df = Indicator().ATR(data=ssl_df, timeperiod=14)
    wae_df = Indicator().WAE(df=atr_df)
    
    def final_signal(row):
        long_condition = (
            row['Close'] > row['baseline'] and 
            row['SSL_BUY'] and 
            row['trendUp'] > row['e1']
        )
        short_condition = (
            row['Close'] < row['baseline'] and 
            row['SSL_SELL'] and 
            row['trendDown'] > row['e1']
        )

        if long_condition:
            return "BUY"
        elif short_condition:
            return "SELL"
        else:
            return None
    
    wae_df['FINAL_SIGNAL'] = wae_df.apply(final_signal, axis=1)
    return wae_df        

def backtest_func(df):
    entry_price = None
    trade_type = None
    pips_gained = []
    
    for index, row in df.iterrows():
        if row['FINAL_SIGNAL'] in ['SELL', 'BUY']:
            if entry_price is None:
                entry_price = row['Close']
                trade_type = row['FINAL_SIGNAL']
                print(f"Entry Price: {entry_price}, Trade Type: {trade_type}")
            else:
                exit_price = row['Close']
                pips = exit_price - entry_price if trade_type == "SELL" else entry_price - exit_price
                pips_gained.append(abs(pips))
                print(f"Exit Price: {exit_price}, Entry Price: {entry_price}, Pips Gained: {abs(pips)}")

                # Update entry price and trade type
                entry_price = row['Close']
                trade_type = row['FINAL_SIGNAL']
                print(f"Entry Price: {entry_price}, Trade Type: {trade_type}")

    return sum(pips_gained)

if __name__ == "__main__":
    check_df = strategy(df)
    total_pips = backtest_func(check_df)
    print(f"Total Pips Gained: {total_pips}")
