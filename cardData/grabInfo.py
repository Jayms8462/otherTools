from pymongo import MongoClient
import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from deepdiff import DeepDiff
import csv
import argparse
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path='./login.env')

parser = argparse.ArgumentParser(description='A Script to grab into from tcdb.com and collect the card data. \
                                 Adding this data to the respective DB and killing the process. \
                                 This script is designed to operate on independant systems to distribute the workload between them. \
                                 -U or --url ***Required***, Sets Url e.x. https://www.tcdb.com/ViewSet.cfm/sid/132133/1990-Green-Bay-Packers-Police \
                                 -D or --db ***Required***, database name e.x. cards \
                                 -H or --host ***Required***, host to run the script \
                                 -u or --user ***Required***, username for the db \
                                 -p or --pass ***Required***, password for database \
                                 ')
parser.add_argument('-U', '--url', type=str, required=True, help="Sets Url e.x. https://www.tcdb.com/ViewSet.cfm/sid/132133/1990-Green-Bay-Packers-Police")
parser.add_argument('-D', '--db', type=str, required=True, help="database name e.x. cards")
parser.add_argument('-H', '--host', type=str, required=True, help="host to run the script")
parser.add_argument('-u', '--user', type=str, required=True, help="username for the db")
parser.add_argument('-p', '--password', type=str, required=True, help="password for database")
args = parser.parse_args()

# os.system('cls' if os.name == 'nt' else 'clear')
if os.name == 'nt':
    options = Options()
    options.binary_location = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
    options.add_argument("detach=True")
    options.headless= True
    driver = webdriver.Firefox(executable_path=r'C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\geckodriver.exe', options=options)

dbString = "mongodb://" + args.user + args.password + "@127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1&authSource=admin"

# print(args.url)
# print(args.db)
# print(args.host)
# print(args.user)
# print(args.password)

print(os.getenv('user'))


# options = Options()
# options.binary_location = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
# options.add_argument("detach=True")
# options.headless= True
# driver = webdriver.Firefox(executable_path=r'C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\geckodriver.exe', options=options)

# def get_database():

#    CONNECTION_STRING = "mongodb://jportune:<password>@127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1&authSource=admin"
 
#    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
#    client = MongoClient(CONNECTION_STRING)
 
#    # Create the database for our example (we will use the same database throughout the tutorial
#    return client['cardDB']

# def errorItems(i):
#     print("Error on:", i)
#     with open("errorUrl.txt", 'a', encoding="utf-8") as f:
#         f.write(i + '\n')
#     f.close()

# # This is added so that many files can reuse the function get_database()
# if __name__ == "__main__":   
#     # Get the database
#     dbname = get_database()
    


#     ### Creates objects and stores it in titlesList for later manipulation
#     with open('urls.txt') as data:
        
#         idx = 0
#         for i in data:
#             ### Grabbing Card Data Section
#             try:
#                 url = i.replace("ViewSet.cfm", "Checklist.cfm")
#                 driver.get(url)
#                 errorNum = 0
#                 while driver.current_url == 'https://www.tcdb.com/DefaultError.html':
#                     errorNum += 1
#                     print("Error, Trying Again: " + url)
#                     time.sleep(30)
#                     if errorNum <= 3:
#                         driver.get(url)
#                     else:
#                         with open("errorUrl.txt", 'a', encoding="utf-8") as f:
#                             f.write(i)
#                         f.close()
#                         continue

