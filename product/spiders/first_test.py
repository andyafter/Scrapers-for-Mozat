# -*- coding: utf-8 -*-
import scrapy


class FirstTestSpider(scrapy.Spider):
    name = "first_test"
    allowed_domains = ["http://www.zalora.sg/"]
    start_urls = (
        'http://www.http://www.zalora.sg//',
    )

    def parse(self, response):
        pass
