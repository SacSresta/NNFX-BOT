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

# Initialize an empty list to store the last candle data
candle_data = []


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

def main():
    instrument = "EUR_USD"
    global candle_data  # Use the global candle_data list
    while True:
        last_candle = fetch_and_process_data(instrument)
        if last_candle is not None:
            logging.info(f"Last candle data: {last_candle}")
            # Append the last_candle to the candle_data list
            candle_data.append(last_candle.to_dict())
            if 'SIGNAL' in last_candle and last_candle['SIGNAL']:
                side = last_candle['Position']
                order_response = ForexData().create_order(instrument=instrument, units=1000, order_type="MARKET", side=side)
                if order_response is not None:
                    logging.info(f"Order placed. Side: {side}, Time: {last_candle['Time']}, Details: {order_response}")

        time.sleep(60)

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

if __name__ == "__main__":
    print("Bot started.")
    try:
        main()
    except KeyboardInterrupt:
        print("Bot stopped.")
        logging.info("Script interrupted. Saving collected candle data.")
        save_candle_data(candle_data)
