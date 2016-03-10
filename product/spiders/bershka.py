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

# here I'm not using any configurable spiders so far

from bs4 import BeautifulSoup
import re

class BershkaSpider(Spider):
    name = "bershka"
    allowed_domains = ["bershka.com"]
    start_urls = (
        'http://www.bershka.com/',
    )

    def parse(self, response):
        soup = BeautifulSoup(str(response.body), 'lxml')
        print soup
        for link in soup.findAll('a', {'class' : 'ng-binding'}):
            print link
        pass
