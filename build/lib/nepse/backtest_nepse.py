from yfinance_check.series import backtest

directory = r"C:\Users\sachi\OneDrive\Documents\BOTS\nnfx_bot\nepse\data_check"
output_directory =r"C:\Users\sachi\OneDrive\Documents\BOTS\nnfx_bot\nepse\datas_stats" 

backtest(directory=directory,output_directory=output_directory)