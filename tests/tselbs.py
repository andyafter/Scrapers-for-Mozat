from bs4 import BeautifulSoup
from selenium import webdriver
driver = webdriver.Firefox()
driver.get('http://www.bershka.com/sg/')
elem = driver.find_element_by_tag_name('li')

driver.close()
