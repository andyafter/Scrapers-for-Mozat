BOT_NAME = 'bershka_info'

SPIDER_MODULES = ['src.spiders.bershka.bershka.spiders']
NEWSPIDER_MODULE = 'src.spiders.bershka.bershka'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
}

ITEM_PIPELINES = ['src.spiders.spider_pipeline.SpiderPipeline']
