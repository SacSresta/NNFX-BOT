from src.data import ForexData
from src.Technicals import Indicator
import time
import pandas as pd
import logging
import os
from src.logger import LogWrapper
from src.Trademanager import Trademanager
from src.utils import save_all_candle_data,save_candle_data
from src.Strategy import last_candle_function,running_trades
def main():
    instrument = [
        "EUR_USD", "USD_JPY", "GBP_USD", "AUD_USD", "USD_CAD", "USD_CHF", "NZD_USD",
        "EUR_GBP", "EUR_AUD", "EUR_NZD", "EUR_JPY", "EUR_CHF", "EUR_CAD",
        "GBP_AUD", "GBP_NZD", "GBP_JPY", "GBP_CAD", "GBP_CHF",
        "AUD_NZD", "AUD_JPY", "AUD_CHF", "AUD_CAD",
        "NZD_JPY", "NZD_CHF", "NZD_CAD",
        "CAD_JPY", "CAD_CHF", "CHF_JPY"
    ]  
    candle_data_all = []# Initialize an empty list to store the last candle data
    try:
        while True:
            for instrument in ForexData().tradable_instruments():
                last_candle = last_candle_function(instrument=instrument,granularity="M1")
                running_trades_list = running_trades(last_candle=last_candle,pair = instrument)              
            
            time.sleep(60)
    except KeyboardInterrupt:
        logging.info("Script interrupted. Saving collected candle data.")
        save_all_candle_data(candle_data_all)
if __name__ == "__main__":
    print("Bot started.")
    main()
    print("Bot stopped.")