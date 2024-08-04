import urllib.parse
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import re
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

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

def calculate_match_percentage(record_name, card_name):
    record_words = record_name.split()
    card_words = card_name.split()
    match_count = sum(1 for word in record_words if word in card_words)
    return (match_count / len(record_words)) * 100

# For debugging purposes
# def write_to_file(data, filename='cards_data.json'):
#     with open(filename, 'w') as file:
#         json.dump(data, file, indent=4)

def update_card(card, db):
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
        "card_number": card_number
    })

    # Check if the record exists and if card_name lengths and values match
    if record:
        match_percentage = calculate_match_percentage(record['card_name'], card_name)
        if len(card_name) == len(record['card_name']) and record['card_name'] == card_name:
            # Update the record with new photo links and add player team
            collection.update_one(
                {"_id": record['_id']},
                {"$set": {
                    "photoFront": front_photo_link,
                    "photoBack": back_photo_link,
                    "playerTeam": team
                }}
            )

            # For debugging
            # print(f"Updated: set_type={set_type}, card_name={card_name}, card_number={card_number}, original_url={original_url}")
        elif match_percentage > 70:
            # Update the record if match percentage is above 70%
            collection.update_one(
                {"_id": record['_id']},
                {"$set": {
                    "photoFront": front_photo_link,
                    "photoBack": back_photo_link,
                    "playerTeam": team,
                    "card_name": card_name
                }}
            )

            # For debugging
            # print(f"Updated: set_type={set_type}, card_name={card_name}, card_number={card_number}, original_url={original_url}")
        else:
            # Insert the record into the errorCards collection if lengths or values do not match
            error_collection = db['errorCards']
            error_collection.insert_one(card)
    else:
        # Insert the record into the errorCards collection if no record is found
        error_collection = db['errorCards']
        error_collection.insert_one(card)

def process_url():
    while True:
        # Retrieve one random URL and type from the sets collection where setComplete is false and Total Cards is not 0
        set_info = sets_collection.aggregate([
            {"$match": {"setComplete": False}},
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
                next_button = pagination.find_element(By.LINK_TEXT, '›')
                if 'disabled' in next_button.get_attribute('class'):
                    break
                next_button.click()
                current_page += 1
                time.sleep(2)  # Wait for the next page to load
            except Exception as e:
                break
        
        ## For Debugging Purposes
        # write_to_file(cards_data, f'cards_data_page_{current_page}.json')

        # If we encountered an error, skip the rest of the processing for this URL
        if not cards_data:
            continue

        # Use ThreadPoolExecutor to update the database concurrently
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(update_card, card, db) for card in cards_data]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error updating card: {e}")

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
