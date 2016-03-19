# -*- coding: utf-8 -*-
import scrapy
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.xlib.pydispatch import dispatcher
from src.utils.config import REQUEST_HEADER, REQUEST_META, HM_INFO
from src.spiders.princessa.princessa.items import PrincessaItem
from src.spiders.spider_item import SpiderItem
from scrapy.http.request import Request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import logging
import re, os


class PrincessaSpider(scrapy.Spider):
    name = "princessa"
    allowed_domains = ["shopprincessa.com"]
    start_urls = (
        'http://www.shopprincessa.com/store',
    )

    def __init__(self, **kwargs):
        super(PrincessaSpider, self).__init__(self, **kwargs)

    def parse(self, response):
        list_url = "http://www.shopprincessa.com/store"
        soup = BeautifulSoup(str(response.body), 'lxml')
        all_links = soup.find_all('ul', {"class": "page-numbers"})
        pages = all_links[0].find_all('a', {'class':'page-numbers'})
        page_number = -1
        for p in pages:
            number = p.get('href').split('/')[-1]
            if page_number<int(number):
                page_number = int(number)

        print "page_numbers", page_number

        store_urls = []
        store_urls.append(list_url)
        for i in range(2, page_number+1):
            store_urls.append(list_url+'/page/'+ str(i))

        print store_urls

        for link in store_urls:
            yield Request(link, callback=self.parseBrief)

    def parseBrief(self, response):
        print response.url
        soup = BeautifulSoup(str(response.body), 'lxml')
        product = soup.select('div.products-loop div.product')
        print len(product), "here is the product loop"*3

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
            item['white_suitable_images'] = ""
            item['white_suitable_images_index'] = 0
            item['merchant_en'] = 'Princessa'
            item['brand_en'] = 'princessa'
            item['name'] = link.find('div', {'class': 'product-title'}).get_text()
            item['info'] = link.find('div',{'class': 'product-excerpt'}).get_text().split(')')[-1]
            for des in link.find('div',{'class': 'product-excerpt'}):
                item['description'] = des.strip()
                break
            item['pid'] ='princessa_'+ link.find('span', {'class': 'show-quickly'}).get('data-prodid')

            price = link.find('span', {'class': 'amount'}).get_text()
            item['price'] = int(float(price[1:])*100)
            item['discount_price'] = 0 #

            for i in link.find_all('a', {'class': 'product-content-image'}):
                item['detail_image_path'] = '|'.join(i.get('data-images').split(','))
            item['group_id'] = ""
            yield item


if __name__ == '__main__':
    os.environ["SCRAPY_SETTINGS_MODULE"] = "src.spiders.princessa.princessa.settings"
    process = CrawlerProcess(get_project_settings())
    process.crawl(PrincessaSpider)
    process.start()
    print "finished"
