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
        self.driver.get(response.url)
        # button = WebDriverWait(self.driver, 10).until(
        #     #EC.visibility_of_element_located((By.XPATH, "//li[contains(@id, '-link')]"))
        #     EC.visibility_of_element_located((By.XPATH, "//a"))
        #     # this here you should check out the following link:
        #     # https://saucelabs.com/resources/selenium/css-selectors
        #     )
        #doc = self.driver.execute_script('return document;')
        links = self.driver.find_elements(By.XPATH, "//li[contains(@id, '-link')]")
        alinks = li.find_elements(By.XPATH, "//a")
        links = []
        for link in alinks:
            if link.get_attribute('href') not in links:
                links.append(link.get_attribute('href'))
        for link in links:
            if self.start_urls[0] in link and 'woman' in link:
                yield self.parseBrief(link)
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
                time.sleep(0.5)
                lenOfPage = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                    match=True

        doc = self.driver.execute_script('return document;')
        all_items = self.driver.find_elements(By.XPATH, "//li[contains(@class, 'item')]")

        links = {}
        for li in all_items:
            item = {}
            tag = li.get_attribute('innerHTML')
            soup = BeautifulSoup(str(tag), 'lxml')
            image =  soup.find('img')
            a = soup.find('a')
            s = soup.find_all('span')
            for i in s:
                if not i.get('class'):
                    continue
                if 'productPrice' in i.get('class'):
                    price = i.get_text()
            item["url"] = a.get("href")
            item['suitable_images'] =image.get('src')
            item['suitable_images_index'] = 1
            #price = li.find_element_by_xpath("//span[contains(@class, 'productPrice')]").text
            item['price'] = int(float(price[1:])*100)
            yield self.parseItem(item)
            break

    def parseItem(self, partial_item):
        print "item parsing"
        item = SpiderItem()
        item.update(partial_item)
        self.driver.get(item['url'])
        item['discount_price'] = 0
        item['brand_en'] ="bershka"
        item['merchant_en'] = 'Bershka'
        item['merchant'] = 85
        # C-m a s i (modify add spider item)
        # well if you use emacs, can go to my branch to download these
        # small stuff, works better if you are familiar
        item['white_suitable_images_index'] = 0
        item['white_suitable_images'] = ""
        pid = self.driver.execute_script("return inditex.iParams.categoryId;")
        item['pid'] = 'bershka_' + str(int(pid[0]))
        category = self.driver.execute_script("return inditex.iCategoryKey;")
        # there are many ways of finding category
        item['category'] = ' '.join(item['url'].split('/')[-1].split('-'))
        item['description'] = self.driver.find_element_by_xpath("//meta[@name='description']").get_attribute('content')
        item['name'] = self.driver.title.split('-')[0]
        doc = self.driver.execute_script('return document;')
        imgs = doc.find_elements_by_tag_name("img")
        images = []
        for i in imgs:
            link = i.get_attribute('src')
            if link:
                if len(link.split('/'))==14:
                    print link
                    images.append(link)
        item['detail_image_path'] = "|".join(images)
        item['suitable_images'] = images[0]
        item['info'] = doc.find_element_by_id('compositionboxScroll')
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print item
        return  item
