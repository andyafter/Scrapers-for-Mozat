# -*- coding: utf-8 -*-

# Scrapy settings for bershika project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'bershika'

SPIDER_MODULES = ['src.spiders.bershka.bershka.spiders']
NEWSPIDER_MODULE = 'src.spiders.bershka.bershka.spiders'


DOWNLOADER_MIDDLEWARES = {
   'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
   'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
}