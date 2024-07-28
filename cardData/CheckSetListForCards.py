#################################################################################################
#
# This script is used to get the number of cards in a set. This is accomplished by checking the 
# list page of the set and counting the cards. It then updates that number in the database. If 
# the list page has no cards then it will delete the entry in the database.
#
#################################################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from pymongo import MongoClient
import re
import urllib.parse

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

def defineDriver():
    firefox_options = Options()
    firefox_options.headless = True
    driver = webdriver.Firefox(options=firefox_options)
    return driver

# Connect to MongoDB
uri = f'mongodb://{encoded_username}:{encoded_password}@{host}:{port}/{db_name}?authSource={auth_db}'
client = MongoClient(uri)
db = client['carddb']
collection = db['Sets']

# Find documents that match the query
results = collection.find({"cardCountVerified": "Cleaned"})

print("\n", "\n")
deleteEntries = input("Are we deleting entries?:")
print("\n", "\n")

driver = defineDriver()

for result in results:
    original_url = result.get('Url')

    # Use regular expression to extract the /sid/<number>/ part of the URL
    match = re.search(r'/sid/(\d+)/', original_url)
    if match:
        sid_number = match.group(1)
        checklistUrl = "https://www.tcdb.com/PrintChecklist.cfm/sid/" + sid_number
        driver.get(checklistUrl)

        checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
        
        # Update Total Cards and handle deletion condition
        num_checkboxes = len(checkboxes)
        if num_checkboxes == 0 and deleteEntries == 'y':
            # Delete the document from MongoDB
            collection.delete_one({"_id": result['_id']})
            print(f"Deleted document with _id: {result['_id']}")
        else:
            #Update Total Cards field
            collection.update_one(
                {"_id": result['_id']},
                {"$set": {"Total Cards": num_checkboxes}}
            )
            print(f"Updated document with _id: {result['_id']} - Total Cards: {num_checkboxes}")
        
        # Close the driver to free up resources
        # driver.quit()

# Close MongoDB connection
# client.close()

