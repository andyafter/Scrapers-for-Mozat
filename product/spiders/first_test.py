# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

from product.items import ProductItem


class FirstTestSpider(BaseSpider):
    name = "first_test"
    allowed_domains = ["zalora.sg"]
    start_urls = (
        'http://www.zalora.sg//',
    )

    deals_list_xpath = '//li[@dealid]'
    item_fields = {
        'title': './/span[@itemscope]/meta[@itemprop="name"]/@content',
    }

    def parse(self, response):
        result = ProductItem()
        print "here is the parse"
        print result
        #yield  result
        pass
