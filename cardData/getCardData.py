import urllib.parse
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import re
import time

# MongoDB connection details
username = <username>
password = <password>
host = <Host>
port = <Port>
auth_db = <authdb>
db_name = <dbname>

# URL-encode the username and password
encoded_username = urllib.parse.quote_plus(username)
encoded_password = urllib.parse.quote_plus(password)

# MongoDB URI
MONGO_URI = f"mongodb://{encoded_username}:{encoded_password}@{host}:{port}/{auth_db}"

# Create a MongoClient to the running mongod instance
client = MongoClient(MONGO_URI)

# Specify the database to work with
db = client[db_name]

# Print a success message
print("Connected to the database successfully!")

# Specify the sets collection to work with
sets_collection = db['Sets']

# Initialize Selenium WebDriver for Firefox
options = Options()
options.headless = True  # Run in headless mode to avoid opening browser windows
driver = webdriver.Firefox(options=options)

def process_url():
    while True:
        # Retrieve one random URL and type from the sets collection where setComplete is false and Total Cards is not 0
        set_info = sets_collection.aggregate([
            {"$match": {"setComplete": False, "Total Cards": {"$lte": 10}}},
            {"$sample": {"size": 1}}
        ])
        
        info = next(set_info, None)
        if info is None:
            print("No more incomplete sets available.")
            break

        original_url = info['Url']
        set_type = info['Type']
        modified_url = original_url.replace('ViewSet.cfm', 'Checklist.cfm')

        # Open the URL and extract photo links
        print(f"Opening URL: {modified_url}")
        driver.get(modified_url)

        # Define the XPath to the table body and pagination element
        xpath_to_table = "/html/body/div[1]/div[3]/div[2]/div[1]/table[2]/tbody"
        xpath_to_pagination = "/html/body/div[1]/div[3]/div[2]/div[1]/nav/ul"

        # Store the extracted data for later use
        cards_data = []

        def extract_data_from_page():
            try:
                table_body = driver.find_element(By.XPATH, xpath_to_table)
                rows = table_body.find_elements(By.TAG_NAME, "tr")

                for row in rows:
                    tds = row.find_elements(By.TAG_NAME, "td")
                    row_data = [td.text for td in tds if td.text.strip()]  # Remove blank elements

                    # Extract data from the row
                    front_photo_link = tds[0].find_element(By.TAG_NAME, "img").get_attribute("src")

                    if front_photo_link == "https://www.tcdb.com/Images/AddCard.gif":
                        front_photo_link = None
                        back_photo_link = None
                    else:
                        front_photo_link = row.find_element(By.LINK_TEXT, row_data[0]).get_attribute("href")
                        back_photo_link = front_photo_link

                    if len(row_data) >= 3:
                        card_number = row_data[0]
                        card_name = row_data[1]  # Extract only the name part before any additional text like SN99
                        team = row_data[2]
                    else:
                        card_number = row_data[0]
                        card_name = row_data[1]  # Extract only the name part before any additional text like SN99
                        team = None

                    # Print the extracted data
                    # print(f"Front Photo: {front_photo_link}, Back Photo: {back_photo_link}, Card Number: {card_number}, Card Name: {card_name}, Team: {team}")

                    # Store the data
                    cards_data.append({
                        "front_photo": front_photo_link,
                        "back_photo": back_photo_link,
                        "card_number": card_number,
                        "card_name": card_name,
                        "team": team,
                        "set_type": set_type,
                        "original_url": original_url
                    })

            except Exception as e:
                print(f"Error processing data on the current page: {e}")

        current_page = 1

        while True:
            extract_data_from_page()
            try:
                pagination = driver.find_element(By.XPATH, xpath_to_pagination)
                next_button = pagination.find_elements(By.TAG_NAME, "li")[-1]
                if "disabled" in next_button.get_attribute("class") or "Next" not in next_button.text:
                    break
                next_button.find_element(By.TAG_NAME, "a").click()
                current_page += 1
                # print(f"Navigating to page {current_page}")
                time.sleep(2)  # Wait for the next page to load
            except Exception as e:
                # print(f"Error navigating to the next page: {e}")
                break

        # Update the database with the extracted data
        for card in cards_data:
            set_type = card['set_type']
            original_url = card['original_url']
            card_number = card['card_number']
            card_name = card['card_name']
            front_photo_link = card['front_photo']
            back_photo_link = card['back_photo']
            team = card['team']

            # Connect to the appropriate collection based on set_type
            collection = db[set_type]

            # Search for the record with original_url, card number, and a regex match for card name
            record = collection.find_one({
                "original_url": original_url,
                "card_number": card_number,
                "card_name": {"$regex": re.escape(card_name), "$options": "i"}
            })

            # Update the record with new photo links and add player team, or log to errorCards if not found
            if record:
                collection.update_one(
                    {"_id": record['_id']},
                    {"$set": {
                        "photoFront": front_photo_link,
                        "photoBack": back_photo_link,
                        "playerTeam": team
                    }}
                )
                # print(f"Updated record for Card Number: {card_number}, Card Name: {card_name}")
            else:
                # Insert the record into the errorCards collection
                error_collection = db['errorCards']
                error_collection.insert_one(card)
                # print(f"No record found for Card Number: {card_number}, Card Name: {card_name}. Added to errorCards collection.")

        # Mark the set as complete in the Sets collection
        sets_collection.update_one(
            {"_id": info['_id']},
            {"$set": {"setComplete": True}}
        )
        print(f"Marked set as complete for URL: {modified_url}")

# Process the URLs sequentially
process_url()

# Close the WebDriver
driver.quit()

# Print a completion message
print("Database update complete.")
