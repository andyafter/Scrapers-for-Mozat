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

from product.spiders.configurable_spider.crawler_config import CrawlerConfigure
from product.spiders.configurable_spider.constants import *
from product.spiders.configurable_spider.common_utils import getLogger, qualify_link

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from ghost import Ghost
import re
#from ghost import Ghost
from selenium import selenium

# starting the ghost for crawler
#ghost = Ghost()


class DesigualSpider(Spider):
    name = "desigual"
    allowed_domains = ["www.desigual.com"]
    start_urls = (
        'http://www.desigual.com/en_MT/',
    )


    def __init__(self):
        # well actually after I have went through the site I found that the following links contain
        # everything
        self.urls = [
            "http://www.desigual.com/en_MT/women/clothing/see-all/"
            #"http://www.desigual.com/en_MT/living/decor/homewear/"
        ]
        self.img = {}
        self.count = 0
        self.sel = selenium("localhost", 8000, "*firefox","http://www.desigual.com/en_MT/women/")
        self.sel.start()

    def parse(self, response):
        sel = self.sel
        print sel.get_html_source()
        '''
        for i in range(2,33):
            # wired, when you set the number larger than the maximum
            # it always returns the last page
            self.urls.append(self.urls[0] + 'page/' + str(i) +'/')
        for link in self.urls:
            yield Request(link, callback = self.parseBrief)
            break
        '''

    def parseBrief(self, response):
        soup = BeautifulSoup(str(response.body), 'lxml')
        category_links = soup.find_all('div', {'class': 'image quick-buy-item subsection-col'})

        for link in category_links:
            self.count += 1
            print link
            img = link.find('img').get('src')
            #print link.find('div').get('id')
            #yield Request(link, callback = self.parseItem)
            yield Request(img, callback = self.parseItem)
            break


    def parseItem(self, response):
        soup = BeautifulSoup(str(response.body), 'lxml')
        img_links = soup.find_all('img')
        for i in img_links:
            print i

        pass
