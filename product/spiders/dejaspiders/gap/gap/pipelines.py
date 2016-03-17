# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from src.utils.config import RAW_INFO_TAG_ROOT
from src.spiders.spider_pipeline import SpiderPipeline as TagPipline
from src.spiders.spider_pipeline import SpiderSkuPipeline as ProductPipline
from os.path import join
class GapTagPipeline(TagPipline):
    def process_item(self, item, spider):
        data_diretory = join(RAW_INFO_TAG_ROOT, GAP_DATA_DIRECTORY)
        TagPipline.process_item(self, item, spider, data_diretory)
        return item

class GapProductPipeline(ProductPipline):
    def process_item(self, item, spider):
        ProductPipline.process_item(self, item, spider)
        return item