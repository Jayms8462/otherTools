from pymongo import MongoClient
import urllib.parse
import threading
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

# Connect to MongoDB
uri = f'mongodb://{encoded_username}:{encoded_password}@{host}:{port}/{db_name}?authSource={auth_db}'
client = MongoClient(uri)
db = client[db_name]

def getSetCollection():
    return db['Sets']

def getCardCollection(entry_type):
    return db[entry_type]

def process_entry(entry):
    originalUrl = entry.get('Url')
    setCount = entry.get('Total Cards')
    setType = entry.get('Type')

    setCollection = getCardCollection(setType)
    setCollCount = setCollection.count_documents({'original_url': originalUrl})

    if setCount == setCollCount:
        collection.update_one({'_id': entry['_id']}, {'$set': {'cardCountVerified': True}})
    else:
        collection.update_one({'_id': entry['_id']}, {'$set': {'cardCountVerified': "Fail"}})

def worker():
    while True:
        entry = None
        with lock:
            if not entries:
                break
            entry = entries.pop()

        if entry:
            process_entry(entry)

def main():
    global entries
    global collection
    global lock

    collection = getSetCollection()
    lock = threading.Lock()

    while collection.count_documents({'cardCountVerified': False}) > 0: # 'Total Cards': { '$gte': 17 }
        start_time = time.time()

        pipeline = [
            {'$match': {'cardCountVerified': False}}, # 'Total Cards': { '$gte': 17 }
            {'$sample': {'size': 12}}  # Adjust sample size as needed
        ]
        entries = list(collection.aggregate(pipeline))

        num_threads = min(12, len(entries))  # Adjust number of threads as needed
        threads = []

        for _ in range(num_threads):
            thread = threading.Thread(target=worker)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Run Time: {execution_time:.2f} seconds, Remaining: {collection.count_documents({'cardCountVerified': False})}") # 'Total Cards': { '$gte': 17 }

if __name__ == "__main__":
    main()
