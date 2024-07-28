from pymongo import MongoClient
import urllib.parse
from tqdm import tqdm
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

# Connect to MongoDB
client = MongoClient(f'mongodb://{encoded_username}:{encoded_password}@{host}:{port}/{db_name}?authSource={auth_db}')
db = client[db_name]
collection = db['Baseball']

# Function to process a single URL and remove duplicates within that URL
def process_url(url):
    # Find all documents with the current 'original_url'
    documents = collection.find({'original_url': url})
    
    # Dictionary to track unique (card_number, card_name) combinations within the same 'original_url'
    unique_cards = {}

    # Convert documents cursor to list
    documents_list = list(documents)
    for doc in documents_list:
        key = (doc['card_number'], doc['card_name'])
        if key in unique_cards:
            # If duplicate found, delete the current document
            collection.delete_one({'_id': doc['_id']})
        else:
            # Add to the dictionary if unique
            unique_cards[key] = doc['_id']

# Function to remove duplicates within each set identified by 'original_url'
def remove_duplicates():
    # Retrieve all unique 'original_url' values
    unique_urls = collection.distinct('original_url')

    # Use ThreadPoolExecutor to process URLs in parallel
    with ThreadPoolExecutor(max_workers=14) as executor:
        futures = {executor.submit(process_url, url): url for url in unique_urls}
        
        # Initialize tqdm progress bar for the unique URLs
        for future in tqdm(as_completed(futures), total=len(unique_urls), desc='Processing URLs', unit='url'):
            url = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {url}: {e}")

# Call the function to remove duplicates
remove_duplicates()

print("Duplicates removed successfully.")
