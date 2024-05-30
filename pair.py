
def run_check():

    current_trade_pairs = [
        "EUR_USD", "GBP_NZD", "AUD_CAD",
    ]
    signal_currency_pair = "GBP_USD"

    signal_currency = signal_currency_pair.split("_")

    for current_trade_pair in current_trade_pairs:
        current_trade_currency = current_trade_pair.split("_")
        if (current_trade_currency[0] == signal_currency[0]) or (current_trade_currency[1] == signal_currency[1]):
            print(current_trade_currency)

        elif (current_trade_currency[0] == signal_currency[1]) or (current_trade_currency[1] == signal_currency[0]):
            print(current_trade_currency)


run_check()