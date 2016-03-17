# -*- coding: utf-8 -*-
import scrapy
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.xlib.pydispatch import dispatcher
from src.utils.config import REQUEST_HEADER, REQUEST_META, HM_INFO
from src.spiders.gap.gap.items import GapItem
from src.utils.config import GAP_INFO
from src.spiders.spider_item import  SpiderItem
from scrapy.http import Request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
from urllib2 import Request, urlopen
from bs4 import BeautifulSoup
import logging
import re


class BershkaSpider(scrapy.Spider):
    name = "bershka"
    allowed_domains = ["bershka.com"]
    start_urls = (
        'http://www.bershka.com/sg/',
    )

    def __init__(self):
        self.driver = webdriver.Chrome()
        selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
        # Only display possible problems
        selenium_logger.setLevel(logging.WARNING)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.driver.close()

    def parse(self, response):
        self.driver.get(response.url)
        # test for all links in the start page.
        try:
            elem = WebDriverWait(self.web_driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//a'))
            )
        except Exception as e:
            print e
        for el in elem:
            print el.get_attribute('innerHTML')

        pass
        '''
        item = SpiderItem()
        item['category'] = "hahaha" #done no specific column to find category name
        item['info'] = "info" # done
        item['name'] = "andy" # done
        item['brand_en'] = "andybrand" # done
        item['description'] = 'as' # done
        item['pid'] = "12345" # done
        item['merchant'] = 1 #
        item['detail_image_path'] = "haha|haha" # done
        item['suitable_images'] = "hahahaha" # done
        item['suitable_images_index'] = 0 #
        item['white_suitable_images_index'] = 0 # done
        item['white_suitable_images'] = "haha" # done
        item['url'] = 'sdajsdad' # done
        item['merchant_en'] = "ba" # done
        item['brand_en'] = 'soe' # done
        item['price'] = 100 # done
        item['discount_price'] = 20 # done
        '''
        pass

    def parseBrief(self, link):
        return []

    def parseItem(self, partial_item):
        print "item parsing"

        return

if __name__ == '__main__':
    #sys.path.append('/home/mozat/deja_product/deja-product')
    os.environ["SCRAPY_SETTINGS_MODULE"] = "src.spiders.bershka.bershka.settings"
    process = CrawlerProcess(get_project_settings())
    process.crawl(BershkaSpider)
    process.start()
    print "finished"