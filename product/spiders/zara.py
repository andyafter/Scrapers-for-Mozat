# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose
from scrapy.http.request import Request

from scrapy_sqlitem import SqlSpider
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
        print response.meta
        soup = BeautifulSoup(str(response.body), 'lxml')
        #return None
        pass

    def parseItem(self, response):
        soup = BeautifulSoup(str(response.body), 'lxml')
        pics = soup.find_all('a',{"class": "_seoImg"})

        # if meta price is empty you can add price here
        meta = response.meta['meta']
        item = ProductItem()

        # get price
        if not meta['price']:
            price = soup.findAll('p')
            for p in price:
                if not p.get('class'):
                    continue
                if 'price' in p.get('class'):
                    # simply because that in the doc, price was tagged as integer
                    meta['price'] = int(float(p.find('span').get('data-price')))

        for i in meta:
            if i is 'image':
                continue
            else:
                if i  in item:
                    continue
                print i
                item[i] = meta[i]

        # write some wrapper for this one
        # for thumb_imagesite
        item['detail_images'] = meta['image']
        for img in pics:
            item['detail_images'] += "|" + img.get('href')
        item['thumb_images'] = " "
        timg = soup.find_all('div',{'class': 'colors _colors'})
        item['buy_color'] = ' '

        for img in timg:
            if item['thumb_images'] == '':
                item['thumb_images'] = img.find('img').get('src')
            item['thumb_images'] += '|' + img.find('img').get('src')
            for c in img.find_all('span'):
                if not c.string:
                    continue
                item['buy_color'] += ' ' + c.string
                print c.string
        # did not find any description in the model
        #item['description'] = soup.find('p',{'class': 'description'}).find('span').string


        yield item
