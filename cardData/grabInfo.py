from pymongo import MongoClient
import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.service import Service
from deepdiff import DeepDiff
import csv
import argparse
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path='./login.env')

parser = argparse.ArgumentParser(description='A Script to grab into from tcdb.com and collect the card data. \
                                 Adding this data to the respective DB and killing the process. \
                                 This script is designed to operate on independant systems to distribute the workload between them. \
                                 -u or --username, username for DB auth \
                                 -p or --password, password for db auth \
                                 -U or --url ***Required***, Sets Url e.x. https://www.tcdb.com/ViewSet.cfm/sid/132133/1990-Green-Bay-Packers-Police \
                                 -H or --host ***Required***, host to run the script \
                                 -P or --port ***Required***, mongodb port number')
parser.add_argument('-u', '--username', type=str, default=os.getenv('user'), help='Username for DB Auth')
parser.add_argument('-p', '--password', type=str, default=os.getenv('password'), help='Password for DB Auth')
parser.add_argument('-U', '--url', type=str, required=True, help="Sets Url e.x. https://www.tcdb.com/ViewSet.cfm/sid/132133/1990-Green-Bay-Packers-Police")
parser.add_argument('-H', '--host', type=str, required=True, help="host to run the script")
parser.add_argument('-P', '--port', type=str, required=True, help="mongodb port number")
args = parser.parse_args()

if os.name == 'nt':
    os.system('cls')
    try:
        service = Service(executable_path=r'C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\geckodriver.exe')
        options = Options()
        options.binary_location = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
        options.add_argument("detach=True")
        options.add_argument("-headless")
        driver = webdriver.Firefox(service=service, options=options, log_path="./geckodriver.log")
    except:
        service = Service(executable_path=r'C:\\Users\\ajpor\\Desktop\\git\\otherTools\\cardData\\geckodriver.exe')
        options = Options()
        options.binary_location = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
        options.add_argument("detach=True")
        options.add_argument("-headless")
        driver = webdriver.Firefox(service=service, options=options, log_path="./geckodriver.log")

def get_database():
   dbString = "mongodb://" + args.username + ':' + args.password + "@" + args.host + ":" + args.port
   CONNECTION_STRING = dbString
   client = MongoClient(CONNECTION_STRING)
   return client['cardDB']

class setInfo:
    def __init__(self, title, publisher, setName, subSet, setCount, releaseDate, setYear, tcdbUrl, priceguideUrl, setType):
        self.title = title
        self.publisher = publisher
        self.setName = setName
        self.subSet = subSet
        self.setCount = setCount
        self.releaseDate = releaseDate
        self.setYear = setYear
        self.tcdbUrl = tcdbUrl
        self.priceguideUrl = priceguideUrl
        self.setType = setType

class cardImport:
    def __init__(self, cardNum, playerName, playerTeam, playerExtra, unfilteredData, cardUrl, cardSet, setYear, setType, tcdbUrl, priceguideUrl):
        self.cardNum = cardNum
        self.playerName = playerName
        self.playerTeam = playerTeam
        self.playerExtra = playerExtra
        self.unfilteredData = unfilteredData
        self.cardUrl = cardUrl
        self.cardSet = cardSet
        self.setYear = setYear
        self.setType = setType
        self.tcdbUrl = tcdbUrl
        self.priceguideUrl = priceguideUrl

def errorItems(i):
    print("Error on:", i)
    with open("errorUrl.txt", 'a', encoding="utf-8") as f:
        f.write(i + '\n')
    f.close()

def validateData(string, isMatch, url):
    # To Validate that the set title and Url Match
    if string in url:
        isMatch = True
    else:
        isMatch = False
    return isMatch

def checkDupRecord(setDbName, valData, recordCheckUrl, type, typeSearch):
    collection_name = dbname[setDbName]
    recordCount = collection_name.count_documents({typeSearch: recordCheckUrl})
    match recordCount:
        case 0:
            collection_name.insert_one(valData.__dict__)
        case 1:
            record = collection_name.find({typeSearch: recordCheckUrl})
            for i in record:
                match type:
                    case 'set':
                        recordCl = setInfo(title=i["title"], publisher=i["publisher"], setName=i["setName"], subSet=i["subSet"], setCount=i["setCount"], releaseDate=i["releaseDate"], setYear=i["setYear"], tcdbUrl=i["tcdbUrl"], priceguideUrl=i["priceguideUrl"], setType=i["setType"])
                    case 'card':
                        recordCl = cardImport(cardNum=i["cardNum"], playerName=i["playerName"], playerTeam=i["playerTeam"], playerExtra=i["playerExtra"], unfilteredData=i["unfilteredData"], cardUrl=i["cardUrl"], cardSet=i["cardSet"], setYear=i["setYear"], setType=i["setType"], tcdbUrl=i["tcdbUrl"], priceguideUrl=i["priceguideUrl"])

            objDiff = DeepDiff(recordCl, valData, exclude_paths="root['_id']")
            if objDiff != {}:
                collection_name.delete_one({typeSearch: recordCheckUrl})
                collection_name.insert_one(valData.__dict__)
        case _ if recordCount > 1:
            record = collection_name.find({typeSearch: recordCheckUrl})
            for i in record:
                collection_name.delete_one({typeSearch: recordCheckUrl})
            collection_name.insert_one(valData.__dict__)