#                 try:
#                     ### Multi Page Sets
#                     lastPage = driver.find_element(By.CLASS_NAME, "pagination.justify-content-center.flex-wrap").find_element(By.LINK_TEXT, "»").get_attribute("href")
#                     nextLink = driver.find_element(By.CLASS_NAME, "pagination.justify-content-center.flex-wrap").find_element(By.LINK_TEXT, "›")
#                     listLen = lastPage.replace(url.replace('\n', '') + "?PageIndex=", '')
#                     listLen = int(listLen)
#                     collection_name = dbname['cards']
#                     while listLen >= 1:
#                         cardSet = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/p[1]/strong").text
#                         setYear = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/div/nav/ol/li[4]/a").text
#                         setType = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/div/nav/ol/li[2]/a").text
#                         tableEle = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/table[2]/tbody").find_elements(By.TAG_NAME, "tr")
#                         for j in tableEle:
#                             cardUrlData = []
#                             tableData = j.text.replace('\n', '\t').replace('   ', '\t').replace('  ', '').split('\t')
#                             for k in j.find_elements(By.TAG_NAME, "a"):
#                                 if k.get_attribute("href") != None:
#                                     if "ViewCard.cfm" in k.get_attribute("href"):
#                                         if k.get_attribute("href") not in cardUrlData:
#                                             cardUrlData.append(k.get_attribute("href"))
#                             if len(tableData) > 3:
#                                     cardNum = tableData[0]
#                                     playerName = tableData[1]
#                                     playerTeam = tableData[3]
#                                     playerExtra = tableData[2]
#                                     unfilteredData = j.text.replace('\n', ' ')
#                                     cardUrl = cardUrlData[0]
#                             elif len(tableData) == 2:
#                                     cardNum = tableData[0]
#                                     playerName = tableData[1]
#                                     playerTeam = ""
#                                     playerExtra = ""
#                                     unfilteredData = j.text.replace('\n', ' ')
#                                     cardUrl = cardUrlData[0]
#                             else:
#                                     cardNum = tableData[0]
#                                     playerName = tableData[1]
#                                     playerTeam = tableData[2]
#                                     playerExtra = ""
#                                     unfilteredData = j.text.replace('\n', ' ')
#                                     cardUrl = cardUrlData[0]
#                             itemImport = {
#                                 "cardNum": cardNum,
#                                 "playerName": playerName,
#                                 "playerTeam": playerTeam,
#                                 "playerExtra": playerExtra,
#                                 "unfilteredData": unfilteredData,
#                                 "cardUrl": cardUrl,
#                                 "cardSet": cardSet,
#                                 "setYear": setYear,
#                                 "setType": setType,
#                                 "setUrl": i.replace('\n', '')
#                             }

#                             ### Add data to DB
#                             record = collection_name.find({"cardUrl": itemImport["cardUrl"]})
#                             recCount = collection_name.count_documents({"cardUrl": itemImport["cardUrl"]})

#                             match recCount:
#                                 case _ if recCount == 0:
#                                     collection_name.insert_one(itemImport)
#                                 case _ if recCount == 1:
#                                     record = collection_name.find_one({"cardUrl": itemImport["cardUrl"]})
#                                     objDiff = DeepDiff(record, itemImport, exclude_paths="root['_id']")
#                                     if objDiff != {}:
#                                         filter = { '_id': record["_id"] }
#                                         newvalues = { "$set": {
#                                             "cardNum": itemImport["cardNum"],
#                                             "playerName": itemImport["playerName"],
#                                             "playerTeam": itemImport["playerTeam"],
#                                             "playerExtra": itemImport["playerExtra"],
#                                             "unfilteredData": itemImport["unfilteredData"],
#                                             "cardUrl": itemImport["cardUrl"],
#                                             "cardSet": itemImport["cardSet"],
#                                             "setYear": itemImport["setYear"],
#                                             "setType": itemImport["setType"],
#                                             "setUrl": itemImport["setUrl"]
#                                             }
#                                         }
#                                         collection_name.update_one(filter, newvalues)
#                                 case _ if recCount > 1:
#                                     for j in record:
#                                         collection_name.delete_one({
#                                             "cardUrl": itemImport["cardUrl"]
#                                             }
#                                         )
#                                     collection_name.insert_one(itemImport)
#                         nextLink.click()
#                         if listLen != 2:
#                             nextLink = driver.find_element(By.CLASS_NAME, "pagination.justify-content-center.flex-wrap").find_element(By.LINK_TEXT, "›")
#                         listLen -= 1
#                 except:
#                     ### Single Page Sets
#                     collection_name = dbname['cards']
#                     try:
#                         cardSet = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/p[1]/strong").text
#                     except:
#                         try:
#                             cardSet = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/h4").text
#                         except:
#                             try:
#                                 cardSet = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/p[1]/strong").text
#                             except:
#                                 try:
#                                     cardSet = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/h1").text
#                                 except:
#                                     try:
#                                         cardSet = driver.find_element(By.XPATH, "/html/body/div/div[3]/div[2]/div[1]/h1").text
#                                     except:
#                                         cardSet = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/p[1]/strong").text
                                    
