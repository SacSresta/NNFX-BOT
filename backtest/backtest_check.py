from src.data import ForexData
from src.Technicals import Indicator
from src.Trademanager import Trademanager
import pandas as pd

class backtester():
    @staticmethod
    def strategy(df):
        # Assuming Indicator methods are static methods or accessible directly
        baseline_df = Indicator().Baseline(data=df, period=8)
        ssl_df = Indicator().SSL(data=baseline_df, period=10)
        atr_df = Indicator().ATR(data=ssl_df, timeperiod=14)
        wae_df = Indicator().WAE(df=atr_df)
        return wae_df

    @staticmethod
    def backtest_forex(df):
        entry_price = None
        trade_type = None
        pips_gained = []
        for index, row in df.iterrows():
            if row['FINAL_SIGNAL_shift'] == 'SELL' or row['FINAL_SIGNAL_shift'] == 'BUY':
                if entry_price is None:
                    entry_price = row['Close']
                    trade_type = row['FINAL_SIGNAL_shift']
                    print(entry_price, trade_type)
                elif entry_price is not None:
                    exit_price = row['Close']
                    pips = exit_price - entry_price if trade_type == "SELL" else entry_price - exit_price
                    pips_gained.append(abs(pips))
                    print(exit_price, entry_price, abs(pips))
                    entry_price = row['Close']
                    trade_type = row['FINAL_SIGNAL_shift']
                    print(entry_price, trade_type)

        return sum(pips_gained)

    @staticmethod
    def backtest_stock(df,unit = 10):
        collection = []
        collection_units = []
        gain_amount = []
        positive_count = 0
        negative_count = 0
        total_collection_inv = []

        unit = unit
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
                    total_collection_inv.append(total_investment)
                    collection = []
                    collection_units = []
                    if gain > 0:
                        positive_count += 1
                    elif gain < 0:
                        negative_count += 1

        total_gain = sum(gain_amount)
        total_trades = positive_count + negative_count
        win_rate = (positive_count / total_trades * 100) if total_trades > 0 else 0

        return total_gain, positive_count, negative_count, win_rate,total_trades,sum(total_collection_inv)


