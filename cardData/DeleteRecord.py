from pymongo import MongoClient
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

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
uri = f'mongodb://{encoded_username}:{encoded_password}@{host}:{port}/{db_name}?authSource={auth_db}'
client = MongoClient(uri)
db = client[db_name]

def clean_failed_records(set_record):
    try:
        set_id = set_record['_id']
        entry_type = set_record['Type']
        original_url = set_record['Url']

        # Get the corresponding collection based on type
        card_collection = db[entry_type]

        # Remove records where original_url matches Url
        result = card_collection.delete_many({'original_url': original_url})
        print(f"Deleted {result.deleted_count} records from {entry_type} where original_url = {original_url}")

        # Update cardCountVerified to "Cleaned" in Sets collection
        db['Sets'].update_one(
            {'_id': set_id},
            {'$set': {'cardCountVerified': 'Cleaned'}}
        )
        print(f"Updated cardCountVerified to 'Cleaned' for set {set_id}")
    except Exception as e:
        print(f"Error processing set {set_id}: {str(e)}")

def main(num_threads):
    sets_collection = db['Sets']

    # Find all sets where cardCountVerified is "Fail"
    failed_sets = sets_collection.find({'cardCountVerified': 'Fail'})

    # Process sets in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(clean_failed_records, failed_sets)

    client.close()  # Close MongoDB connection

if __name__ == "__main__":
    num_threads = 12  # Set the number of threads here
    main(num_threads)
