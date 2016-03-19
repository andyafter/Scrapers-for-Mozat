# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose
from scrapy.http.request import Request
from product.items import SpiderItem

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
        #category_links = soup.find_all('li', {"class": "_category-links"})
        category_links = soup.find_all('li')
        for link in category_links:
            if not link.get('class'):
                continue
            if '_category-link' in link.get('class'):
                for a in link.findAll('a'):
                    url = a.get('href')
                    meta  = {} # this is used to store the data
                    if a.string.lower() is 'view all':
                        print a.string
                        continue
                    meta['category'] = a.string
                    yield Request(url,meta = meta,
                                  callback = self.parseCategory)

    def parseCategory(self, response):
        soup = BeautifulSoup(str(response.body), 'lxml')
        products = soup.find_all('li')
        for link in products:
            if not link.get('class'):
                continue
            if 'product' in link.get('class'):
               meta = {}
               meta['url'] = 'http:' + link.find('a', {"class":'item'}).get('href')
               meta['pid'] = 'zara_' + link.get('id').split('-')[1]
               meta['name'] = link.find('a',{'class': 'name'}).string
               meta['category'] = response.meta['category']
               meta['suitable_images'] = link.find('img').get('src')
               meta['suitable_images_index'] = 1
               #meta['brand'] = 9 # brand id
               meta['merchant'] =74  # merchant id
               meta['brand_en'] = 'zara'
               meta['merchant_en'] = 'Zara'
               meta['discount_price'] = 0 # no discount in zata
               meta['white_suitable_images'] = " "
               meta['white_suitable_images_index'] = 0
               if  link.find('span'):
                   # might be empty
                   meta['price'] = int(float(link.find('span').get('data-price').split()[0])*100)
#        pass
               yield Request(meta['url'],meta = {'meta':meta},
                                  callback = self.parseItem)

    def parseItem(self, response):
        soup = BeautifulSoup(str(response.body), 'lxml')
        pics = soup.find_all('a',{"class": "_seoImg"})

        # if meta price is empty you can add price here
        meta = response.meta['meta']
        item = SpiderItem()

        # this is the version of pid from google drive doc
        n = 0
        for i in soup.findAll('p',{'class': 'reference'}):
            item['pid'] = 'zara_' + i.string.split()[1]

        item['info'] = ' ' # no information for this one
        item['description'] = item['info']

        # get price
        if not meta['price']:
            price = soup.findAll('p')
            for p in price:
                if not p.get('class'):
                    continue
                if 'price' in p.get('class'):
                    # simply because that in the doc, price was tagged as integer
                    meta['price'] = int(float(p.find('span').get('data-price'))*100)
                    print meta['price']

        for i in meta:
            if i is 'image':
                continue
            else:
                if i  in item:
                    continue
                item[i] = meta[i]

        images = []
        for img in pics:
            images.append(img.get('href'))
        item['detail_image_path'] = '|'.join(images)

        #item['description'] = soup.find('p',{'class': 'description'}).find('span').string
        yield item
