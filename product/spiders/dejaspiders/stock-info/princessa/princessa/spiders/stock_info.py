import os, sys
import scrapy
from src.utils.config import BATCH_SIZE, REQUEST_HEADER, REQUEST_META, ProductStatus, BuySize
from src.utils.db.db_helper import DbHelper
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import  get_project_settings
from src.spiders.spider_item import SpiderItem
from scrapy.item import Item
from src.utils.counter_helper import Counter
import numpy as np
from src.utils.scrapy_settings.setting_config import ProjectSettings
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import re, time, logging, json
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class PrincessaInfoSpider(scrapy.Spider):
    name = 'princessa_info'
    allowed_domains = ['shopprincessa.com']
    merchant_id = 76
    start_urls = (
        "http://www.shopprincessa.com/",
    )

    def parse(self, response):
        product_number = 0
        mydb = DbHelper()
        self.merchant_id = 82
        product_urls = mydb.get_urlPid(self.merchant_id, product_number, BATCH_SIZE)
        for product in product_urls:
            item = {}
            item['pid'] = product['pid']
            item['id'] = product['id']
            yield Request(product["shop_url"], meta = item, callback = self.parseInfo)

    def parseInfo(self, response):
        print "here starting the parse"
        print response.url
        item = SpiderItem()
        item['pid'] = response.meta['pid']
        item['id'] = response.meta['id']
        soup =  BeautifulSoup(str(response.body), 'lxml')
        stock = soup.select("form.variations_form")
        # here is just a trick
        variations =  stock[0].get('data-product_variations')
        var_json = json.loads(variations)

        regular_price  = 0
        price = 0
        item['stock_info'] = {}
        item['buy_size_type'] = 'UK'
        item['buy_size'] = ['S', 'M', 'L']
        for i in var_json:
            regular_price= float(i['display_regular_price'])
            price = float(i['display_price'])
            if  not i["attributes"]["attribute_pa_warehouse"] == "singapore":
                continue
            size  = i["attributes"]["attribute_pa_size"]
            print type(i['is_in_stock'])
            if i['is_in_stock']:
                item['stock_info']['UK '+size[0].upper()] = 1
            else:
                item['stock_info']['UK '+size[0].upper()] = 0
        if regular_price == price:
            item['price'] = int(price*100)
            item['discount_price'] = 0
            item['discount_percent'] = 0
        else:
            item['discount_price'] = int(regular_price - price) * 100
            item['discount_percent'] = int(item['discount_price']/regular_price)
            item['price'] = int(price*100)
        item['buy_color'] = []
        item['buy_size_type'] = 'UK'
        item['status'] = 0
        yield item


if __name__ == '__main__':
    os.environ["SCRAPY_SETTINGS_MODULE"] = "src.spiders.princessa.princessa.settings"
    process = CrawlerProcess(get_project_settings())
    process.crawl(PrincessaInfoSpider)
    process.start()
    print 'done'
