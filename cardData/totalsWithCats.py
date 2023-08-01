import os
import pyautogui ### Allows pressing of keys
from os.path import exists
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

os.system('cls' if os.name == 'nt' else 'clear')

options = Options()
options.binary_location = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
options.add_argument("detach=True")
# options.headless= True
driver = webdriver.Firefox(executable_path=r'C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\geckodriver.exe', options=options)
driver.maximize_window()

urls = [
    "https://www.tcdb.com/ViewAll.cfm/sp/Baseball/year/1987",

]

for url in urls:
    try:
        driver.get(url)
        pyautogui.keyDown('ctrl')
        pyautogui.press('-')
        pyautogui.press('-')
        pyautogui.press('-')
        pyautogui.press('-')
        pyautogui.keyUp('ctrl')
        sets = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/div").find_elements(By.TAG_NAME, "a")
        urlData = []
        for i in sets:
            urlData.append(i.get_attribute("href"))
        listLen = len(urlData)
        index = 0
        while index < listLen:
            arrowList = []
            listList = []
            driver.get(urlData[index])
            xpath = "/html/body/div[1]/div[3]/div[1]/div[2]/ul[" +  str(index + 1) + "]"
            list = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[2]").find_element(By.XPATH, xpath).find_elements(By.TAG_NAME, "img")
            listLenEle = len(list)
            for j in list:
                arrowList.append(j.get_attribute("id"))
            for j in reversed(arrowList):
                driver.find_element(By.ID, j).click()
            listLinks = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[2]").find_element(By.XPATH, xpath).find_elements(By.TAG_NAME, "a")
            for j in listLinks:
                listList.append(j.get_attribute("href"))
            for j in listList:
                with open("links.txt", 'a', encoding="utf-8") as f:
                    f.write(j + "\n")
                f.close()
            index += 1
            driver.refresh()
        print("Complete:", url)
    except:
        with open("errors.txt", 'a', encoding="utf-8") as f:
            f.write(url + "\t" + urlData[index] + "\n")
        f.close()