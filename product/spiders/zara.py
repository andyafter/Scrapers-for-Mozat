# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose
from bs4 import BeautifulSoup


class ZaraSpider(BaseSpider):
    name = "zara"
    allowed_domains = ["zara.com"]
    start_urls = (
        'http://www.zara.com/sg/',
    )

    def parse(self, response):
        print "start parsing!!!"
        soup = BeautifulSoup(str(response.body), 'lxml')
        #print response.body
        category_links = soup.find_all('li', {"class": "_category-link     "})
        print category_links
        pass
