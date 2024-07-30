import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import numpy as np
import yfinance as yf
from backtest.backtest_check import backtester

def backtesting(data, plot=False):
    class SSLStrategy(Strategy):
        # Define strategy parameters
        period = 10
        
        @staticmethod
        def SSL(data, period):
            data = data.copy()
            data['smaHigh'] = data['High'].rolling(window=period).mean()
            data['smaLow'] = data['Low'].rolling(window=period).mean()
            data['sslDown'] = np.where(data['Close'] < data['smaLow'], data['smaHigh'], data['smaLow'])
            data['sslUp'] = np.where(data['Close'] < data['smaLow'], data['smaLow'], data['smaHigh'])
            data['Position'] = np.where(data['smaLow'] == data['sslDown'], 'buy', 'sell')
            data['SIGNAL'] = data['Position'] != data['Position'].shift(1)
            data['SSL_BUY'] = (data['Position'] == 'buy') & (data['SIGNAL'])
            data['SSL_SELL'] = (data['Position'] == 'sell') & (data['SIGNAL'])
            return data

        def init(self):
            # Initialize indicators
            ssl_data = self.SSL(self.data.df, self.period)
            self.ssl_down = self.I(lambda: ssl_data['sslDown'], name='sslDown')
            self.ssl_up = self.I(lambda: ssl_data['sslUp'], name='sslUp')

        def next(self):
            # Trading logic
            if crossover(self.ssl_up, self.ssl_down):
                self.buy()
            elif crossover(self.ssl_down, self.ssl_up):
                if self.position:
                    self.position.close()

    # Ensure the data has DatetimeIndex for resampling
    if not isinstance(data.index, pd.DatetimeIndex):
        data.index = pd.to_datetime(data.index)

    # Process data
    df = data.copy()  # Ensure df is a copy
    df = backtester.strategy(df=df)
    df.dropna(inplace=True)
    
    # Ensure the data has SSL columns
    df = SSLStrategy.SSL(df, SSLStrategy.period)
    
    # Check for empty data
    if df.empty:
        print("Data is empty after applying SSL strategy.")
        return None
    
    # Resample data to weekly frequency
    df_resampled = df.resample('W').last()
    
    # Check resampled data
    if df_resampled.empty:
        print("Resampled data is empty.")
        return None

    # Set up and run the backtest
    bt = Backtest(df, SSLStrategy, cash=10_000, commission=0.02)
    stats = bt.run()
    print(stats)

    if plot:
        bt.plot()
    return stats

if __name__ == "__main__":
    # Download data
    data = pd.read_csv(r"C:\Users\sachi\OneDrive\Documents\BOTS\nnfx_bot\nepse\data_check\UNHPL_data.csv")
    print(data)
    
    # Ensure the 'Date' column is a datetime object and set it as the index
    data['Date'] = pd.to_datetime(data['Date'], format='%Y/%m/%d')
    data.set_index('Date', inplace=True)
    
    # Ensure the index is in the desired format
    data.index = data.index.strftime('%Y-%m-%d')
    
    backtesting(data=data, plot=True)
