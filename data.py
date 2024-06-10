import json
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
from oandapyV20.exceptions import V20Error
import oandapyV20.endpoints.positions as position
import pandas as pd
import time

accountID = "101-011-24509333-004"
access_token = "5c2da6fbe43ec464a3816fc74229f496-e6769428284068cfcf8dca4a32febf83"

class ForexData:
    def __init__(self, accountID=accountID, access_token=access_token):
        self.api = API(access_token=access_token)
        self.accountID = accountID

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
        df=pd.merge(df,pd.DataFrame(response),left_index=True, right_index=True,how = 'inner')
        if 'candles' in df.columns:
            df = df.drop(columns='candles')
        df=df[['instrument', 'Time', 'granularity', 'Open', 'High', 'Low', 'Close']]
        return df

    def fetch_tradable_instruments(self):
        r = accounts.AccountInstruments(accountID=self.accountID)
        response = self.api.request(r)
        return [instrument['name'] for instrument in response['instruments'] if instrument['type'] == 'CURRENCY']

    def fetch_last_candle(self, instrument, granularity="M1"):
        return self.fetch_data(instrument=instrument, count=1, granularity=granularity, price="M")
    
    def create_order(self, instrument, units, order_type="MARKET", side="buy"):
        data = {
            "order": {
                "instrument": instrument,
                "units": str(units) if side.lower() == "buy" else str(-units),
                "type": order_type,
                "positionFill": "DEFAULT"
            }
        }
        r = orders.OrderCreate(accountID=self.accountID, data=data)
        try:
            response = self.api.request(r)
            return response
        except V20Error as err:
            return None

    def running_trades(self):
        r = trades.TradesList(accountID=self.accountID)
        response = self.api.request(r)
        return pd.DataFrame(response['trades'])

    def run_check(self, pair):
        try:
            current_trades_df = self.running_trades()
            if current_trades_df.empty:
                return False,[]
            
            current_trade_pairs = current_trades_df['instrument'].tolist()
            signal_currency = pair.split("_")
            matching_pairs = []  # List to store all matching pairs

            for current_trade_pair in current_trade_pairs:
                current_trade_currency = current_trade_pair.split("_")
                # Check if any part of the trade pair matches the signal currency
                if (signal_currency[0] in current_trade_currency or signal_currency[1] in current_trade_currency):
                    matching_pairs.append(current_trade_pair)
            if matching_pairs:
                return True, matching_pairs  # Return True with a list of all matching pairs
            else:
                return False, []
        except Exception as e:
            return"Unable to check the running trades."      

    def close_trade(self, trade_id, units=None):
        data = {
            "units": "ALL" if units is None else str((units))  # Ensure units are positive and correctly formatted
        }
        r = trades.TradeClose(accountID=self.accountID, tradeID=trade_id, data=data)
        try:
            response = self.api.request(r)
            return response
        except V20Error as err:
            print(f"Error closing trade {trade_id}: {err}")
            return None
        
    def get_account_balance(self):

        """
        Retrieves the current account balance from an OANDA v20 account.
        
        Args:
        - account_id (str): Your OANDA account ID.
        - access_token (str): Your OANDA API access token.
        
        Returns:
        - float: The account balance.
        """
        account = accounts.AccountDetails(ForexData().accountID)
        response = ForexData().api.request(account)

    # Extract the balance from the response
        balance = float(response['account']['balance'])
        return balance

if __name__ == "__main__":
    forex_data = ForexData()
    r = trades.TradesList(accountID=ForexData().accountID)
    response = ForexData().api.request(r)
    print(response)