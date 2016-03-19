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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import re, time, logging
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class BershkaInfoSpider(scrapy.Spider):
    name = 'bershka_info'
    allowed_domains = ['bershka.com']
    merchant_id = 85
    start_urls = (
        "http://www.bershka.com/sg/",
    )
    def __init__(self):
        self.web_driver = webdriver.Chrome()
        selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
        # Only display possible problems
        selenium_logger.setLevel(logging.WARNING)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
         self.web_driver.close()
         pass

    def parse(self, response):
        product_number = 0
        mydb = DbHelper()
        product_urls = mydb.get_urlPid(self.merchant_id, product_number, BATCH_SIZE)
        for prod in product_urls:
            url = prod['shop_url']
            item = SpiderItem()
            item['pid'] = prod['pid']
            item['id'] = prod['id']
            self.web_driver.get(url)
            try:
                elem = WebDriverWait(self.web_driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//span'))
                    )
            except Exception as e:
                print e

            color_list = self.web_driver.find_elements_by_css_selector( 'div.prodColorInfo span')
                # so css works some times
            item['buy_color'] = []
            for i in color_list:
                item['buy_color'].append(i.get_attribute('innerHTML'))

            size_list = self.web_driver.find_elements_by_css_selector('ul.sizes span')
            item['buy_size_type'] = 'UK'
            item['buy_size'] = []
            for i in size_list:
                item['buy_size'].append(i.get_attribute('innerHTML'))

            price = self.web_driver.find_elements_by_css_selector('div.prodInfo span.productPrice')
            item['price'] = int(float(price[0].text[1:])*100)
            item['discount_price'] = 0
            item['discount_percent'] = 0
            item['stock_info'] = {}
            for color in item['buy_color']:
                for size in item['buy_size']:
                    info = "UK "+size+"_"+color
                    item['stock_info'][info] = 1

            if item['buy_color'] == [] or item['buy_size'] == []:
                item['status'] = 0
            item['status'] = 1

            yield item




if __name__ == '__main__':
    os.environ["SCRAPY_SETTINGS_MODULE"] = "src.spiders.bershka.bershka.settings"
    process = CrawlerProcess(get_project_settings())
    process.crawl(BershkaInfoSpider)
    process.start()
    print 'done'
