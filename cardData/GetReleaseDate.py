from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
import os
from pymongo import MongoClient

os.system('cls' if os.name == 'nt' else 'clear')
idx = 0
iteration_count = 0
max_iterations = 1000  # Number of iterations after which to restart the driver

link = [

]

def defineDriver():
    firefox_options = Options()
    firefox_options.headless = True
    driver = webdriver.Firefox(options=firefox_options)
    return driver

def getData(driver, url, collection):
    driver.get(url)
    if "ViewSet.cfm" in url or "Checklist.cfm" in url:
        try:
            total_cards_element = driver.find_element(By.XPATH, "//p[contains(., 'Total Cards:')]").text
            total_cards = total_cards_element.split(':')[1].strip()
        except:
            total_cards = "Unknown"

        try:
            release_date_element = driver.find_element(By.XPATH, "//li[contains(., 'Release Date:')]").text
            release_date = release_date_element.split(':')[1].strip()
        except:
            release_date = "Unknown"

        # Prepare data for MongoDB insertion
        data = {
            "Release Date": release_date,
            "Total Cards": total_cards,
            "Url": url,
            "Year": "",  # You need to fill these based on your requirements
            "Publisher": "",
            "Set": "",
            "Sub-Set": "",
            "Original String": "",
            "Type": "",
            "YearVerified": "",
            "PublisherVerified": ""
        }

        # Insert data into MongoDB
        collection.insert_one(data)
        print("Inserted data into MongoDB:", data)

def main():
    global idx, iteration_count

    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['carddb']
    collection = db['Sets']

    driver = defineDriver()

    for url in link:
        idx += 1
        iteration_count += 1
        try:
            getData(driver, url, collection)
        except TimeoutException:
            print("Timeout hit for Url:", url)
            driver.quit()
            driver = defineDriver()
            getData(driver, url, collection)
        except WebDriverException:
            print("WebDriver hit for Url:", url)
            driver.quit()
            driver = defineDriver()
            getData(driver, url, collection)

        if iteration_count >= max_iterations:
            driver.quit()
            driver = defineDriver()
            iteration_count = 0

    driver.quit()

if __name__ == "__main__":
    main()