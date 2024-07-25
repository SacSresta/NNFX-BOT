from src.data import ForexData
from src.Technicals import Indicator
import time
import pandas as pd
import logging
import os
from src.logger import LogWrapper
from src.Trademanager import Trademanager
from src.utils import save_all_candle_data,save_candle_data
from src.Exception import CustomException

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def last_candle_function(instrument,granularity):
    candle_data_all = []
    try:
        last_candle = Trademanager().fetch_and_process(instrument=instrument,granularity=granularity)
        if last_candle is not None:
            candle_data_all.append(last_candle)       
        save_all_candle_data(candle_data_all)
        return last_candle

    except CustomException as e:
        logger.error("Error in function 'last_candle' : %s",e)
        return None
    
def running_trades(last_candle,pair):
    try:
        if 'SIGNAL' in last_candle and last_candle['SIGNAL']:
            print(f"Found signal for {pair}")
            check,matching_pair = ForexData().run_check(pair=pair)
            print(check)
            print(matching_pair)
            if check is True:
                final_check(matching_pair=matching_pair,pair=pair,last_candle=last_candle)
            
            elif check is False:
                units,SL,TP,side = order_manager(last_candle=last_candle,pair=pair)
                order_response = ForexData().create_order(instrument=pair,units=round(units),order_type="MARKET",side = side, stop_loss=SL,take_profit=TP)
                if order_response is not None:
                    print(f"Order placed for {pair}. Side: {side}, Time: {last_candle['Time']},Details:{order_response}")

            else:
                return "No active trades"
        else:
            print(f"Signal Not found for {pair}")    
    except CustomException as e:
        print(e)


def final_check(pair, matching_pair,last_candle):
    try:
        for trades in matching_pair:
            if trades != pair:
                trade_id, units = closing_running_trades(pair=trades)
                print(f"{pair} this is trades:{trades}")
                ForexData().close_trade(trade_id=trade_id, units=abs(int(units)))
                units,SL,TP,side = order_manager(last_candle=last_candle,pair=pair)
                order_response = ForexData().create_order(instrument=pair,units=round(units),order_type="MARKET",side = side, stop_loss=SL,take_profit=TP)
                if order_response is not None:
                    print(f"Order placed for {pair}. Side: {side}, Time: {last_candle['Time']},Details:{order_response}")
                    return "This is just a check"

            elif trade == pair:
                pass
    except CustomException as e:
        return str(e)


def closing_running_trades(pair):
    for index,trades in ForexData().running_trades().iterrows():
        if trades['instrument'] == pair:
            return trades['id'],trades['currentUnits']    




def order_manager(last_candle,pair):
    side = last_candle['Position']
    price_type = 'bid' if side == "buy" else 'ask'
    last_candle = Trademanager().fetch_and_process(instrument=pair, price_type=price_type, granularity="D")
    pipvalue = Trademanager().pip_size(last_candle)
    position_size = round(Trademanager().position_size_calculator(stop_loss=pipvalue*1.5))
    unit = position_size * last_candle['Close'] if pair != "EUR_USD" else position_size
    SL = last_candle['SL']
    TP = last_candle['TP']
    return unit,SL,TP,side



    
        
        
if __name__ == "__main__":
    last_candle = last_candle_function(instrument='EUR_USD', granularity='D')
    if last_candle is not None:
        running_trades_result = running_trades(last_candle, pair='EUR/USD')
        final_check(pair='EUR/USD', running_trades=running_trades_result)
