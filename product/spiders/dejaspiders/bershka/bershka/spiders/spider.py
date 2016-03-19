# -*- coding: utf-8 -*-
import scrapy
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.xlib.pydispatch import dispatcher
from src.utils.config import REQUEST_HEADER, REQUEST_META, HM_INFO
from src.spiders.gap.gap.items import GapItem
from src.utils.config import GAP_INFO
from src.spiders.spider_item import  SpiderItem
from scrapy.http import Request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib2 import Request, urlopen
from bs4 import BeautifulSoup
import logging
import re
import os, sys, time

# this is for running in emacs
from twisted.internet import reactor


class BershkaSpider(scrapy.Spider):
    name = "bershka"
    allowed_domains = ["bershka.com"]
    start_urls = (
        'http://www.bershka.com/sg/',
    )

    def __init__(self):
        #self.driver = webdriver.Firefox()
        self.web_driver = webdriver.Chrome()
        selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
        # Only display possible problems
        selenium_logger.setLevel(logging.WARNING)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
         self.web_driver.close()

    def parse(self, response):
        self.web_driver.get(response.url)
        exclude = ["man"] # man dress is the only category that should be eliminated
        try:
            elem = WebDriverWait(self.web_driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//a'))
            )
        except Exception as e:
            print e

        all_cates = []
        for el in elem:
            link = el.get_attribute('href') #
            if not link:
                continue
            if len(link.split("/"))<=6: #  this is what is needed
                continue
            if "man" in link.split('/'):
                continue
            print link
            if link not in all_cates:
                all_cates.append(link)

        return

        # this here parse the item list page
        for link in all_cates:
            items = self.parseBrief(link)
            for item in items:
                spider_item = SpiderItem()
                spider_item.update(item)
                i = self.parseItem(item["url"])
                spider_item.update(i)
                yield spider_item


    def parseBrief(self, link):
        self.web_driver.get(link)
        try:
            elem = WebDriverWait(self.web_driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class, "item")]'))
            )
        except Exception as e:
            print e
        bg = self.web_driver.find_element_by_xpath('//body[@class="desktop"]')
        # scroll till end
        lenOfPage = self.web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
                lastCount = lenOfPage
                time.sleep(1)
                lenOfPage = self.web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                    match=True

        result = []
        #  result contains basic information about each item
        for idx, el in enumerate(elem):
            li_tag = el.get_attribute('innerHTML')
            # make sure that there is no unicode problem:
            soup = BeautifulSoup(str(li_tag.encode('ascii', 'ignore')), 'lxml')
            item = {}
            item["url"] = soup.find('a').get('href')
            item["suitable_images"] = soup.find('img').get('src')
            item['suitable_images_index'] = 0 #
            el_text = el.text.split('\n')
            name, price = "", ""
            if len(el_text) == 1:
                price = el_text[0]
            elif len(el_text) == 2:
                name = el_text[0]
                price = el_text[1]
            else:
                print el_text, "something wrong here"
            item["name"] = name
            if '-' in price:
                item["price"] = int(price.split('-')[0][1:].replace('.', ''))
            else:
                item["price"] = int(price[1:].replace('.',''))
            result.append(item)
        return result

    def parseItem(self, url):
        self.web_driver.get(url)
        try:
            elem = WebDriverWait(self.web_driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//img'))
            )
        except Exception as e:
            print e
        images = []
        for i in elem:
            if not i.get_attribute('data-ng-click'):
                continue
            src =  i.get_attribute('src')
            if not src:
                continue
            images.append(src)
        item = {}
        item['detail_image_path'] = '|'.join(images)
        item["name"] = self.web_driver.title.split('-')[0]
        item['description'] = self.web_driver.find_element_by_xpath("//meta[@name='description']").get_attribute('content')
        item["white_suitable_images_index"] = 0
        item["white_suitable_images"] = ""
        item['discount_price'] = 0
        item['brand_en'] ="bershka"
        item['merchant_en'] = 'Bershka'
        item['merchant'] = 85
        item['discount_price'] = 0
        item['info'] = ""
        item['group_id'] = ""
        s = url.split('/')
        item['category'] = s[4]+ " " + s[6]
        item['pid'] = 'bershka_'+s[-1].split('p')[-1].split('.')[0]
        return item

if __name__ == '__main__':
    # to run on emacs  you should  C-u C-c C-c
    #sys.path.append('/User/panan/Desktop/crawler/deja-product')
    os.environ["SCRAPY_SETTINGS_MODULE"] = "src.spiders.bershka.bershka.settings"
    process = CrawlerProcess(get_project_settings())
    process.crawl(BershkaSpider)
    process.start()
    print "finished"
