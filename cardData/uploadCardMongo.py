from pymongo import MongoClient
import os
from deepdiff import DeepDiff
import concurrent.futures

os.system('cls' if os.name == 'nt' else 'clear')

def get_database():

   CONNECTION_STRING = "mongodb://jportune:<password>@127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1&authSource=admin"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['cardDB']

def uploadData(data):
    collection_name = dbname['cards']
    i = data
    i = i.replace('\n', '')
    i = i.split('\t')

    cardNum = i[0]
    playerName = i[1]
    playerTeam = i[2]
    playerExtra = i[3]
    unfilteredData = i[4]
    cardUrl = i[5]
    cardSet = i[6]
    setYear = i[7]
    setType = i[8]
    setUrl = i[9]

    record = collection_name.find({"cardUrl": cardUrl})
    recCount = collection_name.count_documents({"cardUrl": cardUrl})
    itemImport = {
        "cardNum": cardNum,
        "playerName": playerName,
        "playerTeam": playerTeam,
        "playerExtra": playerExtra,
        "unfilteredData": unfilteredData,
        "cardUrl": cardUrl,
        "cardSet": cardSet,
        "setYear": setYear,
        "setType": setType,
        "setUrl": setUrl
    }

    match recCount:
        case _ if recCount == 0:
            print("Adding New Entry:", itemImport["cardUrl"])
            collection_name.insert_one(itemImport)
        case _ if recCount == 1:
            record = collection_name.find_one({"cardUrl": itemImport["cardUrl"]})
            objDiff = DeepDiff(record, itemImport, exclude_paths="root['_id']")
            if objDiff != {}:
                print("Updating record:", cardUrl)
                filter = { '_id': record["_id"] }
                newvalues = { "$set": {
                    "cardNum": cardNum,
                    "playerName": playerName,
                    "playerTeam": playerTeam,
                    "playerExtra": playerExtra,
                    "unfilteredData": unfilteredData,
                    "cardUrl": cardUrl,
                    "cardSet": cardSet,
                    "setYear": setYear,
                    "setType": setType,
                    "setUrl": setUrl
                    }
                }
                collection_name.update_one(filter, newvalues)
        case _ if recCount > 1:
            print("Found Multi Entries, deleting them and adding:", itemImport["cardUrl"])
            record = collection_name.find({"cardUrl": itemImport["cardUrl"]})
            for j in record:
                collection_name.delete_one({"cardUrl": itemImport["cardUrl"]})
            collection_name.insert_one(itemImport)

if __name__ == "__main__":   
    # Get the database
    dbname = get_database()

    collection_name = dbname['cards']
    with open('./Data/cards.txt', encoding="utf-8") as file:
        data = file.readlines()
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(uploadData, data)
