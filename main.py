from data import ForexData
from Technicals import Indicator
import time
import pandas as pd
import logging
import os

# Configure logging for your script
logging.basicConfig(filename='trade_log.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Configure logging for oandapyV20 library
logger = logging.getLogger('oandapyV20')
logger.setLevel(logging.CRITICAL)

def fetch_and_process_data(instrument):
    try:
        logging.info(f"Fetching data for instrument: {instrument}")
        df = ForexData().fetch_data(instrument=instrument, count=400, granularity="M1")
        if df is not None:
            indicator = Indicator()
            ssl_df = indicator.SSL(data=df, period=10)
            baseline_df = indicator.Baseline(ssl_df, period=8)
            logging.info(f"Data fetched and processed for instrument: {instrument}")
            return baseline_df.iloc[-1]  # Return the last candle
    except Exception as e:
        logging.error(f"Error fetching and processing data for instrument {instrument}: {e}")
        return None

def save_candle_data(candle_data):
    new_data_df = pd.DataFrame(candle_data)
    try:
        if os.path.exists('candle_data.csv'):
            existing_data_df = pd.read_csv('candle_data.csv')
            combined_data_df = pd.concat([existing_data_df, new_data_df], ignore_index=True)
        else:
            combined_data_df = new_data_df

        combined_data_df.to_csv('candle_data.csv', index=False)
        logging.info("Candle data saved to candle_data.csv.")
    except PermissionError as e:
        logging.error(f"Permission error saving candle data to CSV: {e}")
        alternative_filename = 'candle_data_backup.csv'
        combined_data_df.to_csv(alternative_filename, index=False)
        logging.info(f"Backup candle data saved to {alternative_filename}.")

def main():
    instrument = [
        "EUR_USD", "USD_JPY", "GBP_USD", "AUD_USD", "USD_CAD", "USD_CHF", "NZD_USD",
        "EUR_GBP", "EUR_AUD", "EUR_NZD", "EUR_JPY", "EUR_CHF", "EUR_CAD",
        "GBP_AUD", "GBP_NZD", "GBP_JPY", "GBP_CAD", "GBP_CHF",
        "AUD_NZD", "AUD_JPY", "AUD_CHF", "AUD_CAD",
        "NZD_JPY", "NZD_CHF", "NZD_CAD",
        "CAD_JPY", "CAD_CHF", "CHF_JPY"
    ]
    candle_data = []  # Initialize an empty list to store the last candle data
    try:
        while True:
            for pair in instrument:
                last_candle = fetch_and_process_data(pair)
                if last_candle is not None:
                    logging.info(f"Last candle data: {last_candle}")
                    # Append the last_candle to the candle_data list
                    candle_data.append(last_candle.to_dict())
                    if 'SIGNAL' in last_candle and last_candle['SIGNAL']:
                        result = ForexData().run_check(pair)
                        if isinstance(result, tuple):  # Check if result is a tuple
                            check, running_pair = result
                            if check == True:
                                current_trades = ForexData().running_trades()
                                for run_pair in running_pair:
                                    print(f"{run_pair} is running and we have generated signal for {pair}")
                                    trades_to_close = current_trades[current_trades['instrument'] == run_pair]
                                    for index, trade in trades_to_close.iterrows():
                                        logging.info(f"Order for id: {trade['id']} for {trade['currentUnits']} units of pair {run_pair} is getting closed as it was opened before.")
                                        print(f"Order for id: {trade['id']} for {trade['currentUnits']} units of pair {run_pair} is getting closed as it was opened before.")
                                        ForexData().close_trade(trade_id= trade['id'], units=abs(int(trade['currentUnits'])))
                        side = last_candle['Position']
                        order_response = ForexData().create_order(instrument=pair, units=1000, order_type="MARKET", side=side)
                        print(f"Order created for pair{pair}")
                        if order_response is not None:
                            logging.info(f"Order placed for {pair}. Side: {side}, Time: {last_candle['Time']}, Details: {order_response}")
    except KeyboardInterrupt:
        logging.info("Script interrupted. Saving collected candle data.")
        save_candle_data(candle_data)

if __name__ == "__main__":
    print("Bot started.")
    main()
    print("Bot stopped.")