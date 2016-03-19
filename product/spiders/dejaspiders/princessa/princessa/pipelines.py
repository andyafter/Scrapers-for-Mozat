# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from src.utils.config import RAW_INFO_TAG_ROOT
from src.spiders.spider_pipeline import ProductPipeline as ProductPipline
from os.path import join


class PrincessaProductPipeline(ProductPipline):
    def process_item(self, item, spider):
        ProductPipline.process_item(self, item, spider)
        return item
