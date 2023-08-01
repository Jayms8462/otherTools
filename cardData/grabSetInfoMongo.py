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
    record = collection_name.find({"setCount": 0})

    idx = 0

    for i in record:
        driver.get(i["tcdbUrl"])
        errorNum = 0
        urlCheck = driver.current_url
        urlCheckIf = False
        if 'https://www.tcdb.com/DefaultError.html' in urlCheck:
            urlCheckIf = True

        while urlCheckIf:
            errorNum += 1
            print("Error, Trying Again: ")
            time.sleep(10)
            if errorNum <= 3:
                driver.get(i["tcdbUrl"])
                if 'https://www.tcdb.com/DefaultError.html' not in urlCheck:
                    urlCheckIf = False
            else:
                errorUrl(i["tcdbUrl"])
                urlCheckIf = False
                continue

        ### Get Title
        try:
            title = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/h4").text
        except NoSuchElementException:
            try:
                title = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/p[1]/strong").text
            except:
                title = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/h4").text
            

        try:
            setCount = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/p[1]").text
            setCount = int(setCount.split('Total Cards: ')[1].replace(',', ''))
        except NoSuchElementException:
            try:
                setCount = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/p[2]").text
                setCount = int(setCount.split('Total Cards: ')[1].replace(',', ''))
            except:
                setCount = 0
        except IndexError:
            setCount = 0

        try:
            releaseDate = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/ul/li").text
            releaseDate = releaseDate.split('Release Date: ')[1]
        except NoSuchElementException:
            try:
                releaseDate = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/ul/li")
                releaseDate = releaseDate.split('Release Date: ')[1]
            except:
                releaseDate = ""

        try:
            setYear = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/nav/ol/li[4]/a").text
        except NoSuchElementException:
            try:
                setYear = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/div/nav/ol/li[4]/a").text
            except:
                setYear = ""
        
        try:
            tcdbUrl = i["tcdbUrl"]
        except NoSuchElementException:
            tcdbUrl = ""

        try:
            setType = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/nav/ol/li[2]/a").text
        except NoSuchElementException:
            try:
                setType = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/div/nav/ol/li[2]/a").text
            except:
                setType = ""

        publisher = ""
        setName = ""
        subSet = ""
        priceguideUrl = ""

        itemImport = {
            "title": title, 
            "publisher": publisher, 
            "setName": setName, 
            "subSet": subSet,
            "setCount": setCount, 
            "releaseDate": releaseDate, 
            "setYear": setYear, 
            "tcdbUrl": tcdbUrl,
            "priceguideUrl": priceguideUrl,
            "setType": setType
        }
        
        record = collection_name.find({"tcdbUrl": tcdbUrl})
        recCount = collection_name.count_documents({"tcdbUrl": tcdbUrl})
        
        match recCount:
            case _ if recCount == 0:
                collection_name.insert_one(itemImport)
            case _ if recCount == 1:
                record = collection_name.find_one({"tcdbUrl": tcdbUrl})
                objDiff = DeepDiff(record, itemImport, exclude_paths="root['_id']")
                if objDiff != {}:
                    filter = { '_id': record["_id"] }
                    newvalues = { "$set": {
                        "title": itemImport["title"],
                        "publisher": itemImport["publisher"],
                        "setName": itemImport["setName"],
                        "subSet": itemImport["subSet"],
                        "setCount": itemImport["setCount"],
                        "releaseDate": itemImport["releaseDate"],
                        "setYear": itemImport["setYear"],
                        "tcdbUrl": itemImport["tcdbUrl"],
                        "priceguideUrl": itemImport["priceguideUrl"],
                        "setType": itemImport["setType"]
                        }
                    }
                    collection_name.update_one(filter, newvalues)
            case _ if recCount > 1:
                for j in record:
                    collection_name.delete_one({"title": j["title"],
                                            "publisher": j["publisher"],
                                            "setName": j["setName"],
                                            "subSet": j["subSet"],
                                            "setCount": j["setCount"],
                                            "releaseDate": j["releaseDate"],
                                            "setYear": j["setYear"],
                                            "tcdbUrl": j["tcdbUrl"],
                                            "priceguideUrl": j["priceguideUrl"],
                                            "setType": j["setType"]})
                collection_name.insert_one(itemImport)

        idx += 1
        print(idx, "Complete:", i["tcdbUrl"])


    