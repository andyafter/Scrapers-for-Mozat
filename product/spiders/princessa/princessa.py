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
import re

logger = getLogger(__name__)


class PrincessaSpider(Spider):
    name = "princessa"
    allowed_domains = ["shopprincessa.com"]
    start_urls = (
        'http://www.shopprincessa.com/',
    )

    def __init__(self):
        # simple method to deal with XHR in this website
        self.urls = ['http://www.shopprincessa.com/store' + '/page/' + str(i) for i in range(2,21)]
        self.urls.append('http://www.shopprincessa.com/store')

    def parse(self, response):
        for link in self.urls:
            print "links"
            yield Request(link, callback = self.parseBrief)

    def parseBrief(self, response):
        soup = BeautifulSoup(str(response.body), 'lxml')
        product = soup.find_all('div', {'class': re.compile(r'product\b')})
        brief = soup.find_all('a', {'class': 'product-content-image'})
        for link in product:
            if 'product' not in link.get('class'):
                continue
            item = SpiderItem()
            #print link.get('class')
            item['merchant'] = 82
            item['url'] =  link.find('a').get('href')
            item['category'] = "Princessa women" # since here there is no way you can find the category
            item['suitable_images'] = link.find('img').get('src')
            item['suitable_images_index'] = 1
            item['white_suitable_images'] = " "
            item['white_suitable_images_index'] = 0
            item['merchant_en'] = 'Princessa'
            item['brand_en'] = 'princessa'
            item['name'] = link.find('div', {'class': 'product-title'}).get_text()
            item['info'] = link.find('div',{'class': 'product-excerpt'}).get_text().split(')')[-1]
            for des in link.find('div',{'class': 'product-excerpt'}):
                item['description'] = des.strip()
                break
            item['pid'] ='princessa-'+ link.find('span', {'class': 'show-quickly'}).get('data-prodid')

            price = link.find('span', {'class': 'amount'}).get_text()
            item['price'] = int(float(price[1:])*100)
            item['discount_price'] = 0 # not sure, didn't find any

            for i in link.find_all('a', {'class': 'product-content-image'}):
                item['detail_image_path'] = '|'.join(i.get('data-images').split(','))
            yield item
