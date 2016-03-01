# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose
from scrapy.http.request import Request

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
        #category_links = soup.find_all('li', {"class": "_category-links"})
        category_links = soup.find_all('li')
        for link in category_links:
            if not link.get('class'):
                continue
            if '_category-link' in link.get('class'):
                # category links are all the categories
                # click inside there will be a list of li tags whoes class contains
                # "product", and these li tags contains information that you need
                # after you click inside the product refereces, there will be detailed information
                # that you need
                for a in link.findAll('a'):
                    url = a.get('href')
                    meta  = {} # this is used to store the data
                    yield Request(url,meta = meta,
                                  callback = self.parseCategory)

    def parseCategory(self, response):
        print "calling back"
        print response.meta
        soup = BeautifulSoup(str(response.body), 'lxml')
        #return None
        pass

    def parseItem(self, response):

        pass
