# -*- coding: utf-8 -*-
import scrapy
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


class GapSpider(scrapy.Spider):
    name = "gap"
    allowed_domains = ["gap.com"]
    start_urls = (
        'http://www.gap.com/browse/subDivision.do?cid=5646&mlink=5058,10323290,visnav&clink=10323290',
    )

    def parse(self, response):
        soup = BeautifulSoup(str(response.body), 'lxml')
        # testing for item parsing
        print "parsing item testing"
        all_links = soup.find_all('li',{'class':'category'})
        for i in all_links:
            print i.find('a').get('href')
        # man boys toddler
        exclude = ["men", "boys", "toddler", "baby", "gap factory"]
        # we don't care about gap factory first
        for link in all_links:
            print link.get('class')
            for li in link:
                if type(li.find('a')) == int:
                    continue
                print li.find('a').get_text()
        # test the get_text part
        # here takes another round to get all the category links

        #url = "http://www.gap.com/browse/subDivision.do?cid=5646&mlink=5058,10323290,visnav&clink=10323290"
        #url = "http://www.gap.com/browse/category.do?cid=1033762&departmentRedirect=true#department=136"
        #yield Request(url, callback = self.parseBrief)
        pass

    def parseBrief(self, response):
        # I don't care about the
        soup = BeautifulSoup(str(response.body), 'lxml')
        cate_links = soup.find_all("li", {'class': 'category'})
        # for i in cate_links:
        #     print i.find('a')
        item_links  = soup.find_all("li")
        items = []
        for link in item_links:
            if not link.get('id'):
                print "oh, no id"
                continue
            if "categoryProductItem" in link.get("id"):
                items.append(link.find("a"))
        print "length of item links", len(item_links)
        #items = item_links.find_all('li')
        #print "items", len(items)
        print "items", len(items)
        pass
