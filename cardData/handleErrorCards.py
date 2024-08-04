import urllib.parse
from pymongo import MongoClient
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

# Function to process a single document
def process_document(error_card):
    set_type = error_card.get('set_type')
    
    # Check if set_type is available in the error_card
    if set_type:
        target_collection = db[set_type]
        # Find the corresponding document in the target collection
        target_document = target_collection.find_one({
            'card_number': error_card['card_number'],
            'original_url': error_card['original_url']
        })
        
        if target_document:
            # Prepare updated fields
            updated_fields = {
                'photoFront': error_card.get('front_photo'),
                'photoBack': error_card.get('back_photo'),
                'playerTeam': error_card.get('team')
            }
            
            # Check if card_name lengths are different
            if len(target_document.get('card_name', '')) != len(error_card.get('card_name', '')):
                updated_fields['card_name'] = error_card.get('card_name')

            # Remove fields with None values
            updated_fields = {k: v for k, v in updated_fields.items() if v is not None}
            
            # Print the details of updated fields
            print(f"Updating document with _id: {error_card['_id']} with fields: {updated_fields}")
            
            # Update the document in the target collection
            target_collection.update_one(
                {'_id': target_document['_id']},
                {'$set': updated_fields}
            )
            
            # Delete the document from the errorCards collection
            db.errorCards.delete_one({'_id': error_card['_id']})
            print(f"Updated and deleted document with _id: {error_card['_id']}")
            return 1
        else:
            print(f"No matching document found in {set_type} collection for _id: {error_card['_id']}")
            return 0
    else:
        print(f"set_type not found in document with _id: {error_card['_id']}")
        return 0

# Function to update and delete documents concurrently
def update_and_delete_documents():
    # Get the errorCards collection
    error_cards_collection = db.errorCards
    
    # Find all documents in the errorCards collection
    error_cards = list(error_cards_collection.find())

    # Initialize counters
    total_documents = len(error_cards)
    updated_documents = 0

    # Use ThreadPoolExecutor for concurrent processing
    with ThreadPoolExecutor(max_workers=26) as executor:
        futures = [executor.submit(process_document, error_card) for error_card in error_cards]
        
        for future in as_completed(futures):
            updated_documents += future.result()
    
    print(f"Total documents processed: {total_documents}")
    print(f"Total documents updated and deleted: {updated_documents}")

# Run the function to update and delete documents
update_and_delete_documents()
