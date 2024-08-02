from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import os
import time
import requests as req
import re


def nepse_ticker_fetcher():
    stocks = []
    url = 'https://www.sharesansar.com/today-share-price'

    response = req.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Corrected BeautifulSoup usage
    target_div = soup.find('div', class_='headFixedWrapper')
    table = target_div.find('table', {'id': 'headFixed'}) if target_div else None
    stocks_name = table.find_all('a') if table else []
    for stock in stocks_name:
        stocks.append(stock.text.strip())
    return stocks

'''
def format_df(df, current_date):
    df.insert(0, "Date", current_date.strftime("%Y-%m-%d"))
    return df
'''
def sanitize_filename(filename):

    # Replace invalid characters with underscores
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def fetch_nepse_data(tickers_list =None):

    tickers_list =tickers_list

    # Initialize the WebDriver
    driver = webdriver.Chrome()
    directory_path = r'C:\Users\sachi\OneDrive\Documents\BOTS\nnfx_bot\nepse\nepse_pickles'

    # Define current date
    current_date = datetime.now()

    try:
        for ticker in tickers_list:
            df_list = []
            page_number = 1

            # Navigate to the target URL
            url = f'https://www.sharesansar.com/company/{ticker}'
            print(f"Data Extraction Started for {ticker}")
            driver.get(url)

            try:
                # Wait until the "Price History" link is present and click it
                price_history_link = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "btn_cpricehistory"))
                )
                price_history_link.click()

                while page_number <= 135:
                    try:
                        # Wait for the pagination button to be clickable
                        pagination_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, f"//a[@aria-controls='myTableCPriceHistory'][text()='{page_number}']"))
                        )
                        pagination_button.click()

                        # Wait for the content to load
                        time.sleep(2)

                        # Parse the page content with BeautifulSoup
                        page_source = driver.page_source
                        soup = BeautifulSoup(page_source, 'html.parser')

                        # Find the table again
                        target_div = soup.find('div', class_="table-responsive cpricehistory-section")
                        table = target_div.find('table', {'id': 'myTableCPriceHistory'}) if target_div else None

                        if table:
                            # Extract table headers
                            headers = [th.text.strip() for th in table.find('thead').find_all('th')]

                            # Extract table rows
                            rows = []
                            for tr in table.find('tbody').find_all('tr'):
                                cells = tr.find_all('td')
                                if len(cells) == len(headers):  # Ensure row has the correct number of columns
                                    row = [cell.text.strip() for cell in cells]
                                    rows.append(row)

                            # Create a DataFrame if rows are found
                            if rows:
                                df = pd.DataFrame(rows, columns=headers)
                                df_list.append(df)
                                print(f"Data extracted from page {page_number}")
                            else:
                                print(f"No data found on page {page_number}")

                        # Move to the next page
                        page_number += 1

                    except Exception as e:
                        print(f"Failed to process page {page_number}: {e}")
                        break

            except Exception as e:
                print(f"Failed to process ticker {ticker}: {e}")

            # If needed, combine all DataFrames into one
            if df_list:
                combined_df = pd.concat(df_list, ignore_index=True)
                if not os.path.exists(directory_path):
                    os.makedirs(directory_path)
                symbol = sanitize_filename(ticker)
                combined_file_name = os.path.join(directory_path, f"{symbol}_{current_date.strftime('%Y-%m-%d')}.pkl")
                combined_df.to_pickle(combined_file_name)
                print(f"Combined data saved to {combined_file_name}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the browser
        driver.quit()
        print("Scraping completed")


if __name__ == "__main__":
    file_path = r"nepse/nepse_ticker_data.txt"
    stocks_list = []

    # Open and read the file
    with open(file_path, 'r') as file:
        # Read the contents and split by newlines
        stocks_list = file.read().splitlines()

    # Print the list of stock symbols
    print(stocks_list)
    fetch_nepse_data(tickers_list=stocks_list)