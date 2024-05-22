from data import ForexData
from Technicals import Indicator
import time
import oandapyV20.endpoints.orders as orders
import pandas as pd
import logging

# Configure logging
logging.basicConfig(filename='trade_log.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Initialize an empty list to store the last candle data
candle_data = []

def fetch_and_process_data(instrument):
    try:
        df = ForexData().fetch_data(instrument=instrument, count=400, granularity="M1")
        if df is not None:
            indicator = Indicator()
            ssl_df = indicator.SSL(data=df, period=10)
            baseline_df = indicator.Baseline(ssl_df, period=8)
            return baseline_df.iloc[-1]  # Return the last candle
    except Exception as e:
        logging.error(f"Error fetching and processing data: {e}")
        return None

def create_order(instrument, units, order_type="MARKET", side="buy"):
    """
    Create an order with the given parameters.
    """
    # Define the order data
    data = {
        "order": {
            "instrument": instrument,
            "units": str(units) if side.lower() == "buy" else str(-units),
            "type": order_type,
            "positionFill": "DEFAULT"
        }
    }

    # Create the order request
    r = orders.OrderCreate(accountID=accountID, data=data)
    try:
        response = api.request(r)
        logging.info(f"Order created: {response}")
        return response
    except oandapyV20.exceptions.V20Error as err:
        logging.error(f"Error creating order: {err}")
        return None

def main():
    instrument = "EUR_USD"
    global candle_data  # Use the global candle_data list
    while True:
        last_candle = fetch_and_process_data(instrument)
        if last_candle is not None:
            print("Last candle:")
            print(last_candle)
            # Append the last_candle to the candle_data list
            candle_data.append(last_candle.to_dict())
            if last_candle['SIGNAL']:
                side = last_candle['Position']
                order_response = create_order(instrument=instrument, units=1000, order_type="MARKET", side=side)
                if order_response is not None:
                    logging.info(f"Order placed. Side: {side}, Time: {last_candle['Time']}, Details: {order_response}")

        time.sleep(60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # When the script is interrupted, save the collected data to a DataFrame and analyze
        df_candle_data = pd.DataFrame(candle_data)
        print("Collected candle data:")
        print(df_candle_data)
        df_candle_data.to_csv('candle_data.csv', index=False)
        logging.info("Script interrupted. Candle data saved to candle_data.csv.")
