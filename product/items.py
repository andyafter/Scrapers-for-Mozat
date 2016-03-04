# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
from scrapy.item import Item, Field
from scrapy_sqlitem import SqlItem
from sqlalchemy import Table, MetaData
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, SmallInteger
from product.models import ItemInfo


class ProductItem(SqlItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sqlmodel = ItemInfo
    # this class seems to be use less anymore
    # I used dirty ways


class SpiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
#     def __init__(self):
    url = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    info = scrapy.Field()
    pid = scrapy.Field()
    price = scrapy.Field()
    detail_images = scrapy.Field()
    detail_image_path = scrapy.Field()
    discount_price = scrapy.Field()
    white_suitable_images = scrapy.Field()
    white_suitable_images_index = scrapy.Field()
    suitable_images = scrapy.Field()
    suitable_images_index = scrapy.Field()
    merchant = scrapy.Field()
    brand_en = scrapy.Field()
    merchant_en = scrapy.Field()
    pass
