# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from scrapy_sqlitem import SqlItem
from models import ItemInfo


class ProductItem(SqlItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sqlmodel = ItemInfo
    '''
    name = scrapy.Field()
    pid = scrapy.Field()
    tag_source =scrapy.Field()
    # unless strongly urged I'm not gonna write any nullables
    tag_id =scrapy.Field()
    update_time = scrapy.Field()
    category = scrapy.Field()
    sub_category = scrapy.Field()
    brand = scrapy.Field()
    detail_images = scrapy.Field()
    thumb_images = scrapy.Field()
    suitable_images = scrapy.Field()
    white_suitable = scrapy.Field()
    tag_status = scrapy.Field()
    visenze_result = scrapy.Field()
    merchant = scrapy.Field()
    koutu = scrapy.Field()
    shop_url = scrapy.Field()
    brand_en = scrapy.Field()
    merchant_en = scrapy.Field()
    price = scrapy.Field()
    discount_price = scrapy.Field()
    discount_percent = scrapy.Field()
    buy_size = scrapy.Field()
    buy_color = scrapy.Field()
    stock_info = scrapy.Field()
    status = scrapy.Field()
    '''

class Test(Item):
    """Livingsocial container (dictionary-like object) for scraped data"""
    title = Field()
