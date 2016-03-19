BOT_NAME = 'gap_info'

SPIDER_MODULES = ['src.spiders.gap.gap.spiders']
NEWSPIDER_MODULE = 'src.spiders.gap.gap'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
}

ITEM_PIPELINES = ['src.spiders.spider_pipeline.SpiderPipeline']
