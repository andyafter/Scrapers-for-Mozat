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
        'http://www.gap.com/',
    )

    def parse(self, response):
        soup = BeautifulSoup(str(response.body), 'lxml')
        all_links = soup.find_all('a')
        for link in all_links:
            #print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
            if link.get('href'):
                print link.get('href')
        pass
