import os
import pandas as pd
import re
from nepse.data_fetcher import selenium_web
def process_csv_files(input_folder=r'C:\Users\sachi\OneDrive\Documents\BOTS\nnfx_bot\nepse\data',
                      output_folder=r'C:\Users\sachi\OneDrive\Documents\BOTS\nnfx_bot\nepse\data_check'):
    # List all files in the input folder
    files = os.listdir(input_folder)

    # Filter the list to include only CSV files
    csv_files = [file for file in files if file.endswith('.csv')]

    # Dictionary to store DataFrames for each symbol
    symbol_dataframes = {}

    # Function to sanitize file names
    def sanitize_filename(filename):
        # Replace invalid characters with underscores
        return re.sub(r'[<>:"/\\|?*]', '_', filename)

    # Iterate over the list of CSV files and read each one into a DataFrame
    for csv_file in csv_files:
        file_path = os.path.join(input_folder, csv_file)
        try:
            df = pd.read_csv(file_path)
            if 'Symbol' not in df.columns:
                print(f"Warning: 'Symbol' column not found in {csv_file}. Skipping this file.")
                continue
            
            # Iterate over unique symbols in the current DataFrame
            for symbol in df['Symbol'].unique():
                symbol_df = df[df['Symbol'] == symbol]
                
                # If the symbol is already in the dictionary, append the new data
                if symbol in symbol_dataframes:
                    symbol_dataframes[symbol] = pd.concat([symbol_dataframes[symbol], symbol_df])
                else:
                    symbol_dataframes[symbol] = symbol_df
        except Exception as e:
            print(f"Error processing file {csv_file}: {e}")

    # Ensure the directory for saving symbol DataFrames exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save each symbol DataFrame to a separate CSV file
    for symbol, df in symbol_dataframes.items():
        # Sanitize the symbol to create a valid file name
        safe_symbol = sanitize_filename(symbol)
        output_path = os.path.join(output_folder, f"{safe_symbol}_data.csv")
        try:
            df['Open'] = df['Open'].str.replace(',', '').astype(float)
            df['High'] = df['High'].str.replace(',', '').astype(float)
            df['Low'] = df['Low'].str.replace(',', '').astype(float)
            df['Close'] = df['Close'].str.replace(',', '').astype(float)
            df.to_csv(output_path, index=False)
            print(f"Data for symbol {symbol} saved to {output_path}")
        except Exception as e:
            print(f"Error saving file for symbol {symbol}: {e}")


if __name__ == "__main__":
    df = selenium_web(days=5)
    print(df)
    process_csv_files()