#                     setYear = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/div/nav/ol/li[4]/a").text
#                     setType = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/div/nav/ol/li[2]/a").text
#                     tableEle = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/table[2]/tbody").find_elements(By.TAG_NAME, "tr")
#                     for j in tableEle:
#                         cardUrlData = []
#                         tableData = j.text.replace('\n', '\t').replace('   ', '\t').replace('  ', '').split('\t')
#                         for k in j.find_elements(By.TAG_NAME, "a"):
#                             if k.get_attribute("href") != None:
#                                 if "ViewCard.cfm" in k.get_attribute("href"):
#                                     if k.get_attribute("href") not in cardUrlData:
#                                         cardUrlData.append(k.get_attribute("href"))
#                         if len(tableData) > 3:
#                                 cardNum = tableData[0]
#                                 playerName = tableData[1]
#                                 playerTeam = tableData[3]
#                                 playerExtra = tableData[2]
#                                 unfilteredData = j.text.replace('\n', ' ')
#                                 cardUrl = cardUrlData[0]
#                         elif len(tableData) == 2:
#                                 cardNum = tableData[0]
#                                 playerName = tableData[1]
#                                 playerTeam = ""
#                                 playerExtra = ""
#                                 unfilteredData = j.text.replace('\n', ' ')
#                                 cardUrl = cardUrlData[0]
#                         else:
#                                 cardNum = tableData[0]
#                                 playerName = tableData[1]
#                                 playerTeam = tableData[2]
#                                 playerExtra = ""
#                                 unfilteredData = j.text.replace('\n', ' ')
#                                 cardUrl = cardUrlData[0]
#                         itemImport = {
#                             "cardNum": cardNum,
#                             "playerName": playerName,
#                             "playerTeam": playerTeam,
#                             "playerExtra": playerExtra,
#                             "unfilteredData": unfilteredData,
#                             "cardUrl": cardUrl,
#                             "cardSet": cardSet,
#                             "setYear": setYear,
#                             "setType": setType,
#                             "setUrl": i.replace('\n', '')
#                         }

#                         record = collection_name.find({"cardUrl": itemImport["cardUrl"]})
#                         recCount = collection_name.count_documents({"cardUrl": itemImport["cardUrl"]})

#                         match recCount:
#                             case _ if recCount == 0:
#                                 collection_name.insert_one(itemImport)
#                             case _ if recCount == 1:
#                                 record = collection_name.find_one({"cardUrl": itemImport["cardUrl"]})
#                                 objDiff = DeepDiff(record, itemImport, exclude_paths="root['_id']")
#                                 if objDiff != {}:
#                                     print("Updating record:", cardUrl)
#                                     filter = { '_id': record["_id"] }
#                                     newvalues = { "$set": {
#                                         "cardNum": cardNum,
#                                         "playerName": playerName,
#                                         "playerTeam": playerTeam,
#                                         "playerExtra": playerExtra,
#                                         "unfilteredData": unfilteredData,
#                                         "cardUrl": cardUrl,
#                                         "cardSet": cardSet,
#                                         "setYear": setYear,
#                                         "setType": setType,
#                                         "setUrl": i.replace('\n', '')
#                                         }
#                                     }
#                                     collection_name.update_one(filter, newvalues)
#                             case _ if recCount > 1:
#                                 for j in record:
#                                     collection_name.delete_one({
#                                         "cardUrl": itemImport["cardUrl"]
#                                         }
#                                     )
#                                 collection_name.insert_one(itemImport)

#                     idx += 1
#                     print(idx, "Complete:", i.replace("\n", ""))
#             except:
#                 i = i.replace('\n', '')
#                 errorItems(i)