from data import ForexData
from Technicals import Indicator
import time
import pandas as pd


class Trademanager():
    def __init__(self):
        pass

    def fetch_and_process(self,instrument):
        df = ForexData().fetch_data(instrument=instrument, count=400, granularity="M1")
        if df is not None:
            indicator = Indicator()
            ssl_df = indicator.SSL(data=df, period=10)
            baseline_df = indicator.Baseline(ssl_df, period=8)
            #logging.info(f"Data fetched and processed for instrument: {instrument}")
            return baseline_df.iloc[-1]
        return None
    
    def save_last_candle(cls):
        last_candle = []


    def running_pair_check_create_order(self,df,pair):
        instrument = pair
        last_candle_detail = df
        side = df['Position']
        if 'SIGNAL' in last_candle_detail and last_candle_detail['SIGNAL']:
            signal_currency, matching_pair= ForexData().run_check(instrument)
            if matching_pair is not None:
                current_trades = ForexData().running_trades()
                trades_to_close = current_trades[current_trades['instrument'] == matching_pair]
                for index, trade in trades_to_close.iterrows():
                    print(f"Order for id: {trade['id']} for {trade['currentUnits']} units of pair {run_pair} is getting closed as it was opened before.")
                    ForexData().close_trade(trade_id= trade['id'], units=abs(int(trade['currentUnits'])))
                    ForexData().create_order(instrument=signal_currency)
            else:
                ForexData().create_order(instrument=signal_currency, units=1000, str ="MARKET" ,side=side)
                print("ORDER CREATED")


    def create_order(self,df,pair):
        df = value
        if df is None:
            side = df['Position']
            ForexData().create_order(instrument=pair, units=1000, order_type="MARKET", side=side)
        pass

        
    


    

    
    
    

        