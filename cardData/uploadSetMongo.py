from pymongo import MongoClient
import os

os.system('cls' if os.name == 'nt' else 'clear')

def get_database():

   CONNECTION_STRING = "mongodb://jportune:<password>@127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1&authSource=admin"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['cardDB']

if __name__ == "__main__":   
    # Get the database
    dbname = get_database()

    collection_name = dbname['cardTitles']
    with open('./storage/titles.txt', encoding="utf-8") as data:
        idx = 0
        for i in data:
            i = i.replace('\n', '')
            i = i.split('\t')
            title = i[0]
            setCount = i[1]
            setYear = i[2]
            tcdbUrl = i[4]
            setType = i[5]

            recCount = collection_name.count_documents({"tcdbUrl": i[4]})
            itemImport = {
                "title": title, 
                "publisher": "", 
                "setName": "", 
                "subSet": "",
                "setCount": int(setCount), 
                "releaseDate": "", 
                "setYear": int(setYear), 
                "tcdbUrl": tcdbUrl,
                "priceguideUrl": "",
                "setType": setType
            }

            match recCount:
                case _ if recCount == 0:
                    print(idx, "Adding New Entry:", i[4])
                    collection_name.insert_one(itemImport)
                # case _ if recCount == 1:
                #     print(idx, "Found, No Changes Needed:", i[4])
                case _ if recCount > 1:
                    print(idx, "Found Multi Entries, deleting them and adding:", i[4])
                    record = collection_name.find({"tcdbUrl": itemImport["tcdbUrl"]})
                    for j in record:
                        collection_name.delete_one({"tcdbUrl": itemImport["tcdbUrl"]})
                    collection_name.insert_one(itemImport)
            idx += 1
