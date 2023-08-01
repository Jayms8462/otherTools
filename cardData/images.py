import os
import time
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import concurrent.futures
import urllib3
import subprocess

http = urllib3.PoolManager()

os.system('cls' if os.name == 'nt' else 'clear')

options = Options()
options.binary_location = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
options.add_argument("detach=True")
options.headless = True
driver = webdriver.Firefox(executable_path=r'C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\geckodriver.exe', options=options)
# driver = webdri
# 
# ver.Chrome('C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\chromedriver.exe')

urls = [
]

def getCards(storCount, url):
    table = driver.find_element(By.CLASS_NAME, "table.table-sm.table-hover")
    tableRow = table.find_elements(By.TAG_NAME, "tr")
    for i in tableRow:
        if i.text == 'Card Median Price':
            continue
        tableRowData = re.split(r'   ', i.text)
        cardUrl = i.find_element(By.TAG_NAME, "td").find_element(By.TAG_NAME, "a").get_attribute("href")
        tableRowData = "\t".join([url, tableRowData[0], tableRowData[1], cardUrl])

        with open("Data/" + storCount, 'a', encoding="utf-8") as f:
            f.write(tableRowData + "\n")
        f.close()

def errorUrl(url):
    time.sleep(30)
    driver.get(url)

nextLink, count = False, 0

for url in urls:
    path = "data"
    dir_list = os.listdir(path)
    for file in dir_list:
        if file == "cardsDB.xlsx" or file == "titles.txt" or file == "~$cardsDB.xlsx":
            continue
        else:
            with open("Data/" + file, "r", encoding="utf-8") as f:
                if len(f.readlines()) >= 500000:
                    continue
                elif file == dir_list[-1]:
                    storCount = "data" + str(len(dir_list) + 1) + ".txt"
                    break
                else:
                    storCount = file
                    break
    
    url = url.replace('\n', '')
    try:
        url = url.replace('/ViewSet.cfm/', '/Prices.cfm/')
        driver.get(url)

        while driver.current_url == 'https://www.tcdb.com/DefaultError.html':
            print("Default Page Failure, Trying Again:", url)
            errorUrl(url)

        if nextLink == False:
            try:
                driver.find_element(By.LINK_TEXT, "›")
                nextLink = True
            except:
                getCards(storCount, url)

        while nextLink == True:
            try: 
                getCards(storCount, url)
                time.sleep(2)
                driver.find_element(By.LINK_TEXT, "›").click()
            except:
                getCards(storCount, url)
                nextLink = False
        count += 1
        print(count, file, "Completed:", url)   
                
    except:
        with open("error.txt", 'a', encoding="utf-8") as g:
            g.write(url + "\n")
        g.close()
        print("Error on: ", url)

# def main():
#     with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
#         executor.map(getData, urls)

# if __name__ == '__main__':
#     main()