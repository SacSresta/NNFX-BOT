from src.data import ForexData
from src.Technicals import Indicator
import time
import pandas as pd
import numpy as np


class Trademanager():
    def __init__(self):
        self.account_bal = ForexData().get_account_balance()

    def fetch_data(self,instrument,count = 400,granularity = "M1",price_type = "mid"):
        df = ForexData().fetch_data(instrument=instrument, count=count, granularity=granularity,price_type=price_type)
        if df is not None:
            indicator = Indicator()
            ssl_df = indicator.SSL(data=df, period=10)
            Atr_df = indicator.ATR(data=ssl_df, timeperiod= 14)
            baseline_df = indicator.Baseline(Atr_df, period=8)
            #logging.info(f"Data fetched and processed for instrument: {instrument}")
            return baseline_df
        return None

    def fetch_and_process(self,instrument,count = 400,granularity = "M1",price_type = "mid"):
        df = ForexData().fetch_data(instrument=instrument, count=count, granularity=granularity,price_type=price_type)
        if df is not None:
            indicator = Indicator()
            ssl_df = indicator.SSL(data=df, period=10)
            Atr_df = indicator.ATR(data=ssl_df, timeperiod= 14)
            baseline_df = indicator.Baseline(Atr_df, period=8)
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

    def trades_to_close_df(self, matching_pairs):
        current_trades = ForexData().running_trades()
        list_df = []
        for matching_pair in matching_pairs:
            trades_to_close = current_trades[current_trades['instrument'] == matching_pair]
    
        return trades_to_close


    def _close_relevant_trades(self, pair, running_pairs, current_trades):
        """
        Close the relevant trades based on the running pairs.
        
        Args:
        - pair (str): The currency pair for which the signal was generated.
        - running_pairs (list): List of currency pairs currently running.
        - current_trades (DataFrame): DataFrame of current running trades.
        """
        for run_pair in running_pairs:
            if pair == run_pair:
                print(f"{run_pair} is running and we have generated a signal for {pair}")
                trades_to_close = current_trades[current_trades['instrument'] == run_pair]
                for index, trade in trades_to_close.iterrows():
                    #logging.info(f"Order for id: {trade['id']} for {trade['currentUnits']} units of pair {run_pair} is getting closed as it was opened before.")
                    print(f"Order for id: {trade['id']} for {trade['currentUnits']} units of pair {run_pair} is getting closed as it was opened before.")
                    ForexData().close_trade(trade_id=trade['id'], units=abs(int(trade['currentUnits'])))

    def position_size_calculator(self,risk_pct = 0.02,stop_loss = None,ask = None):
        if stop_loss is None:
            raise ValueError("Stop loss must be specified")
        account_bal = self.account_bal
        risk_amount = account_bal * risk_pct
        position_size = risk_amount / stop_loss
        return position_size * 10000

    def pip_size(self, last_candle):
        pipLocation = ForexData().pipLocation(pair=last_candle['instrument'])
        if pipLocation is None:
            return None
        pip_value = pow(10, float(abs(pipLocation)))
        
        return round(last_candle['ATR'] * pip_value)
    
if __name__ == "__main__":
    last_candle = Trademanager().fetch_and_process(instrument="AUD_JPY",granularity="M1",price_type="ask")
    pipvalue = Trademanager().pip_size(last_candle)
    unit = Trademanager().position_size_calculator(stop_loss=pipvalue*1.5,risk_pct=0.02)
    print(Trademanager().account_bal)
    print(pipvalue *1.5)
    print(last_candle['Close'])
    print(unit * last_candle['Close'])


    
    
    

        