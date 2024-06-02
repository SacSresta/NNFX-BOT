from Trademanager import Trademanager
from data import ForexData

def main():
    while True:
        instrument = ["EUR_USD","GBP_USD"]
        for pair in instrument:
            running_pair = Trademanager().pair_run_check(pair)
            if running_pair is Not None:
                ForexData().close_trade(running_pair)
                ForexData().create_order(pair)
            else:
                ForexData().create_order(pair)
                





