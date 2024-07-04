import os 
import sys
import pandas as pd
import numpy as np
import logging

logging.basicConfig(filename='trade_log.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Configure logging for oandapyV20 library
logger = logging.getLogger('oandapyV20')
logger.setLevel(logging.CRITICAL)

def save_all_candle_data(candle_data_all):
    new_data_df = pd.DataFrame(candle_data_all)
    try:
        if os.path.exists('all_data/candle_data_all.csv'):
            existing_data_df = pd.read_csv('all_data/candle_data_all.csv')
            combined_data_df = pd.concat([existing_data_df, new_data_df], ignore_index=True)
        else:
            combined_data_df = new_data_df

        combined_data_df.to_csv('all_data/candle_data_all.csv', index=False)
        logging.info("Candle data saved to candle_data_all.csv.")
    except PermissionError as e:
        logging.error(f"Permission error saving candle data to CSV: {e}")
        alternative_filename = 'all_data/backup/candle_data_backup.csv'
        combined_data_df.to_csv(alternative_filename, index=False)
        logging.info(f"Backup candle data saved to {alternative_filename}.")

def save_candle_data(candle_data, pair, directory='data'):
    # Create the directory if it does not exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Construct the file path
    file_path = os.path.join(directory, f'{pair}.csv')
    backup_file_path = os.path.join(directory, f'{pair}_candle_data_backup.csv')

    new_data_df = pd.DataFrame(candle_data)
    try:
        if os.path.exists(file_path):
            existing_data_df = pd.read_csv(file_path)
            combined_data_df = pd.concat([existing_data_df, new_data_df], ignore_index=True)
        else:
            combined_data_df = new_data_df

        combined_data_df.to_csv(file_path, index=False)
        logging.info(f"Candle data saved to {file_path}.")
    except PermissionError as e:
        logging.error(f"Permission error saving candle data to CSV: {e}")
        combined_data_df.to_csv(backup_file_path, index=False)
        logging.info(f"Backup candle data saved to {backup_file_path}.")