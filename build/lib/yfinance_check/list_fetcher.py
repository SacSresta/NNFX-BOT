import pandas as pd
import numpy as np
import yfinance as yf
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os

def save_file(directory, file_name, data_list):
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Define the file path
    file_path = os.path.join(directory, file_name)
    
    # Save the data to the file
    with open(file_path, 'w') as file:
        for item in data_list:
            file.write(f"{item}\n")

def fetch_data():
    # Set up the WebDriver
    driver = webdriver.Chrome()

    stocks_list = []
    query = 0
    for i in range(0, 10):
        # Navigate to the Yahoo Finance screener page
        url = f"https://finance.yahoo.com/most-active?count=25&offset={query}"
        driver.get(url)

        # Get the page source
        page_source = driver.page_source

        # Parse the page source using BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        elem = soup.find_all('a', class_="Fw(600) C($linkColor)", attrs={"data-test": "quoteLink"})

        for e in elem:
            stocks_list.append(e.text)

        query += 25

    # Close the WebDriver
    driver.quit()

    # Save the stocks_list to a text file
    save_file(directory='yfinance_check', file_name='stocks_list.txt', data_list=stocks_list)

    return stocks_list

# Fetch the data and save it
stocks_list = fetch_data()
print(stocks_list)
