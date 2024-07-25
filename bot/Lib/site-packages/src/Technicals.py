import talib
import pandas as pd
import numpy as np

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
        data['SSL_BUY'] = (data['Position'] == 'buy') & (data['SIGNAL'])
        data['SSL_SELL'] = (data['Position'] == 'sell') & (data['SIGNAL'])  
        return data


    def ATR(self, data, timeperiod=14):
        data['ATR'] = talib.ATR(data['High'].values, data['Low'].values, data['Close'].values, timeperiod=timeperiod)
        data['atrup'] = data['Close'] + data['ATR']
        data['atrdown'] = data['Close'] - data['ATR']

        # Calculate SL and TP based on the Position
        data['SL'] = data.apply(lambda row: row['Close'] - (row['ATR'] * 1.5) if row['Position'] == 'buy' else row['Close'] + (row['ATR'] * 1.5), axis=1)
        data['TP'] = data.apply(lambda row: row['Close'] + row['ATR'] if row['Position'] == 'buy' else row['Close'] - row['ATR'], axis=1)

        return data
    
    def WAE(self, df, sensitivity=150, fastLength=20, slowLength=40, channelLength=20, mult=2.0):
        df['Close'] = df['Close'].astype(float)
        df['macd'], _, _ = talib.MACD(df['Close'], fastperiod=fastLength, slowperiod=slowLength, signalperiod=9)

        # Manual Bollinger Bands calculation
        df['std'] = df['Close'].rolling(window=channelLength).std()
        df['bb_upper'] = df['baseline'] + (mult * df['std'])
        df['bb_lower'] = df['baseline'] - (mult * df['std'])

        df['t1'] = (df['macd'] - df['macd'].shift(1)) * sensitivity
        df['e1'] = df['bb_upper'] - df['bb_lower']

        df['trendUp'] = np.where(df['t1'] >= 0, df['t1'], 0)
        df['trendDown'] = np.where(df['t1'] < 0, -df['t1'], 0)
        def final_signal(row):
            long_conditon = row['Close'] > row['baseline'] and row['SSL_BUY'] and row['trendUp']>row['e1']
            short_conditon = row['Close'] < row['baseline'] and row['SSL_SELL'] and row['trendDown']>row['e1']

            if long_conditon:
                return "BUY"
            elif short_conditon:
                return "SELL"
            else:
                return None

        df['FINAL_SIGNAL'] = df.apply(final_signal,axis = 1)

        return df
