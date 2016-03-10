# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose
from scrapy.http.request import Request
from product.items import SpiderItem

from scrapy import signals
from scrapy.http import TextResponse
from scrapy.xlib.pydispatch import dispatcher

# here I'm not using any configurable spiders so far
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import re

class BershkaSpider(Spider):
    name = "bershka"
    allowed_domains = ["bershka.com"]
    start_urls = (
        'http://www.bershka.com/sg/',
    )

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.categories = ['NEW-link', 'WOMAN-link', 'Accessories-link', 'Shoes-link', ]
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.driver.close()

    def parse(self, response):
        self.driver.get(response.url)
        button = WebDriverWait(self.driver, 10).until(
                #EC.visibility_of_element_located(By.XPATH, "//li[id='WOMAN-link']")
            EC.visibility_of_element_located((By.XPATH, "//li[contains(@id, '-link')]"))
            # this here you should check out the following link:
            # https://saucelabs.com/resources/selenium/css-selectors
            )
        print button
        print dir(button)
        button.click()

        '''
        list = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//"))
            )
        '''
