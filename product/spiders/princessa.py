# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose
from scrapy.http.request import Request

from configurable_spider.crawler_config import CrawlerConfigure


class PrincessaSpider(BaseSpider):
    name = "princessa"
    allowed_domains = ["shopprincessa.com"]
    start_urls = (
        'http://www.shopprincessa.com/',
    )

    def parse(self, response):
        print "Yes!!!!!"
        pass
