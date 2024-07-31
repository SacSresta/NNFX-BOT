from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
import os
import time

def selenium_web(days=10):
    driver = webdriver.Chrome()
    current_date = datetime.now()

    # Define the number of days to go back
    days_to_scrape = days
    df_list = []
    try:
        for _ in range(days_to_scrape):
            try:
                # Open the website
                driver.get("https://www.sharesansar.com/today-share-price")

                # Wait for the date picker to be present
                date_picker = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "fromdate"))
                )

                # Clear any existing value in the input field and input the desired date
                date_picker.clear()
                date_picker.send_keys(current_date.strftime("%Y-%m-%d"))
                date_picker.send_keys(Keys.RETURN)

                # Wait until the search button is clickable
                search_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "btn_todayshareprice_submit"))
                )

                # Click the search button
                search_button.click()

                # Wait for the table to be present in the DOM
                table_element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'headFixedWrapper'))
                )

                # Introduce an additional wait to ensure data is fully loaded
                time.sleep(2)  # Adjust sleep time as needed

                # Get the page source and parse it with BeautifulSoup
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Locate the target div and table
                target_div = soup.find('div', class_='headFixedWrapper')
                table = target_div.find('table', {'id': 'headFixed'}) if target_div else None

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
                        format_df(df, current_date)

                        # Ensure the directory exists
                        directory_path = r'C:\Users\sachi\OneDrive\Documents\BOTS\nnfx_bot\nepse\datas'
                        if not os.path.exists(directory_path):
                            os.makedirs(directory_path)
                            print(f"Directory {directory_path} created")

                        # Save the DataFrame to a CSV file
                        file_name = os.path.join(directory_path, f"data_{current_date.strftime('%Y-%m-%d')}.csv")
                        df.to_csv(file_name, index=False)
                        df_list.append(df)
                        print(f"Data extracted and saved to {file_name}")
                    else:
                        print(f"Market closed on {current_date.strftime('%Y/%m/%d')}")

                # Move to the previous day
                current_date -= timedelta(days=1)

            except Exception as e:
                print(e)

    finally:
        # Close the browser
        driver.quit()
        print("Scraping completed")
        return df_list


def format_df(df, current_date):
    df.insert(0, "Date", current_date.strftime("%Y-%m-%d"))
    return df

if __name__ == "__main__":
    selenium_web(days=15)