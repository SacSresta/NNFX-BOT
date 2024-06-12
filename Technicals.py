from data import ForexData
import talib
import plotly.graph_objects as go
import technical

class Indicator:
    def SMA_CROSS(self, data, short_period, long_period):
        data[f'SMA_{short_period}'] = talib.SMA(data['Close'].values, timeperiod=short_period)
        data[f'SMA_{long_period}'] = talib.SMA(data['Close'].values, timeperiod=long_period)
        return data
    

    
    def Baseline(self, data,period):
        data['baseline'] = data['Close'].rolling(window=period).mean()
        return data



    def SSL(self, data, period):
        data['smaHigh'] = data['High'].rolling(window=period).mean()
        data['smaLow'] = data['Low'].rolling(window=period).mean()
        data['sslDown'] = data.apply(lambda row: row['smaHigh'] if row['Close'] < row['smaLow'] else row['smaLow'], axis=1)
        data['sslUp'] = data.apply(lambda row: row['smaLow'] if row['Close'] < row['smaLow'] else row['smaHigh'], axis=1)
        data['Position'] = data.apply(lambda row: "buy" if row['smaLow'] == row['sslDown'] else "sell", axis=1)
        data['SIGNAL'] = data['Position'] != data['Position'].shift(1)  
        return data


    def ATR(self, data, timeperiod=14):
        data['ATR'] = talib.ATR(data['High'].values, data['Low'].values, data['Close'].values, timeperiod=timeperiod)
        data['atrup'] = data['Close'] + data['ATR']
        data['atrdown'] = data['Close'] - data['ATR']

        # Calculate SL and TP based on the Position
        data['SL'] = data.apply(lambda row: row['Close'] - (row['ATR'] * 1.5) if row['Position'] == 'buy' else row['Close'] + (row['ATR'] * 1.5), axis=1)
        data['TP'] = data.apply(lambda row: row['Close'] + row['ATR'] if row['Position'] == 'buy' else row['Close'] - row['ATR'], axis=1)

        return data

if __name__ == "__main__":
    forex_data = ForexData()
    df = forex_data.fetch_data("GBP_USD")
    indicator = Indicator()
    print(indicator.SMA_CROSS(df, 8, 10))
    print(indicator.SSL(df, 10))
    print(indicator.ATR(df, 14))