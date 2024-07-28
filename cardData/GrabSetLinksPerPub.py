from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

driver = webdriver.Firefox()

link = [

]

for url in link:

    driver.get(url)

    pageLinks = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[2]").find_elements(By.TAG_NAME, "a")
    setType = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/nav/ol/li[3]/a").text

    for i in pageLinks:
        if "Gallery.cfm" not in i.get_attribute("href"):
            title = i.text
            link = i.get_attribute("href")
            with open("dataUrl.txt", 'a', encoding="utf-8") as f:
                f.write(title + "\t" + link + "\t" + setType + "\n")
            f.close()
    print("Complete Url: ", url)