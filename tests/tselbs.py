from bs4 import BeautifulSoup
from selenium import webdriver

import time
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get('http://www.bershka.com/sg/new/woman/woman-c1133010.html')
elem = driver.find_element_by_xpath("//li[contains(@class, 'item')]")
lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match=False
while(match==False):
    lastCount = lenOfPage
    # here is the sleeping time
    time.sleep(0.1)
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    if lastCount==lenOfPage:
        match=True

all_items = driver.find_elements(By.XPATH, "//li[contains(@class, 'item')]/descendant::a[1]")
item['']
