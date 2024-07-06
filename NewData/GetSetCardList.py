from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from pymongo import MongoClient
import re

def getSetCollection():
    # Connect to the MongoDB client
    client = MongoClient('mongodb://localhost:27017/')
    db = client['carddb']
    collection = db['Sets']
    return collection

def getCardCollection(entry_type):
    # Connect to the MongoDB client
    client = MongoClient('mongodb://localhost:27017/')
    db = client['carddb']
    collection = db[entry_type]
    return collection

def defineDriver():
    firefox_options = Options()
    firefox_options.headless = True
    driver = webdriver.Firefox(options=firefox_options)
    return driver

def getData(driver, url, collection, entry_id, entry_type):
    driver.get(url)

     # Find all checkbox elements
    checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
    
    # Extract the text following each checkbox
    data = []
    for checkbox in checkboxes:
        text = checkbox.find_element(By.XPATH, './following-sibling::font').text
        data.append(text)

    # Get the length of data
    total_cards = len(data)
    
    # Update the collection entry with total_cards and cardList
    collection.update_one(
        {'_id': entry_id},
        {'$set': {'Total Cards': total_cards}}
    )

    #Redefine collection to put card list in the correct collection
    collection = getCardCollection(entry_type)

    for item in data:
        # Split by whitespace
        parts = item.split(maxsplit=1)
        if len(parts) >= 2:
            card_number = parts[0]  # First part is the card number
            card_name = parts[1]    # Rest is the card name

            card_doc = {
                'card_number': card_number,
                'card_name': card_name,
                'original_url': original_url,
                'photoFront': "",
                'photoBack': "",
                'cardType': entry_type,
                'setId': entry_id,
                'hasErrorOrVar': False
            }
            collection.insert_one(card_doc)
        else:
            print(f"Failed to parse item: {item}")


# Entrypoint
# Find an entry where cardListComplete is false
collection = getSetCollection()
count = collection.count_documents({'cardListComplete': False}) - 1
driver = defineDriver()

while count >= 0:
    collection = getSetCollection()
    entry = collection.find_one({'cardListComplete': False})
    if entry:
        original_url = entry.get('Url')

        # Use regular expression to extract the /sid/<number>/ part of the URL
        match = re.search(r'/sid/(\d+)/', original_url)
        if match:
            sid_number = match.group(1)
            checklistUrl = "https://www.tcdb.com/PrintChecklist.cfm/sid/" + sid_number
            getData(driver = driver, url = checklistUrl, collection = collection, entry_id=entry['_id'], entry_type=entry['Type'])

            # to Update once card list is input into db
            collection.update_one({'_id': entry['_id']}, {'$set': {'cardListComplete': True}})

        else:
            print("SID number not found in the URL.")
    else:
        print("No entry found with cardListComplete: false")

    count = count - 1
    print("Remaining:", count , "Url Complete:", original_url)
