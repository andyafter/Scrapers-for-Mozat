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
from urllib2 import Request, urlopen
from bs4 import BeautifulSoup
import logging
import re

test = {}

class GapSpider(scrapy.Spider):
    name = "gap"
    allowed_domains = ["gap.com"]
    start_urls = (
            'http://www.gap.com/',
    )
    URL_PREFIX = 'http://www.gap.com'
    def __init__(self, **kwargs):
        selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
        selenium_logger.setLevel(logging.WARNING)
        self.web_driver = webdriver.Firefox()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.web_driver.close()

    def parse(self, response):
        soup = BeautifulSoup(str(response.body), 'lxml')
        all_links = soup.find_all('ul',{'class':'gpnavigation'})
        # man boys toddler
        exclude = ["men", "boys", "toddler", "baby", "gap factory"]
        # we don't care about gap factory firstr
        all_cates = {}
        # select all categoies you want to search
        # general category anyway
        for link in all_links:
            for li in link:
                if type(li.find('a')) == int:
                    continue
                cate = li.find('a').get_text()
                carry_on = True
                for exc in exclude:
                    if exc in cate:
                        carry_on = False
                if not carry_on:
                    if cate != "women":
                        continue
                if '/' == li.find('a').get('href'):
                    continue
                all_cates[cate] = self.start_urls[0]+li.find('a').get('href')[1:]

        for cate in all_cates:
            categories = self.findCates(all_cates[cate])
            for cate in categories:
                list_page_url = self.start_urls[0]+categories[cate]
                item_brief_list = self.parseBrief(list_page_url)
                for item_brief in item_brief_list:
                    print "parsing item"
                    item = SpiderItem()
                    item["category"] = cate
                    item.update(item_brief)
                    item_url = self.start_urls[0] + item["url"][1:]
                    item_info = self.parseItem(item_url)
                    item.update(item_info)
                    item["merchant"] = 76
                    item["merchant_en"] = "Gap"
                    item["brand_en"] = "gap"
                    item["group_id"] = ""
                    yield item


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
        # test the get_text part
        # here takes another round to get all the category links

        url = "http://www.gap.com/browse/subDivision.do?cid=5646&mlink=5058,10323290,visnav&clink=10323290"
        #briefs = self.parseBrief()
        # testing item page
        item_url = "http://www.gap.com/browse/product.do?cid=1033765&vid=1&pid=130046022"
        #self.parseItem(item_url)
        pass

    def findCates(self, url):
        self.web_driver.get(url)
        try:
            # so after all this is probably the right way to find elements
            elem = WebDriverWait(self.web_driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class, "category")]'))
            )
        except Exception as e:
            print e

        result = {}
        for i in elem:
            soup = BeautifulSoup(str(i.get_attribute('innerHTML')), 'lxml')
            a = soup.find('a')
            if a.get_text() == "sale":
                continue
            result[a.get_text()] = a.get("href")
        return result

    def parseBrief(self, url):
        '''
        Parsing item list pages
        Returns: a list of item briefs, that contains price(discount price), name, link suitable image,
        pid.

        '''
        # I don't care about the
        # url = "http://www.gap.com/browse/category.do?cid=1033762&departmentRedirect=true#department=136"
        self.web_driver.get(url)
        try:
            # so after all this is probably the right way to find elements
            elem = WebDriverWait(self.web_driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class, "productCatItem")]'))
            )
        except Exception as e:
            print e
        result = []
        for i in elem:
            item = {}
            link_content= i.get_attribute("innerHTML")
            soup = BeautifulSoup(str(link_content), 'lxml')
            # turn it into soup so it'll be better

            name_link = soup.find("a", {"class": "productItemName"})
            if "".join(name_link.get_text().split()) == "":
                # get rid of outfits
                continue
            item["name"] = name_link.get_text()
            item["url"] = name_link.get("href")
            item["pid"] = 'gap_' + item["url"].split("=")[-1]
            item["suitable_images"] = soup.find("img").get("src")
            # find if there is any discount price existing
            discount = soup.find("span",{"class": "priceDisplayStrike"})
            # taking care of price here
            price = 0
            discount_price = 0
            if discount:
                ori_price = int(discount.get_text()[1:].replace('.', ''))
                p = soup.find("span",{"class": "priceDisplaySale"}).get_text()
                price = int(p[1:].replace('.',''))
                discount_price =  ori_price - price
                # oh yeah that is because that the dis_price is actually the striked
            else:
                discount_price = 0
                p = soup.find("span",{"class": "priceDisplay"}).get_text()
                price = int(p[1:].replace('.',''))
            item["discount_price"] = discount_price
            item["price"] = price
            result.append(item)
        return result

    def parseItem(self, url):
        '''
        Parsing item with url
        Args: url of item
            url: url of item
        Returns: item, in dictionary

        '''
        # take care of videos when choosing image
        self.web_driver.get(url)
        try:
            # so after all this is probably the right way to find elements
            elem = WebDriverWait(self.web_driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//input[contains(@class, "thumbs")]'))
            )
        except Exception as e:
            print e

        item = {}
        item["detail_image_path"] = ""
        images = []
        for i in elem:
             images.append(i.get_attribute('src'))
        item["detail_image_path"] = "|".join(images)
        item["suitable_images_index"] = 1
        item['white_suitable_images_index'] = 0
        item['white_suitable_images'] = ""

        try:
            # so after all this is probably the right way to find elements
            elem = WebDriverWait(self.web_driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@id, "tabWindow")]'))
            )
        except Exception as e:
            print e
        if len(elem) >= 1:
            item["info"] = elem[0].text
        try:
            # so after all this is probably the right way to find elements
            elem = WebDriverWait(self.web_driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//p[contains(@class, "description")]'))
            )
        except Exception as e:
            print e
        if len(elem)>=1:
            item["description"] = elem[0].text

        return item

def web_to_soup(elem, tag_name):
    '''
    Turning selenium web content element to specified content
    Returns:
    '''
    '''
    # test later putting webdriver as one of the input
    try:
            # so after all this is probably the right way to find elements
            elem = WebDriverWait(self.web_driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//input[contains(@class, "thumbs")]'))
            )
        except Exception as e:
            print e
    '''
    pass


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(GapSpider)
    process.start()
    print "finished"
