# -*- coding: utf-8 -*-
import scrapy


class HmSpider(scrapy.Spider):
    name = "hm"
    allowed_domains = ["http://www.hm.com/sg/"]
    start_urls = (
        'http://www.http://www.hm.com/sg//',
    )

    def parse(self, response):
        pass
