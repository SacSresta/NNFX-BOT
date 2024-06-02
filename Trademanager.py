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
            logging.info(f"Data fetched and processed for instrument: {instrument}")
            return baseline_df.iloc[-1]
        return None
    
    def save_last_candle(cls):
        last_candle = []


    def pair_run_check(self,instrument):
        last_candle_detail = self.fetch_and_process(instrument)
            if 'SIGNAL' in last_candle_detail and last_candle_detail['SIGNAL']:
                check_run = ForexData().run_check(instrument)
                if isinstance(check_run,tuple):
                    check, running_pair = check_run
                    if check ==True:
                        return running_pair
                    else:
                        return None
    
    
    

        