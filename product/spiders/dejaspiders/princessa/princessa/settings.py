# -*- coding: utf-8 -*-

BOT_NAME = 'princessa'

SPIDER_MODULES = ['src.spiders.princessa.princessa.spiders']
NEWSPIDER_MODULE = 'src.spiders.princessa.princessa.spiders'


DOWNLOADER_MIDDLEWARES = {
   'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
   'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,

}

ITEM_PIPELINES = {
    'src.spiders.princessa.princessa.pipelines.PrincessaProductPipeline': 400,
 }

COOKIES_ENABLED=True
