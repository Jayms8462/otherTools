#Chrome Locaiton: C:\Program Files\Google\Chrome\Application\chrome.exe -–remote-debugging-port=9222 -–user-data-dir=C:\Users\ajpor\OneDrive\Desktop\cardData\GoogleData
# SXVWzJaj#ZLZGPhG7$2hYe8@5LC6TC9fvtdViVKjxXU*skWzC4D2V&VzGn4mu%hM

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opt=Options()
opt.add_experimental_option("debuggerAddress", "localhost:9222")
driver=webdriver.Chrome(executable_path="C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\chromedriver.exe",options=opt)

driver.get("http://cnn.com")