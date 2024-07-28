from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import os

os.system('cls' if os.name == 'nt' else 'clear')

firefox_options = Options()
firefox_options.headless = True
driver = webdriver.Firefox(options=firefox_options)

link = [

]

for url in link:
    insertUrl = url.replace("ViewSet.cfm", "Inserts.cfm")
    
    driver.get(insertUrl)

    tableData = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]").find_elements(By.TAG_NAME, "table")
    setType = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/div/nav/ol/li[2]/a").text
    baseSetName = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/p[1]/strong").text

    for links in tableData:
        linkHref = links.find_elements(By.TAG_NAME, "a")
        for i in linkHref:
            if "Checklist.cfm" in i.get_attribute("href") and len(i.text) > 0:
                subSetName = i.text
                subSetLink = i.get_attribute("href")
                with open("dataUrl.txt", 'a', encoding="utf-8") as f:
                    f.write(baseSetName + " - " + subSetName + "\t" + subSetLink + "\t" + setType + "\n")
                f.close()
    print("Complete Url: ", url)