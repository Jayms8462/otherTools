import os
import time
import re
from os.path import exists
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

os.system('cls' if os.name == 'nt' else 'clear')

options = Options()
options.binary_location = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
options.add_argument("detach=True")
options.headless = True
driver = webdriver.Firefox(executable_path=r'C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\geckodriver.exe', options=options)

def getCards(storage):
    table = driver.find_element(By.CLASS_NAME, "table.table-sm.table-hover")
    tableRow = table.find_elements(By.TAG_NAME, "tr")
    for i in tableRow:
        if i.text == 'Card Median Price':
            continue
        tableRowData = re.split(r'   ', i.text)
        cardUrl = i.find_element(By.TAG_NAME, "td").find_element(By.TAG_NAME, "a").get_attribute("href")
        tableRowData = url + '\t' + tableRowData[0] + '\t' + tableRowData[1] + '\t' + cardUrl
        storage.append(tableRowData)
    return storage

count = []
fileCount = 15
index = 0
nextLink = False
file = "data"

with open("urls.txt", "r", encoding="utf-8") as h:
    urls = h.readlines()
    for url in urls:
        start = time.time()
        url = url.replace('\n', '')
        try:
            url = url.replace('/ViewSet.cfm/', '/Prices.cfm/')
            driver.get(url)
            index += 1
            storage = []

            while driver.current_url == 'https://www.tcdb.com/DefaultError.html':
                print("Error, Trying Again: " + url)
                time.sleep(30)
                driver.get(url)
            
            if nextLink == False:
                try:
                    driver.find_element(By.LINK_TEXT, "›")
                    nextLink = True
                except:
                    getCards(storage)

            while nextLink == True:
                try: 
                    getCards(storage)
                    driver.find_element(By.LINK_TEXT, "›").click()
                except:
                    getCards(storage)
                    nextLink = False
            for i in storage:
                with open(file + str(fileCount) + ".txt", "r", encoding="utf-8") as f:
                    if len(f.readlines()) >= 500000:
                        fileCount+=1
                f.close()

                with open(file + str(fileCount) + ".txt", 'a', encoding="utf-8") as f:
                    f.write(i + "\n")
                f.close()
            end = time.time()
            print(index, "Completed:", url, "Runtime:", end - start)          
                    
        except:
            with open("error.txt", 'a', encoding="utf-8") as g:
                g.write(url + "\n")
            g.close()
            print("Error on: ", url)
