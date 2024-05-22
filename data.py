import json
from oandapyV20 import API    # the client
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.orders as orders
import pandas as pd
import time




accountID = "101-011-24509333-001"
access_token = "2092774d87027059265e897f7452eaa9-d4a0390dbef600c8119e62ab83b0b5a2"

# Create an API context
class ForexData:
    def __init__(self, accountID = "101-011-24509333-001", access_token = "2092774d87027059265e897f7452eaa9-d4a0390dbef600c8119e62ab83b0b5a2"):
        self.api = API(access_token=access_token)
        self.accountID =accountID

    def fetch_data(self, instrument, count=5000, granularity="H1", price="M"):
        params = {
            "count": count,
            "granularity": granularity,
            "price": price
        }
        r = instruments.InstrumentsCandles(instrument=instrument, params=params)
        response = self.api.request(r)
        return self.process_data(response)

    def process_data(self, response):
        prices = [(candle['time'], candle['mid']['o'], candle['mid']['h'], candle['mid']['l'], candle['mid']['c']) for candle in response['candles']]
        df = pd.DataFrame(prices, columns=['Time', 'Open', 'High', 'Low', 'Close'])
        df['Time'] = pd.to_datetime(df['Time'])
        df['Time'] = df['Time'].dt.tz_convert('Australia/Sydney')
        for col in ['Open', 'High', 'Low', 'Close']:
            df[col] = df[col].astype(float)
        return df
    
    def fetch_tradable_instruments(self):
        r = accounts.AccountInstruments(accountID=self.accountID)
        response = self.api.request(r)
        return response['instruments']
    
    def fetch_last_candle(self, instrument, granularity="M1"):
        return self.fetch_data(instrument=instrument, count=1, granularity=granularity, price="M")
    
    def create_order(self, instrument, units, order_type="MARKET", side="buy"):
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
        r = orders.OrderCreate(accountID=self.accountID, data=data)
        try:
            response = self.api.request(r)
            print("Order created successfully:")
            print(json.dumps(response, indent=2))
            return response
        except oandapyV20.exceptions.V20Error as err:
            print(f"Error creating order: {err}")
            return None
    
    
    

if __name__ == "__main__":
    forex_data = ForexData()
    instruments = forex_data.fetch_tradable_instruments()
    print(instruments)
    