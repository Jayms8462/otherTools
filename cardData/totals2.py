import os
import time
from os.path import exists
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

os.system('cls' if os.name == 'nt' else 'clear')
# if os.path.exists('C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\count.txt'):
#     os.remove('C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\count.txt')
# if os.path.exists('C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\errorUrl.txt'):
#     os.remove('C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\errorUrl.txt')

options = Options()
options.binary_location = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
options.add_argument("detach=True")
options.headless= True
driver = webdriver.Firefox(executable_path=r'C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\geckodriver.exe', options=options)

urls = [

]

count = []
index = 0

for url in urls:
    try:
        errorNum = 0
        urlViewSet = url.replace("ViewSet.cfm", "Checklist.cfm")
        driver.get(urlViewSet)
        index += 1
        while driver.current_url == 'https://www.tcdb.com/DefaultError.html':
            errorNum += 1
            print("Error, Trying Again: " + url)
            time.sleep(30)
            if errorNum <= 3:
                driver.get(url)
            else:
                continue   

        cardCount= driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/p[2]/strong").text
        if cardCount == "Total Cards:":
            cardCountNum = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/p[2]").text
            cardCountNum = cardCountNum.split(' ')
            cardCountNum = cardCountNum[2]
            setCat = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/div/nav/ol/li[2]/a").text
            with open("count.txt", 'a', encoding="utf-8") as f:
                f.write(url + "\t" + cardCountNum + "\t" + setCat + "\n")
            f.close()
            print(index, " Url Complete: ", url)
        else:
            try:
                cardNum = 0
                pages = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/nav/ul").text
                pages = pages.split("\n")
                pages = pages[: len(pages) - 2]
                for i in pages:
                    pageUrl = urlViewSet + '?PageIndex=' + i
                    driver.get(pageUrl)
                    tableData = driver.find_elements(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[1]/table[2]/tbody/tr')
                    cardNum += len(tableData)
                setCat = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/div/nav/ol/li[2]/a").text
                with open("count.txt", 'a', encoding="utf-8") as f:
                    f.write(url + "\t" + str(cardNum) + "\t" + setCat + "\n")
                f.close()
                print(index, " Url Complete: ", url)
            except:
                tableData = driver.find_elements(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/table[2]/tbody/tr")
                cardNum += len(tableData)
                setCat = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/div/nav/ol/li[2]/a").text
                with open("count.txt", 'a', encoding="utf-8") as f:
                    f.write(url + "\t" + str(cardNum) + "\t" + setCat + "\n")
                f.close()
                print(index, " Url Complete: ", url)
    except NoSuchElementException:
        with open("errorUrl.txt", 'a', encoding="utf-8") as f:
            f.write(url + "\n")
        f.close()
        print(index, " Error Url: ", url)