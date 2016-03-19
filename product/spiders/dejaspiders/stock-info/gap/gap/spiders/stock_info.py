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
import re, time, logging
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class GapInfoSpider(scrapy.Spider):
    name = 'gap_info'
    allowed_domains = ['gap.com']
    merchant_id = 76
    start_urls = (
        "http://www.gap.com/",
    )
    def __init__(self):
        self.web_driver = webdriver.Chrome()
        selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
        selenium_logger.setLevel(logging.WARNING)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
         self.web_driver.close()

    def parse(self, response):
        print "gap"*13
        product_number = 0
        mydb = DbHelper()
        product_urls = mydb.get_urlPid(self.merchant_id, product_number, BATCH_SIZE)
        for product in product_urls:
            print product
            self.web_driver.get(product['shop_url'])
            try:
                close = WebDriverWait(self.web_driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@id, "closeButton")]'))
                        )
            except Exception as e:
                print e

            hv = ActionChains(self.web_driver).move_to_element(close[0]).click()
            hv.perform()

            item = SpiderItem()
            item['pid'] = product['pid']
            item['id'] = product['id']
            item['status'] = 1
            item['stock_info'] = {}
            item['buy_color'] = []
            item['buy_size_type'] = "US"
            strike = self.web_driver.find_elements_by_css_selector('div#colorSwatchContent strike')
            if len(strike) == 1:
                after_discount = float(strike[0].text[1:])
                sale = float(self.web_driver.find_element_by_css_selector('div#colorSwatchContent span.salePrice').text[1:])
                item['price'] = int(sale*100)
                item['discount_price'] = int(sale -after_discount)*100
            else:
                price = self.web_driver.find_element_by_css_selector('span#priceText')
                item['price'] = int(float(price.text[1:]))*100
                item['discount_price'] = 0

            item['discount_percent'] = float(item['discount_price'])/item['price']

            swatch = self.web_driver.find_elements_by_css_selector('div#swatchContent')
            print "swatch"*12
            print len(swatch), swatch[0].text.split('\n')
            item['buy_size'] = ['00']
            for i in range(11):
                item['buy_size'].append(str(2*i))
            # here omitted the tab stuff
            # tab_on = self.web_driver.find_elements_by_xpath('//li[contains(@class, "varianttab on")]')
            # tab_off = self.web_driver.find_elements_by_xpath('//li[contains(@class, "varianttab off")]')
            # print len(tab_on), len(tab_off)
            # for tab in tab_off:
            #     webdriver.ActionChains(self.web_driver).move_to_element(tab).click(tab).perform()
            #     content = self.web_driver.find_element_by_css_selector('div#swatchContent')
            #     print content.text

            try:
                    inputs = WebDriverWait(self.web_driver, 10).until(
                            EC.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "colorSwatch_")]'))
                        )
            except Exception as e:
                print e

            time.sleep(10) # this is important
            for i in inputs:
                #print "input", i.get_attribute('class'), i.get_attribute('type')
                color =" ".join(i.get_attribute('alt').split()[:-1])
                item['buy_color'].append(color)
                hv = ActionChains(self.web_driver).move_to_element(i)
                hv.perform()
                hv.click()
                hv.perform()
                time.sleep(1)
                try:
                    labels = WebDriverWait(self.web_driver, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//label'))
                    )
                except Exception as e:
                    print e

                for label in labels:
                    if "select" in label.get_attribute('innerHTML').lower():
                        if 'regular' in label.get_attribute('innerHTML').lower():
                            continue
                        c = label.get_attribute('innerHTML').split()
                        if len(c)<3:
                            continue
                        # print label .get_attribute('innerHTML')
                        size_color = "US "+ c[-1] + "_" +color
                        item['stock_info'][size_color] = 1
            if item['stock_info'] == {}:
                item['status'] = 1
            else:
                item['status'] = 0
            # print "length of inputs", len(inputs)
            yield item


if __name__ == '__main__':
    os.environ["SCRAPY_SETTINGS_MODULE"] = "src.spiders.gap.gap.settings"
    process = CrawlerProcess(get_project_settings())
    process.crawl(GapInfoSpider)
    process.start()
    print 'done'