def getCardInfo(driver, url):
    cardSet = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/p[1]/strong").text
    tcdbUrl = url
    setYear = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/div[1]/nav/ol/li[4]/a").text
    setType = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/div[1]/nav/ol/li[2]/a").text
    tableEle = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/table[2]/tbody").find_elements(By.TAG_NAME, "tr")
    priceguideUrl = ""
    for j in tableEle:
        cardUrlData = []
        tableData = j.text.replace('\n', '\t').replace('   ', '\t').replace('  ', '').split('\t')
        for k in j.find_elements(By.TAG_NAME, "a"):
            if k.get_attribute("href") != None:
                if "ViewCard.cfm" in k.get_attribute("href"):
                    if k.get_attribute("href") not in cardUrlData:
                        cardUrlData.append(k.get_attribute("href"))
        if len(tableData) > 3:
                cardNum = tableData[0]
                playerName = tableData[1]
                playerTeam = tableData[3]
                playerExtra = tableData[2]
                unfilteredData = j.text.replace('\n', ' ')
                cardUrl = cardUrlData[0]
        elif len(tableData) == 2:
                cardNum = tableData[0]
                playerName = tableData[1]
                playerTeam = ""
                playerExtra = ""
                unfilteredData = j.text.replace('\n', ' ')
                cardUrl = cardUrlData[0]
        else:
                cardNum = tableData[0]
                playerName = tableData[1]
                playerTeam = tableData[2]
                playerExtra = ""
                unfilteredData = j.text.replace('\n', ' ')
                cardUrl = cardUrlData[0]
        cardData = cardImport(cardNum=cardNum, playerName=playerName, playerTeam=playerTeam, playerExtra=playerExtra, unfilteredData=unfilteredData, cardUrl=cardUrl, cardSet=cardSet, setYear=setYear, setType=setType, tcdbUrl=tcdbUrl, priceguideUrl=priceguideUrl)
        checkDupRecord(setDbName="cards", valData=cardData, recordCheckUrl=cardData.cardUrl, type="card", typeSearch="cardUrl")

def getSetData(driver, url, dbname):
    setTitle = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/p[1]/strong").text
    setTitleValidate = setTitle.split(' ')

    # Validate that title and url are a match for one another
    isMatch = False
    lenTitle = len(setTitleValidate)
    lenTitleValidate = 0
    for i in setTitleValidate:
        isMatch = False
        isMatch = validateData(i, isMatch, url)
        if isMatch == True:
            lenTitleValidate += 1
    if lenTitleValidate == lenTitle:
        setTotalCards = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/p[2]").text

        if 'Total Cards:' in setTotalCards:
            setTotalCards = int(setTotalCards.split("Total Cards: ")[-1])
        else:
            setTotalCards = 0

        try:
            setReleaseDate = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/ul/li").text
            if 'Release Date:' in setReleaseDate:
                setReleaseDate = setReleaseDate.split('Release Date: ')[-1]
            else:
                setReleaseDate = ""
        except:
            setReleaseDate = ""

        setYear = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/div/nav/ol/li[4]/a").text
        setType = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/div/nav/ol/li[2]/a").text
        setUrl = url
        setData = setInfo(title = setTitle, publisher = "", setName = "", subSet = "", setCount = setTotalCards, releaseDate = setReleaseDate, setYear = setYear, tcdbUrl = setUrl, priceguideUrl = "", setType = setType)

        checkDupRecord(setDbName="cardTitles", valData=setData, recordCheckUrl=setData.tcdbUrl, type="set", typeSearch="tcdbUrl")


if __name__ == "__main__":

    dbname = get_database()

    url = args.url
    urlChecklist = url.replace("ViewSet.cfm", "Checklist.cfm")
    idx = 0

    driver.get(urlChecklist)
    errorNum = 0
    while driver.current_url == 'https://www.tcdb.com/DefaultError.html':
        errorNum += 1
        print("Error, Trying Again:", url)
        time.sleep(30)
        if errorNum <= 3:
            driver.get(url)
        else:
            with open("errorUrl.txt", 'a', encoding="utf-8") as f:
                f.write(url)
            f.close()

    getSetData(driver, url, dbname)

    try:
        ### Multi Page Sets
        lastPage = driver.find_element(By.CLASS_NAME, "pagination.justify-content-center.flex-wrap").find_element(By.LINK_TEXT, "»").get_attribute("href")
        lastPageCount = int(lastPage.split('?PageIndex=')[-1])
        pageLink = 1
        while pageLink <= lastPageCount:
            driver.get(urlChecklist + "?PageIndex=" + str(pageLink))
            getCardInfo(driver, url)
            pageLink += 1
    except:
        getCardInfo(driver, url)

    driver.close()
    driver.quit()