from pymongo import MongoClient
import pandas as pd

# Initialize MongoDB client
client = MongoClient('mongodb://localhost:27017/')
db = client['carddb']
collection = db['Sets']

# Load the data from the file into a DataFrame
file_path = './updateData.txt'
data = pd.read_csv(file_path, sep='\t')

# List to store rows not found in the database
not_found = []

# Iterate over the rows in the DataFrame
for index, row in data.iterrows():
    url = row['Url']
    update_fields = {k: v for k, v in row.items() if pd.notnull(v) and k != 'Url'}
    
    # Check if the document exists
    result = collection.find_one({'Url': url})
    if result:
        # Update the document if it exists
        if update_fields:
            collection.update_one({'Url': url}, {'$set': update_fields})
    else:
        # Add to not_found list if the document does not exist
        not_found.append(row)
    
    print("Complete", url)

# Write not found entries to a new file
if not_found:
    not_found_df = pd.DataFrame(not_found)
    not_found_df.to_csv('./not_found_entries.csv', index=False)

print("Database update completed. Not found entries have been saved to 'not_found_entries.csv'.")
