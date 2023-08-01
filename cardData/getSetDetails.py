from pymongo import MongoClient
import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from deepdiff import DeepDiff
import csv

os.system('cls' if os.name == 'nt' else 'clear')

options = Options()
options.binary_location = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
options.add_argument("detach=True")
options.headless= True
driver = webdriver.Firefox(executable_path=r'C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\geckodriver.exe', options=options)

def exportSetToCsv(itemImport):
     with open('cardsSet.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([itemImport["title"], 
                         itemImport["publisher"], 
                         itemImport["setName"], 
                         itemImport["subSet"], 
                         itemImport["setCount"], 
                         itemImport["releaseDate"], 
                         itemImport["setYear"], 
                         itemImport["tcdbUrl"], 
                         itemImport["priceguideUrl"], 
                         itemImport["setType"]])
def errorItems(i):
    print("Error on:", i)
    with open("errorUrl.txt", 'a', encoding="utf-8") as f:
        f.write(i)
    f.close()
        
with open('urls.txt') as data:
        idx = 0
        for i in data:
            try:
                i = i.replace('\n', '')
                driver.get(i)
                errorNum = 0
                urlCheck = driver.current_url
                urlCheckIf = False
                if 'https://www.tcdb.com/DefaultError.html' in urlCheck:
                    urlCheckIf = True

                while urlCheckIf == True:
                    errorNum += 1
                    print("Error, Trying Again: ", i)
                    time.sleep(30)
                    if errorNum < 3:
                        driver.get(i)
                        if 'https://www.tcdb.com/DefaultError.html' not in urlCheck:
                            urlCheckIf = False
                    else:
                        errorItems(i)
                        urlCheckIf = False
                        continue   
                try:
                    title = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/h4").text
                except NoSuchElementException:
                    try:
                        title = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/p[1]/strong").text
                    except:
                        title = ""

                try:
                    setCount = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/p[1]").text
                    setCount = int(setCount.split('Total Cards: ')[1].replace(',', ''))
                except NoSuchElementException:
                    try:
                        setCount = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/p[2]").text
                        setCount = int(setCount.split('Total Cards: ')[1].replace(',', ''))
                    except:
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
                    tcdbUrl = i.replace('\n','')
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
                exportSetToCsv(itemImport)

                idx += 1
                print(idx, "Complete:", i)
            except:
                errorItems(i)