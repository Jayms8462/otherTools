import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
import os
from selenium.webdriver.common.keys import Keys
import shutil

# C:\Users\ajpor\OneDrive\Desktop\drivers\Chrome>chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\ajpor\OneDrive\Desktop\drivers\chromedriver\chromeprofile"

options = Options()
options.add_experimental_option("debuggerAddress","localhost:9222")
driver = webdriver.Chrome(executable_path="C:\\Users\\ajpor\\OneDrive\\Desktop\\drivers\\chromedriver\\chromedriver.exe", chrome_options=options)  # Optional argument, if not specified will search path.

urls = [
    "https://www.priceguide.cards/checklist/25319/S/1995-topps-stadium-club-baseball-cards---clear-cut-standard"
]


# driver.get('https://getcardbase.com/user-sets/create')

def makeDir(sport, set, subSet):
    while  not os.path.exists('C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\Images\\' + sport + '\\' + set + '\\' + subSet):   
        if not os.path.exists('C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\Images\\' + sport):
            os.mkdir('C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\Images\\' + sport)
        elif not os.path.exists('C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\Images\\' + sport + '\\' + set):
            os.mkdir('C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\Images\\' + sport + '\\' + set)
        elif not os.path.exists('C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\Images\\' + sport + '\\' + set + '\\' + subSet):
            os.mkdir('C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\Images\\' + sport + '\\' + set + '\\' + subSet)

def imageData(link, rowCardNum, rowCardPlayer, sport, set, subSet):
    makeDir(sport, set, subSet)

    try:
        if not os.path.exists("C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\Images\\" + sport + "\\" + set + "\\" + subSet + "\\#" + rowCardNum + " " + rowCardPlayer.replace(":", "") + ".jpg"):
            var = requests.get(link)
            with open("C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\Images\\" + sport + "\\" + set + "\\" + subSet + "\\#" + rowCardNum + " " + rowCardPlayer.replace(":", "").replace(" / ", ", ").replace("/", ", ") + ".jpg", 'wb') as f:
                f.write(var.content)
    except:
        imageData(link, rowCardNum, rowCardPlayer, sport, set, subSet)

    filePath = 'C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\Images\\' + sport + '\\' + set + '\\' + subSet
    return filePath

def getData(sport, set, subSet):
    body = driver.find_element(By.CSS_SELECTOR, "body")

    idx = 0
    while idx <= 6:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.75)
        idx += 1

    tableRow = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[4]/div[3]/div/table/tbody")
    tableLineAll = tableRow.find_elements(By.TAG_NAME, "tr")
    for i in tableLineAll:
        imageInfo = []
        rowCardNum = i.find_elements(By.TAG_NAME, "td")[2].text
        rowCardPlayer = i.find_elements(By.TAG_NAME, "td")[3].text
        rowCardPlayer = rowCardPlayer.replace('"', '')
        rowImages = i.find_elements(By.TAG_NAME, "img")
        for j in rowImages:
            imageInfo.append(j.get_attribute("src"))

        if any("https" in j for j in imageInfo):
            for k in imageInfo:
                if "https://" in k:
                    link = k
                    filePath = imageData(link, rowCardNum, rowCardPlayer, sport, set, subSet)
            print("Complete: #" + rowCardNum + " " + rowCardPlayer)
        else:
            if os.path.exists('C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\Images\\' + sport + '\\' + set + '\\' + subSet):
                with open("downloadFail.txt", "a") as f:
                    f.write(rowCardNum + "\t" + rowCardPlayer + "\n")
                filePath = 'C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\Images\\' + sport + '\\' + set + '\\' + subSet
            else:
                filePath = 'C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\Images\\' + sport + '\\' + set + '\\' + subSet
                makeDir(sport, set, subSet)
                with open("downloadFail.txt", "a") as f:
                    f.write(rowCardNum + "\t" + rowCardPlayer + "\n")
    return filePath

for url in urls:
    os.system('cls' if os.name == 'nt' else 'clear')
    driver.get(url)
    try:
        driver.find_element(By.XPATH, "/html/body/div/div[1]/div[1]/div/div/div[1]")
        input("Complete Security Check and press any button:")
        sport = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[3]/div/div[1]").text
        set = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/nav/ol/li[2]/a/span").text
        set = set.replace(" Baseball", "")
        subSet = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/nav/ol/li[3]/a/span").text
    except:
        sport = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[3]/div/div[1]").text
        set = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/nav/ol/li[2]/a/span").text
        set = set.replace(" Baseball", "")
        subSet = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/nav/ol/li[3]/a/span").text

    # sportClassification = input("Sport Classification: " + sport + "?: ")
    # if sportClassification == "y":
    #     sport = sport
    # else:
    #     sport = input("What Sport is the card set?: ")

    # setClassification = input("Set Classification: " + set + "?: ")
    # if setClassification == "y":
    #     set = set
    # else:
    #     set = input("What is the card set?: ")

    # subsetClassification = input("SubSet Classification: " + subSet + "?: ")
    # if subsetClassification == "y":
    #     subSet = subSet
    # else:
    #     subSet = input("What is the sub set of the cards: ")


    try:
        pageList = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[4]/div[2]/div").find_elements(By.TAG_NAME, "li")
        pageList = len(pageList) - 2
        index = 1

        while index <= pageList:
            try:
                driver.find_element(By.XPATH, "/html/body/div[6]/div/div")
                input("Press Any Key once security check is complete:")
            except:
                filePath = getData(sport, set, subSet)

                if index != pageList:
                    nextLinkCount = pageList + 2
                    nextLink = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[5]/div[2]/div/li[" + str(nextLinkCount) + "]/a/img").click()
                    
                    time.sleep(2)
                index += 1

    except NoSuchElementException:
        filePath = getData(sport, set, subSet)

    if os.path.exists("downloadFail.txt"):
        shutil.move("downloadFail.txt", filePath)
