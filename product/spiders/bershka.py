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
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import re
import time
import logging




class BershkaSpider(Spider):
    name = "bershka"
    allowed_domains = ["bershka.com"]
    start_urls = (
        'http://www.bershka.com/sg/',
    )

    def __init__(self):
        self.driver = webdriver.Firefox()
        selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
        # Only display possible problems
        selenium_logger.setLevel(logging.WARNING)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.driver.close()

    def parse(self, response):
        self.driver.get(responsee.url)
        button = WebDriverWait(self.driver, 10).until(
            #EC.visibility_of_element_located((By.XPATH, "//li[contains(@id, '-link')]"))
            EC.visibility_of_element_located((By.XPATH, "//a"))
            # this here you should check out the following link:
            # https://saucelabs.com/resources/selenium/css-selectors
            )

        #links = self.driver.find_elements(By.XPATH, "//li[contains(@id, '-link')]")
        alinks = self.driver.find_elements(By.XPATH, "//a")
        links = []
        for link in alinks:
            if link.get_attribute('href') not in links:
                links.append(link.get_attribute('href'))
        for link in links:
            if self.start_urls[0] in link and 'woman' in link:
                self.parseBrief(link)
                print link
                break

    def parseBrief(self, link):
        self.driver.get(link)
        bg = self.driver.find_element_by_css_selector('body')

        # scroll till end
        lenOfPage = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
                lastCount = lenOfPage
                # here is the sleeping time
                time.sleep(0.1)
                lenOfPage = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                    match=True

        all_items = self.driver.find_elements(By.XPATH, "//li[contains(@class, 'item')]")

        item = {}
        links = {}
        for li in all_items:
            a = li.find_element_by_xpath("//a")
            item["url"] = a.get_attribute("href")
            img = li.find_element_by_xpath("//img")
            item['suitable_images'] = img.get_attribute('src')
            item['suitable_images_index'] = 1
            info = li.find_element_by_xpath("//div[contains(@class, 'prodinfo')]")
            price = li.find_element_by_xpath("//span[contains(@class, 'productPrice')]").text
            item['price'] = int(float(price[1:])*100)
            self.parseItem(item)
            break
        # actually here I cannot yield the whole stuff.

            # M-x comment-dwin
            # for link in  item.find_elements(By.XPATH, '//a'):
            #     print "right here"
            #     if  link.get_attribute('href') not in links:
            #         links[(link.get_attribute('href'))] = 0
            #         break


    def parseItem(self, partial_item):
        item = SpiderItem()
        print item['url'].split('/')
        item.update(partial_item)
        item['discount_price'] = 0
        item['brand_en'] ="bershka"
        item['merchant_en'] = 'Bershka'
        item['merchant'] = 85
        # C-m a s i (modify add spider item)
        # well if you use emacs, can go to my branch to download these
        # small stuff, works better if you are familiar
        item['white_suitable_images_index'] = 0
        item['white_suitable_images'] = ""
        item['']
        print item
        pass
