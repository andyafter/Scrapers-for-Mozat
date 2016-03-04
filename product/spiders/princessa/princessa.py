# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose
from scrapy.http.request import Request
from product.items import SpiderItem

from product.spiders.configurable_spider.crawler_config import CrawlerConfigure
from product.spiders.configurable_spider.constants import *
from product.spiders.configurable_spider.common_utils import getLogger, qualify_link

logger = getLogger(__name__)


class PrincessaSpider(Spider):
    name = "princessa"
    allowed_domains = ["shopprincessa.com"]
    start_urls = (
        'http://www.shopprincessa.com/',
    )

    '''
    # will come back to configurable crawler later
    def __init__(self, config, config_file, **kwargs):
        super(Spider, self).__init__(**kwargs)
        self.config = CrawlerConfigure(config, config_file).config
        self.conf_name = self.config[NAME]
        self.parsed_collection_page = []
    '''

    def parse(self, response):
        print "Yes!!!!!"
        print "right here"
        item = SpiderItem()
        item['category'] = "hahaha"
        item['info'] = "info"
        item['name'] = "andy"
        item['brand_en'] = "andybrand"
        item['description'] = 'as'
        item['pid'] = "12345"
        item['merchant'] = 1
        item['detail_images'] = "ima|ima"
        item['detail_image_path'] = "haha|haha"
        item['suitable_images'] = "hahahaha"
        item['suitable_images_index'] = 0
        item['white_suitable_images_index'] = 0
        item['white_suitable_images'] = "haha"

        item['url'] = 'sdajsdad'
        item['merchant_en'] = "ba"
        item['brand_en'] = 'soe'
        item['price'] = 100
        item['discount_price'] = 20

        yield item


'''
if __name__ == '__main__':
    #os.environ["SCRAPY_SETTINGS_MODULE"] = "src.spiders.young_hungry_free_configurable.young_hungry_free_configurable.settings"
    process = CrawlerProcess(get_project_settings())
    process.crawl(ConfigurableSpider,*(None, 'princessa.json'))
    process.start()
    print 'Finished'
'''
