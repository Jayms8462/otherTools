from pymongo import MongoClient
import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from deepdiff import DeepDiff
import pprint

os.system('cls' if os.name == 'nt' else 'clear')

options = Options()
options.binary_location = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
options.add_argument("detach=True")
options.headless= True
driver = webdriver.Firefox(executable_path=r'C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\geckodriver.exe', options=options)

def get_database():

   CONNECTION_STRING = "mongodb://jportune:<password>@127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1&authSource=admin"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['cardDB']

def errorUrl(i):
    print("ErrorUrl:", i)
    with open("errorUrl.txt", 'a', encoding="utf-8") as f:
        f.write(i)
    f.close()


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
    # Get the database
    dbname = get_database()
    
    ### Creates objects and stores it in titlesList for later manipulation
    collection_name = dbname['cardTitles']
    record = collection_name.find({"setUrl": { "$exists": "true"}})
    idx = 0

    for i in record:
        collection_name.delete_one({"setUrl": i["setUrl"]})
        

        idx += 1
        print(idx, "Complete:", i["setUrl"])


    