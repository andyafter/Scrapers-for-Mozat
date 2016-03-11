from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


import time
from selenium.webdriver.common.by import By

url ="http://www.bershka.com/sg/new/woman/woman/front-embroidered-yoke-top-c1133010p100161532.html"
driver = webdriver.Firefox()
driver.get(url)

button = WebDriverWait(driver, 10).until(
    #EC.visibility_of_element_located((By.XPATH, "//li[contains(@id, '-link')]"))
    EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'slick-slide')]"))
    # this here you should check out the following link:
    # https://saucelabs.com/resources/selenium/css-selectors
)

elem = driver.find_element_by_xpath("//div[contains(@class, 'slick-track')]")




# lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
# match=False
# while(match==False):
#     lastCount = lenOfPage
#     # here is the sleeping time
#     time.sleep(0.1)
#     lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
#     if lastCount==lenOfPage:
#         match=True

# all_items = driver.find_elements(By.XPATH, "//li[contains(@class, 'item')]/descendant::a[1]")
# item['']
