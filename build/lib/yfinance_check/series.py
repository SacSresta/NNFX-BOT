import os
import pandas as pd
from yfinance_check.ssl_backtest import backtesting

def backtest(directory, output_directory, plot=False, file_type="csv"):
    # List all files in the directory
    files = os.listdir(directory)
    
    stats_dict = {}

    if file_type == "pkl":
        # Filter out only .pkl files
        pkl_files = [file for file in files if file.endswith('.pkl')]

        for pkl_file in pkl_files:
            file_path = os.path.join(directory, pkl_file)
            
            # Load the DataFrame from the .pkl file
            df = pd.read_pickle(file_path)
            
            # Call the backtesting function
            stats = backtesting(data=df, plot=plot)
            
            # Store results in dictionary with filename as key
            stats_dict[pkl_file] = stats
            
    elif file_type == "csv":
        # Filter out only .csv files
        csv_files = [file for file in files if file.endswith('.csv')]

        for csv_file in csv_files:
            file_path = os.path.join(directory, csv_file)
            
            # Load the DataFrame from the .csv file
            df = pd.read_csv(file_path)
            
            # Call the backtesting function
            stats = backtesting(data=df, plot=plot)
            
            # Store results in dictionary with filename as key
            stats_dict[csv_file] = stats

    # Create the output directory if it does not exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Convert dictionary to DataFrame and save as CSV
    stats_df = pd.DataFrame.from_dict(stats_dict, orient='index')
    output_file_path = os.path.join(output_directory, 'stats_dict.csv')
    stats_df.to_csv(output_file_path)

    print(f"Results saved to '{output_file_path}'.")

if __name__ == "__main__":
    directory = r"C:\Users\sachi\OneDrive\Documents\BOTS\nnfx_bot\yfinance_check\stocks_datas"
    output_directory = r"C:\Users\sachi\OneDrive\Documents\BOTS\nnfx_bot\yfinance_check\output"
    backtest(directory=directory, output_directory=output_directory)
